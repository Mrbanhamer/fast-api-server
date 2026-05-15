from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Original Imports
from user_schemas.task_schemas import User, UserWithPassword
from routes.users import user as user_router 
from routes.tasks import router as task_router
from utils.hash_password import verify_password

app = FastAPI()

# --- 1. CORS CONFIGURATION ---
# This allows your React frontend to talk to your API without security blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. PATH SETUP ---
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
frontend_path = os.path.join(project_root, "frontend")

# --- 3. INCLUDE ROUTERS (API Logic) ---
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/user")

print(f"--- PROJECT CHECK ---")
print(f"Base Path: {base_path}")
print(f"Checking for: {os.path.join(frontend_path, 'login.html')}")
print(f"Exists? {os.path.exists(os.path.join(frontend_path, 'login.html'))}")
print(f"---------------------")

# --- 4. API ENDPOINTS ---

# New endpoint for React to check connection
@app.get("/api/status")
async def get_status():
    return {"status": "online", "message": "Backend is reachable"}

# Your original Login logic, but updated to a cleaner API path
@app.post('/api/login')
async def login(data: UserWithPassword, response: Response):
    if data.action == 'profile':
        response.set_cookie(
            key="session_ticket", 
            value="your_secret_token", 
            path="/",
            httponly=True
        )
        return {"status": "success", "message": "Logged in successfully"}
    return {"status": "error", "message": "Login failed"}

# --- 5. FRONTEND SERVING (The "Professional" Way) ---

# This handles the home page (index.html)
@app.get("/")
async def read_index():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse(content="<h1>Frontend index.html not found</h1>", status_code=404)

# This mounts everything inside /frontend so CSS and JS are accessible
# We use "/static" as a prefix so it's clearly separated from API routes
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
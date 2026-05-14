from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Updated imports to reflect new backend structure
from user_schemas.task_schemas import User, UserWithPassword
from routes.users import user as user_router 
from routes.tasks import router as task_router
from utils.hash_password import verify_password

app = FastAPI()

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Path Setup: Pointing to the root of the project
# This looks at backend/ and goes up one level to find the project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
frontend_path = os.path.join(project_root, "frontend")

# 2. Mounting Static Files
# We check if directories exist to prevent the server from crashing
if os.path.exists(os.path.join(frontend_path, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")

if os.path.exists(os.path.join(frontend_path, "javascript")):
    app.mount("/javascript", StaticFiles(directory=os.path.join(frontend_path, "javascript")), name="javascript")

# Mount the entire frontend folder as well
app.mount("/frontend_assets", StaticFiles(directory=frontend_path), name="frontend_assets")

# Include Routers
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/user", tags=["users"])

@app.get('/index', response_class=HTMLResponse)
async def get_login():
    # Use the absolute path to ensure index.html is found
    index_file = os.path.join(frontend_path, "index.html")
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content=f"<h1>Frontend index.html not found at {index_file}</h1>", status_code=404)

@app.post('/index')
async def login(data: UserWithPassword, response: Response):
    if data.action == 'profile':
        response.set_cookie(
            key="session_ticket", 
            value="your_secret_token", 
            path="/",
            httponly=True
        )
        return {"status": "success", "url": "/user/"}

if __name__ == '__main__':
    import uvicorn
    # Make sure we run the app from the correct location
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
from fastapi import FastAPI, Request, Response # Added Response
from fastapi.responses import HTMLResponse, JSONResponse # Added JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from user.users_properties import User, UserWithPassword
from routes.users import user as user_router # Renamed for clarity
from utils.hash_password import verify_password
from routes.tasks import router as task_router

app = FastAPI()

# 1. Get the absolute path to your front_end folder
# We use 'os' to make sure it finds the folder regardless of where you start the terminal
script_dir = os.path.dirname(__file__)
frontend_path = os.path.join(script_dir, "src", "front_end")

# 2. Mount the subfolders so the browser can reach them
# This links http://127.0.0.1:8000/css to your actual css folder
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")

# This links http://127.0.0.1:8000/javascript to your actual javascript folder
app.mount("/javascript", StaticFiles(directory=os.path.join(frontend_path, "javascript")), name="javascript")

app.include_router(user_router)
app.include_router(task_router)

# 1. You MUST include your router for /user/ to work!
app.include_router(user_router, prefix="/user")

# frontend directions
app.mount("/front_end", StaticFiles(directory="src/front_end"), name="front_end")

@app.get('/index', response_class=HTMLResponse)
async def get_login():
    try:
        with open('src/front_end/index.html', 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>File not found</h1>", status_code=404)

@app.post('/index')
async def login(data: UserWithPassword, response: Response):
    if data.action == 'profile':
        response.set_cookie(
            key="session_ticket", 
            value="your_secret_token", 
            path="/", # This makes the cookie available to ALL routes, including /user/
            httponly=True
        )
        return {"status": "success", "url": "/user/"}




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
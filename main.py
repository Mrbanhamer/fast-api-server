from fastapi import FastAPI, Request, Response # Added Response
from fastapi.responses import HTMLResponse, JSONResponse # Added JSONResponse
from fastapi.staticfiles import StaticFiles

from user.users_properties import User, UserWithPassword
from routes.users import user as user_router # Renamed for clarity
from utils.hash_password import verify_password

app = FastAPI()

app.include_router(user_router)

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
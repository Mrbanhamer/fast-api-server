from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm
import uuid
import os

# --- DATABASE IMPORTS ---
from database.sql_connector import (
    log_new_user, 
    is_ticket_in_db, 
    save_ticket, 
    get_user_id_from_email, 
    delete_ticket_from_db,
    login as db_login
)
from user_schemas.user_auth import UserSignup

user = APIRouter(prefix="/user", tags=["Users"])

# This ensures we find the frontend folder regardless of where you start the app
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
frontend_path = os.path.join(project_root, "frontend")

print(f"--- PROJECT CHECK ---")
print(f"Base Path: {base_path}")
print(f"Checking for: {os.path.join(frontend_path, 'login.html')}")
print(f"Exists? {os.path.exists(os.path.join(frontend_path, 'login.html'))}")
print(f"---------------------")

@user.get('/me')
async def get_my_info(request: Request):
    ticket = request.cookies.get("session_ticket")
    user_data = is_ticket_in_db(ticket) 
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid session")
    return {
        "name": user_data['name'],
        "last_name": user_data['last_name'],
        "email": user_data['email']
    }

# --- SIGN-UP ---
@user.get('/signup')
async def get_signup_page():
    # Shorter, cleaner, and handles the 'open/read' for you
    return FileResponse(os.path.join(frontend_path, "signup.html"))

@user.post('/signup')
async def signup_action(data: UserSignup = Depends(UserSignup.as_form)):
    success = log_new_user(data.name, data.last_name, data.email, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Signup Failed")

    user_id = get_user_id_from_email(data.email) 
    new_ticket = str(uuid.uuid4())
    save_ticket(user_id, new_ticket)

    response = RedirectResponse(url="/user/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_ticket", value=new_ticket, httponly=True, path="/")
    return response

# --- LOGIN ---
@user.get('/login')
async def get_login_page():
    return FileResponse(os.path.join(frontend_path, "login.html"))

@user.post('/login')
async def login_action(form_data: OAuth2PasswordRequestForm = Depends()):
    user_id = db_login(form_data.username, form_data.password)
    if not user_id:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    new_ticket = str(uuid.uuid4())
    save_ticket(user_id, new_ticket)

    response = RedirectResponse(url="/user/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_ticket", value=new_ticket, httponly=True, path="/")
    return response

# --- PROTECTED PROFILE ---
@user.get('/')
async def get_user_profile(request: Request):
    ticket = request.cookies.get("session_ticket")
    if not is_ticket_in_db(ticket):
        return RedirectResponse(url="/user/login")

    return FileResponse(os.path.join(frontend_path, "user.html"))

@user.get('/logout')
async def logout(request: Request):
    ticket = request.cookies.get("session_ticket")
    if ticket:
        delete_ticket_from_db(ticket) 
    response = RedirectResponse(url="/user/login")
    response.delete_cookie("session_ticket")
    return response
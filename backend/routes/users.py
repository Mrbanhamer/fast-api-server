from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, Response
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

user = APIRouter(tags=["Users"])

# This ensures we find the frontend folder regardless of where you start the app
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
current_dir = os.path.dirname(os.path.abspath(__file__))      # /backend/routes
project_root = os.path.dirname(os.path.dirname(current_dir)) # /fast-api-server
frontend_path = os.path.join(project_root, "frontend", "src", "frontend")

@user.get('/me')
async def get_my_info(request: Request):
    ticket = request.cookies.get("session_ticket")
    
    # Use the NEW function that returns data, not just True/False
    user_data = is_ticket_in_db(ticket) 
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid session or user not found")
        
    return user_data # This now safely returns the dict: {"name": "...", "email": "..."}

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
    # 1. Verify the user (This checks the email/password in the DB)
    user_id = db_login(form_data.username, form_data.password)
    
    if not user_id:
        # If password is wrong, we stop here.
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # 2. CREATE THE TICKET (The part you mentioned!)
    # We generate a unique ID and link it to this specific user_id
    new_ticket = str(uuid.uuid4())
    
    # 3. SAVE THE TICKET (This puts it in your 'tickets' table)
    save_ticket(user_id, new_ticket)

    # 4. SEND THE TICKET TO THE BROWSER
    # We use a cookie so the browser holds onto it for us
    response = Response(content='{"message": "success"}', media_type="application/json")
    response.set_cookie(
        key="session_ticket", 
        value=new_ticket, 
        httponly=True, 
        path="/", 
        samesite="lax"
    )
    
    return response

# --- PROTECTED PROFILE ---
@user.get('/')
async def get_user_profile(request: Request):
    ticket = request.cookies.get("session_ticket")
    
    # These will show up in your terminal (VS Code/Git Bash)
    print(f"--- COOKIE CHECK ---")
    print(f"Browser sent ticket: {ticket}")
    
    if not is_ticket_in_db(ticket):
        print("Result: Ticket invalid or missing. Redirecting to login.")
        return RedirectResponse(url="/user/login")

    print("Result: Ticket valid! Sending user.html")
    return FileResponse(os.path.join(frontend_path, "user.html"))

@user.get('/logout')
async def logout(request: Request):
    ticket = request.cookies.get("session_ticket")
    
    # 1. Delete from Database so the ticket is "killed"
    if ticket:
        delete_ticket_from_db(ticket) 
    
    # 2. Prepare the redirect back to login
    response = RedirectResponse(url="/user/login", status_code=303)
    
    # 3. Tell the browser to delete the cookie
    response.delete_cookie("session_ticket", path="/") 
    
    return response

@user.get('/profile')
async def catch_profile_redirect():
    # If the frontend tries to go to /profile, send it to /
    return RedirectResponse(url="/user/")
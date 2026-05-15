from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
import uuid

# --- DATABASE IMPORTS ---
from database.sql_connector import (
    log_new_user, 
    is_ticket_in_db, 
    save_ticket, 
    get_user_id_from_email, 
    delete_ticket_from_db,
    login as db_login
)
from schemas.user_auth import UserSignup

user = APIRouter(tags=["Users"])

@user.get('/me')
async def get_my_info(request: Request):
    ticket = request.cookies.get("session_ticket")
    
    # Use the NEW function that returns data, not just True/False
    user_data = is_ticket_in_db(ticket) 
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid session or user not found")
        
    return user_data # This now safely returns the dict: {"name": "...", "email": "..."}

# --- SIGN-UP ---
@user.post('/signup')
async def signup_action(data: UserSignup = Depends(UserSignup.as_form)):
    success = log_new_user(data.name, data.last_name, data.email, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Signup Failed")

    user_id = get_user_id_from_email(data.email)
    new_ticket = str(uuid.uuid4())
    save_ticket(user_id, new_ticket)

    response = Response(content='{"message": "signup successful"}', media_type="application/json")
    response.set_cookie(key="session_ticket", value=new_ticket, httponly=True, path="/", samesite="lax")
    return response

# --- LOGIN ---
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

@user.get('/logout')
async def logout(request: Request):
    ticket = request.cookies.get("session_ticket")
    if ticket:
        delete_ticket_from_db(ticket)
    response = Response(content='{"message": "logged out"}', media_type="application/json")
    response.delete_cookie("session_ticket", path="/")
    return response
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from database.sql_connector import log_new_user

# Import your helper function
from database.sql_connector import login as db_login

user = APIRouter(prefix="/user", tags=["Users"])

# --- 1. THE SIGN-UP PAGE (GET) ---
@user.get('/signup', response_class=HTMLResponse)
async def get_signup_page(request: Request):
    try:
        with open('front_end/user_signup.html', 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Signup File Not Found</h1>", status_code=404)

# --- 2. THE SIGN-UP ACTION (POST) ---
@user.post('/signup')
async def signup_action(
    name: str = Form(...), 
    last_name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...)
):
    # 1. Call your database function
    success = log_new_user(name, last_name, email, password)
    
    if not success:
        # You could redirect back to signup with an error message here
        return HTMLResponse(content="<h1>Signup Failed. Try a different email.</h1>", status_code=400)

    # 2. SUCCESS: Redirect to login page so they can sign in for the first time
    # Or redirect to /user/ and set a cookie if you want to log them in immediately
    return RedirectResponse(url="/user/login", status_code=status.HTTP_303_SEE_OTHER)

# --- 1. THE LOGIN PAGE (GET) ---
@user.get('/login', response_class=HTMLResponse)
async def get_login_page(request: Request):
    try:
        with open('src/front_end/user_login.html', 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Login File Not Found</h1>", status_code=404)

# --- 2. THE LOGIN ACTION (POST) ---
@user.post('/login')
async def login_action(form_data: OAuth2PasswordRequestForm = Depends()):
    # Use your DB function: form_data.username is the email field
    user_data = db_login(form_data.username, form_data.password)
    
    if not user_data:
        # If login fails, stay on login page or show error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # SUCCESS: Create redirect to the profile
    response = RedirectResponse(url="/user/", status_code=status.HTTP_303_SEE_OTHER)
    
    # Give them the "Ticket" (Cookie)
    response.set_cookie(key="session_ticket", value=user_data["email"], httponly=True)
    return response

# --- 3. THE PROTECTED USER PAGE (GET) ---
@user.get('/', response_class=HTMLResponse)
async def get_user_profile(request: Request):
    # CHECK THE TICKET: Is the cookie there?
    ticket = request.cookies.get("session_ticket")
    
    if not ticket:
        # No ticket? Send them to login
        return RedirectResponse(url="/user/login")

    # Ticket exists! Serve the profile page
    try:
        with open('src/front_end/user.html', 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Profile File Not Found</h1>", status_code=404)

# --- 4. THE LOGOUT (BONUS) ---
@user.get('/logout')
async def logout():
    response = RedirectResponse(url="/user/login")
    # Delete the ticket
    response.delete_cookie("session_ticket")
    return response
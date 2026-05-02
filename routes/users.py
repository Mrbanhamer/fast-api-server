from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
import uuid

from database.sql_connector import log_new_user, is_ticket_in_db, save_ticket, get_user_id_from_email

# Import your helper function
from database.sql_connector import login as db_login

user = APIRouter(prefix="/user", tags=["Users"])


# --- 1. THE SIGN-UP PAGE (GET) ---
@user.get('/signup', response_class=HTMLResponse)
async def get_signup_page(request: Request):
    try:
        with open('src/front_end/signup.html', 'r', encoding='utf-8') as f:
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
    # 1. Create the user
    success = log_new_user(name, last_name, email, password)
    
    if not success:
        return HTMLResponse(content="<h1>Signup Failed</h1>", status_code=400)

    # 2. To log them in, we need their new ID. 
    # Let's assume you've added a helper to get ID by email
    user_id = get_user_id_from_email(email) 

    # 3. Create a session ticket just like in your login route
    new_ticket = str(uuid.uuid4())
    save_ticket(user_id, new_ticket)

    # 4. Redirect to the profile ('/user/') instead of login
    response = RedirectResponse(url="/user/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_ticket", value=new_ticket, httponly=True)
    
    return response

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
    # 1. Verify user exists and password is correct
    # This should return the user's ID from the database
    user_id = db_login(form_data.username, form_data.password)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # 2. GENERATE a unique session ticket
    new_ticket = str(uuid.uuid4())
    
    # 3. SAVE that ticket to the 'tickets' table in SQL
    # This links the ticket string to the user_id
    save_ticket(user_id, new_ticket)

    # 4. SUCCESS: Redirect to the profile and hand the browser the ticket
    response = RedirectResponse(url="/user/", status_code=status.HTTP_303_SEE_OTHER)
    
    # We set the cookie to the random UUID, not the email (much more secure!)
    response.set_cookie(
        key="session_ticket", 
        value=new_ticket, 
        httponly=True,
        path="/" # Makes sure the cookie works on all routes
    )
    return response

# --- 3. THE PROTECTED USER PAGE (GET) ---
@user.get('/', response_class=HTMLResponse)
async def get_user_profile(request: Request):
    # CHECK THE TICKET: Is the cookie there?
    ticket = request.cookies.get("session_ticket")
    
# 2. If it's missing OR if it's not in your database, kick them out
    # (Replace 'is_ticket_in_db' with your actual database lookup function)
    if not is_ticket_in_db(ticket):
        # We use '/index' because that's where your login page is
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
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, status, requests
from fastapi.security import OAuth2PasswordRequestForm

# Use APIRouter instead of FastAPI
user = APIRouter(prefix="/user", tags=["Users"])

@user.get('/', response_class=HTMLResponse)
async def get_user_page(request: Request):
    return HTMLResponse()
    return "<h1>User Profile</h1>"

@user.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Check if user exists in your "database"
    # (This is just a placeholder example)
    user_dict = fake_users_db.get(form_data.username)
    
    # 2. IF statement for the "Failed" case
    if not user_dict or form_data.password != user_dict["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. IF successful, return the Token
    return {"access_token": form_data.username, "token_type": "bearer"}
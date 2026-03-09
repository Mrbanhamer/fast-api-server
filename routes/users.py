from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# Use APIRouter instead of FastAPI
router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/", response_class=HTMLResponse)
async def get_user_page(request: Request):
    return "<h1>User Profile</h1>"
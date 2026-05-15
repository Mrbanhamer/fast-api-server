from pydantic import BaseModel
from typing import Optional

class TaskSchema(BaseModel):
    id: Optional[int] = None 
    title: str
    description: Optional[str] = None
    completed: bool = False

# Add these so main.py doesn't crash!
class User(BaseModel):
    username: str
    email: Optional[str] = None

class UserWithPassword(BaseModel):
    username: str
    password: str
    action: Optional[str] = None
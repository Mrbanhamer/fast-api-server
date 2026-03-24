from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    email: EmailStr = Field(...)
    name: str = Field(...)
    last_name: str = Field(...)
    age: Optional[int] = Field(None)
    action: Optional[str] = None  # Add this!

class UserWithPassword(User):
    # This inherits all fields from User and adds password
    password: str = Field(..., min_length=8)
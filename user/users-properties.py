from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    # We define fields as class variables
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., min_length=2, max_length=50, description="User's name")
    last_name: str = Field(..., min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")

class UserWithPassword(User):
    # This inherits all fields from User and adds password
    password: str = Field(..., min_length=8)

    def password(self):
        
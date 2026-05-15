from pydantic import BaseModel, EmailStr
from fastapi import Form

class UserSignup(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str

    # This "as_form" classmethod is a common trick to allow 
    # Pydantic to work with HTML Form data
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
    ):
        return cls(name=name, last_name=last_name, email=email, password=password)
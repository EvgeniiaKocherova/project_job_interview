from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    # Позже добавим сюда refresh_token
# В schemas.py
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
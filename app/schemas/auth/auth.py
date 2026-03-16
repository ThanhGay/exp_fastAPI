from pydantic import BaseModel, EmailStr
from enum import Enum

class AuthLogin(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    username: str
    email: str
    access_token: str
    refesh_token: str

class AuthStatus(int, Enum):
    IDLE=0
    CONNECT=1
    DISCONNECT=2
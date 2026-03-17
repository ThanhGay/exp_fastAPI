from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
import re


class AuthStatus(int, Enum):
    IDLE = 0
    CONNECT = 1
    DISCONNECT = 2


class AuthLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    username: str
    email: str
    fullname: str
    access_token: str
    refesh_token: str


class ChangePassword(BaseModel):
    password: str

    @field_validator("password")
    def validate_password(cls, v):

        regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$"

        if not re.match(regex, v):
            raise ValueError(
                "Password must contain uppercase, number, special character and be at least 8 characters"
            )

        return v

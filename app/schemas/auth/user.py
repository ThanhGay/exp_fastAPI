import re
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from app.schemas.auth.auth import AuthStatus


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=255)
    email: EmailStr
    status: AuthStatus = AuthStatus.IDLE.value

    @field_validator("username", "email", mode="before")
    @classmethod
    def trim_str(cls, v):
        return v.strip() if isinstance(v, str) else v


class UserCreate(BaseModel):
    username: str = Field(..., min_length=5, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str = Field(...)
    last_name: str = Field(...)

    @field_validator("password")
    def validate_password(cls, v):

        regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$"

        if not re.match(regex, v):
            raise ValueError(
                "Password must contain uppercase, number, special character and be at least 8 characters"
            )

        return v

    @field_validator("username", "email", "first_name", "last_name", mode="before")
    @classmethod
    def trim_str(cls, v):
        return v.strip() if isinstance(v, str) else v


class UserUpdate(BaseModel):
    username: str = Field(..., min_length=5, max_length=255)
    email: EmailStr
    first_name: str = Field(...)
    last_name: str = Field(...)

    @field_validator("username", "email", "first_name", "last_name", mode="before")
    @classmethod
    def trim_str(cls, v):
        return v.strip() if isinstance(v, str) else v


class UserView(BaseModel):
    """Response không có password."""

    id: int
    username: str
    email: str
    fullname: str

    model_config = ConfigDict(from_attributes=True)


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

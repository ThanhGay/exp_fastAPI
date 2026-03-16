import re
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from app.schemas.auth.auth import AuthStatus

class UserBase(BaseModel):
    """Chỉ field chung, không có password."""
    username: str = Field(..., min_length=5, max_length=255)
    email: EmailStr
    status: AuthStatus = AuthStatus.IDLE.value


class UserCreate(BaseModel):
    """Input đăng ký / tạo user."""
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


class UserUpdate(BaseModel):
    """Input cập nhật (tất cả optional)."""
    username: str | None = Field(None, min_length=5, max_length=255)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)


class UserView(BaseModel):
    """Response không có password."""
    id: int
    username: str
    email: str
    fullname: str

    model_config = ConfigDict(from_attributes=True)
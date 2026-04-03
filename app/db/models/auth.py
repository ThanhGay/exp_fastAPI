from app.db.models.base import BaseAuth
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean


# User N - N Role
class UserAssignment(BaseAuth):
    user_id = Column(Integer)
    role_id = Column(Integer)


# Role N - N Permission
class PermissionAssignment(BaseAuth):
    role_id = Column(Integer)
    permission_id = Column(Integer)


class User(BaseAuth):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    status = Column(Integer)

    roles = relationship("Role", secondary=UserRole, back_populates="users")

    @property
    def fullname(self) -> str:
        first = self.first_name or ""
        last = self.last_name or ""
        full = (first + " " + last).strip()
        return full or self.username


class Role(BaseAuth):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)


class Permission(BaseAuth):
    id = Column(Integer, primary_key=True)
    code = Column(String(150), unique=True, nullable=False)
    description = Column(Text)

    roles = relationship("Role", secondary=RolePermisison, back_populates="permissions")


class TokenManagement(BaseAuth):
    jti = Column(String(36), nullable=False, index=True)
    user_id = Column(Integer, index=True)
    expire_at = Column(DateTime)

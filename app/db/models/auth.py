from app.db.models.base import BaseAuth
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Table,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship

# User N - N Role
UserRole = Table(
    "UserRole",
    BaseAuth.metadata,
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("role_id", ForeignKey("Role.id"), primary_key=True),
)


# Role N - N Permission
RolePermisison = Table(
    "RolePermission",
    BaseAuth.metadata,
    Column("role_id", ForeignKey("Role.id"), primary_key=True),
    Column("permission_id", ForeignKey("Permission.id"), primary_key=True),
)


class User(BaseAuth):
    __tablename__ = "User"

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
    __tablename__ = "Role"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    users = relationship("User", secondary=UserRole, back_populates="roles")
    permissions = relationship(
        "Permission", secondary=RolePermisison, back_populates="roles"
    )


class Permission(BaseAuth):
    __tablename__ = "Permission"
    id = Column(Integer, primary_key=True)
    code = Column(String(150), unique=True, nullable=False)
    description = Column(Text)

    roles = relationship("Role", secondary=RolePermisison, back_populates="permissions")


class TokenManagement(BaseAuth):
    __tablename__ = "RefreshToken"

    jti = Column(String(36), nullable=False, index=True, primary_key=True)
    user_id = Column(Integer, index=True)
    expire_at = Column(DateTime)

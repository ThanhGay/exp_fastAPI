from sqlalchemy.orm import Session
from app.db.models.auth import (
    Role,
    Permission,
    UserAssignment,
    PermissionAssignment,
)


def create_role(db: Session, name: str) -> Role:
    role = Role(name=name)
    db.add(role)
    db.flush()
    return role


def create_permission(db: Session, code: str, description: str | None) -> Permission:
    permission = Permission(code=code, description=description)
    db.add(permission)
    db.flush()
    return permission


def get_role_by_id(db: Session, role_id: int) -> Role | None:
    return db.query(Role).filter(Role.id == role_id).first()


def get_permission_by_id(db: Session, perm_id: int) -> Permission | None:
    return db.query(Permission).filter(Permission.id == perm_id).first()


def list_roles(db: Session) -> list[Role]:
    return db.query(Role).all()


def list_permissions(db: Session) -> list[Permission]:
    return db.query(Permission).all()


def add_role_to_user(db: Session, user_id: int, role__id: int) -> UserAssignment:
    new_user_role = UserAssignment(user_id=user_id, role__id=role__id)
    db.add(new_user_role)
    db.flush()
    return new_user_role


def add_permission_to_role(
    db: Session, role_id: int, permission_id: int
) -> PermissionAssignment:
    new_role_per = PermissionAssignment(role_id=role_id, permission_id=permission_id)
    db.add(new_role_per)
    db.flush
    return new_role_per

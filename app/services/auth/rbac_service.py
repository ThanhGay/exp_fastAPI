from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.repositories.auth import role_repository as repo
from app.schemas.auth.rbac import (
    RoleCreate,
    PermissionCreate,
    AssignRoleToUser,
    AssignPermToRole,
)


def create_role(db: Session, data: RoleCreate):
    return repo.create_role(db, data.name)


def create_permission(db: Session, data: PermissionCreate):
    return repo.create_permission(db, data.code, data.description)


def assign_role_to_user(db: Session, data: AssignRoleToUser):
    user = repo.assign_role_to_user(db, data.user_id, data.role_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Role not found")
    return user


def assign_perm_to_role(db: Session, data: AssignPermToRole):
    role = repo.assign_permission_to_role(db, data.role_id, data.permission_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role or Permission not found")
    return role


def list_roles(db: Session):
    return repo.list_roles(db)


def list_permissions(db: Session):
    return repo.list_permissions(db)

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
    try:
        role = repo.create_role(db, data.name)
        db.commit()
        return role
    except Exception:
        db.rollback()
        raise


def create_permission(db: Session, data: PermissionCreate):
    try:
        perm = repo.create_permission(db, data.code, data.description)
        db.commit()
        return perm
    except Exception:
        db.rollback()
        raise


def assign_role_to_user(db: Session, data: AssignRoleToUser):
    try:
        user = repo.assign_role_to_user(db, data.user_id, data.role_id)
        if user:
            db.commit()
    except Exception:
        db.rollback()
        raise
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Role not found")
    return user


def assign_perm_to_role(db: Session, data: AssignPermToRole):
    try:
        role = repo.assign_permission_to_role(db, data.role_id, data.permission_id)
        if role:
            db.commit()
    except Exception:
        db.rollback()
        raise
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role or Permission not found")
    return role


def list_roles(db: Session):
    return repo.list_roles(db)


def list_permissions(db: Session):
    return repo.list_permissions(db)

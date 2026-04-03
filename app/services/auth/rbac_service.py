from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.repositories.auth import role_repository as repo
from app.schemas.auth.rbac import (
    RoleCreate,
    RoleView,
    PermissionCreate,
    PermissionView,
    AssignRoleToUser,
    AssignPermissionToRole,
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
        user = repo.add_role_to_user(db=db, user_id=data.user_id, role__id=data.role_id)
        if user:
            db.commit()
    except Exception:
        db.rollback()
        raise
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User or Role not found"
        )
    return user


def assign_permission_to_role(db: Session, data: AssignPermissionToRole):
    try:
        # Validate role
        role = repo.get_role_by_id(db, data.role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            )

        # Validate permissions
        permissions = repo.get_permissions_by_ids(db, data.permission_ids)

        if len(permissions) != len(data.permission_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more permissions not found",
            )

        # Assign permissions (bulk)
        role = repo.add_permissions_to_role(
            db=db, role_id=data.role_id, permission_ids=data.permission_ids
        )

        db.commit()
        return role
    except Exception:
        db.rollback()
        raise


def list_roles(db: Session):
    data = repo.list_roles(db)

    if not data:
        return []

    result: list[RoleView] = []
    for r in data:
        result.append(RoleView(id=r.id, name=r.name))

    return result


def list_permissions(db: Session) -> list[PermissionView]:
    return repo.list_permissions(db)

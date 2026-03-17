from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_permission, get_current_user
from app.schemas.auth.rbac import (
    RoleCreate, PermissionCreate,
    RoleView, PermissionView,
    AssignRoleToUser, AssignPermToRole,
)
from app.services.auth import rbac_service
from app.constants.permissions import PERMISSIONS_SEED

router = APIRouter(prefix="/rbac", tags=["rbac"])

@router.post("/roles", response_model=RoleView,
             dependencies=[Depends(require_permission("rbac.role.create"))])
def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
):
    return rbac_service.create_role(db, data)

@router.get("/roles", response_model=list[RoleView],
            dependencies=[Depends(require_permission("rbac.role.read"))])
def list_roles(
    db: Session = Depends(get_db),
):
    return rbac_service.list_roles(db)

@router.post("/permissions", response_model=PermissionView,
             dependencies=[Depends(require_permission("rbac.permission.create"))])
def create_permission(
    data: PermissionCreate,
    db: Session = Depends(get_db),
):
    return rbac_service.create_permission(db, data)

@router.get("/permissions", response_model=list[PermissionView],
            dependencies=[Depends(require_permission("rbac.permission.read"))])
def list_permissions(
    db: Session = Depends(get_db),
):
    return rbac_service.list_permissions(db)

@router.post("/assign-role",
             dependencies=[Depends(require_permission("rbac.user.assign_role"))])
def assign_role_to_user(
    data: AssignRoleToUser,
    db: Session = Depends(get_db),
):
    return rbac_service.assign_role_to_user(db, data)

@router.post("/assign-permission",
             dependencies=[Depends(require_permission("rbac.role.assign_perm"))])
def assign_perm_to_role(
    data: AssignPermToRole,
    db: Session = Depends(get_db),
):
    return rbac_service.assign_perm_to_role(db, data)
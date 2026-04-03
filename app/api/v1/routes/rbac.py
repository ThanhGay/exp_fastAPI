from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_permission, get_current_user
from app.schemas.auth.rbac import (
    RoleCreate,
    PermissionCreate,
    RoleView,
    PermissionView,
    AssignRoleToUser,
    AssignPermissionToRole,
)
from app.services.auth import rbac_service
from app.services import permission_seed_service
from app.constants.permission_key import PermissionKey
from app.utils.response import ok, ApiResponse


router = APIRouter(prefix="/rbac", tags=["rbac"])


@router.post(
    "/roles",
    response_model=ApiResponse[RoleView],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("rbac.role.create"))],
)
def create_role(req: RoleCreate, db: Session = Depends(get_db)):
    created = rbac_service.create_role(db, req)
    return ok(data=created, message="Role created")


@router.get(
    "/roles",
    response_model=ApiResponse[list[RoleView]],
    # dependencies=[Depends(require_permission("rbac.role.read"))],
)
def list_roles(
    db: Session = Depends(get_db),
):
    res = rbac_service.list_roles(db)
    print(PermissionKey.ADMIN_ROLE_CREATE.value.split("."))
    return ok(data=res)


# @router.post(
#     "/permissions",
#     response_model=PermissionView,
#     dependencies=[Depends(require_permission("rbac.permission.create"))],
# )
# def create_permission(
#     data: PermissionCreate,
#     db: Session = Depends(get_db),
# ):
#     return rbac_service.create_permission(db, data)

@router.post("/permissions/fetch", response_model=ApiResponse)
def fetch_permissions(db: Session = Depends(get_db)):
    data = permission_seed_service.sync_permissions(db=db)
    return ok(message="Fetch permission success !!!")

@router.get(
    "/permissions",
    response_model=ApiResponse[list[PermissionView]],
    # dependencies=[Depends(require_permission("rbac.permission.read"))],
)
def list_permissions(
    db: Session = Depends(get_db),
):
    data = rbac_service.list_permissions(db)
    return ok(data=data)


@router.post(
    "/assign-role", dependencies=[Depends(require_permission("rbac.user.assign_role"))]
)
def assign_role_to_user(
    req: AssignRoleToUser,
    db: Session = Depends(get_db),
):
    data = rbac_service.assign_role_to_user(db, req)
    return ok(data=data)


@router.post(
    "/assign-permission",
    dependencies=[Depends(require_permission("rbac.role.assign_permission"))],
)
def assign_permission_to_role(
    req: AssignPermissionToRole,
    db: Session = Depends(get_db),
):
    data = rbac_service.assign_permission_to_role(db, req)
    return ok(data=data)

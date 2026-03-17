from app.schemas.auth.rbac import PermissionCreate

PERMISSIONS_SEED: list[PermissionCreate] = [
    {"code": "rbac.role.create", "description": "Tao role moi"},
    {"code": "rbac.role.read", "description": "Danh sach role"},
    {"code": "rbac.permission.create", "description": "Tao moi permission"},
    {"code": "rbac.permission.read", "description": "Danh sach permissions"},
    {"code": "rbac.user.assign_role", "description": "Gan role cho user"},
    {"code": "rbac.role.assign_perm", "description": "Gan permission cho role"},
    
    {"code": "user.read", "description": "Danh sach user"},
    {"code": "user.create", "description": "Them moi user"},
]

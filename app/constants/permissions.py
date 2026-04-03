from app.schemas.auth.rbac import PermissionCreate

PERMISSIONS_SEED: list[PermissionCreate] = [
    {"code": "rbac.role.create", "description": "Tao role moi"},
    {"code": "rbac.role.list", "description": "Danh sach role"},
    {"code": "rbac.role.update", "description": "Cap nhat role"},
    {"code": "rbac.role.delete", "description": "Xoa role"},
    {"code": "rbac.role.active", "description": "Active role"},
    {"code": "rbac.role.deactive", "description": "Deactive role"},
    {"code": "rbac.role.assign_permission", "description": "Gan permission cho role"},

    {"code": "rbac.permission.create", "description": "Tao moi permission"},
    {"code": "rbac.permission.read", "description": "Danh sach permissions"},
    
    {"code": "rbac.user.assign_role", "description": "Gan role cho user"},
    
    {"code": "user.read", "description": "Danh sach user"},
    {"code": "user.create", "description": "Them moi user"},
]

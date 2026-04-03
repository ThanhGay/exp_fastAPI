from app.schemas.auth.rbac import PermissionCreate
from .permission_key import PermissionKey as PK

PERMISSIONS_SEED: list[PermissionCreate] = [
    {"code": PK.ADMIN_ROLE_CREATE.value, "description": "Admin tao role moi"},
    {"code": PK.ADMIN_ROLE_ASSIGN_PERMISSION.value, "description": "Admin gan permission cho role"},
    {"code": PK.ADMIN_ROLE_ASSIGN_USER.value, "description": "Admin gan role cho user"},

    {"code": PK.ROLE_CREATE.value, "description": "Tao role moi"},
    {"code": PK.ROLE_LIST.value, "description": "Danh sach role"},
    {"code": PK.ROLE_UPDATE.value, "description": "Cap nhat role"},
    {"code": PK.ROLE_DELETE.value, "description": "Xoa role"},
    {"code": PK.ROLE_ACTIVE.value, "description": "Active role"},
    {"code": PK.ROLE_DEACTIVE.value, "description": "Deactive role"},
    {"code": PK.ROLE_ASSIGN_PERMISSION.value, "description": "Gan permission cho role"},
    {"code": PK.ROLE_ASSIGN_USER.value, "description": "Gan role cho user"},

    {"code": PK.PERMISSION_CREATE.value, "description": "Tao moi permission"},
    {"code": PK.PERMISSION_READ.value, "description": "Danh sach permissions"},
    {"code": PK.PERMISSION_UPDATE.value, "description": "Cap nhat mo ta permissions"},
    {"code": PK.PERMISSION_DELETE.value, "description": "Xoa permission"},
    
    {"code": PK.USER_LIST.value, "description": "Danh sach user"},
    {"code": PK.USER_CREATE.value, "description": "Them moi user"},
    {"code": PK.USER_PROFILE.value, "description": "Ho so user"},
    {"code": PK.USER_UPDATE.value, "description": "Thay doi ho so"},

    {"code": PK.PERSONAL_USER_CHANGE_PWD.value, "description": "Nguoi dung tu doi mat khau"},
    {"code": PK.PERSONAL_USER_UPDATE.value, "description": "Thay doi ho so"},
]

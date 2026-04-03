from enum import Enum

class PermissionKey (str, Enum):
    ADMIN_ROLE_CREATE = "admin.role.create"
    ADMIN_ROLE_ASSIGN_PERMISSION = "admin.role.assign_permission"
    ADMIN_ROLE_ASSIGN_USER = "admin.role.assign_user"

    ROLE_CREATE = "role.create"
    ROLE_LIST = "role.list"
    ROLE_UPDATE = "role.update"
    ROLE_DELETE = "role.delete"
    ROLE_ACTIVE = "role.active"
    ROLE_DEACTIVE = "role.deactive"
    ROLE_ASSIGN_PERMISSION = "role.assign_permission"
    ROLE_ASSIGN_USER = "role.assign_user"

    PERMISSION_CREATE = "permission.create"
    PERMISSION_READ = "permission.read"
    PERMISSION_UPDATE = "permission.update"
    PERMISSION_DELETE = "permission.delete"

    USER_LIST = "user.list"
    USER_CREATE = "user.create"
    USER_PROFILE = "user.profile"
    USER_UPDATE = "user.update"

    PERSONAL_USER_CHANGE_PWD = "personal.user.change_password"
    PERSONAL_USER_UPDATE = "personal.user.update"

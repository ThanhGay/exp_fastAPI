from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str


class PermissionCreate(BaseModel):
    code: str
    description: str | None = None


class RoleView(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PermissionView(BaseModel):
    id: int
    code: str
    description: str | None = None

    class Config:
        from_attributes = True


class AssignRoleToUser(BaseModel):
    user_id: int
    role_id: int


class AssignPermToRole(BaseModel):
    role_id: int
    permission_id: int

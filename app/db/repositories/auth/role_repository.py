from sqlalchemy.orm import Session
from app.db.models.auth import Role, Permission, User


def create_role(db: Session, name: str) -> Role:
    role = Role(name=name)
    db.add(role)
    db.flush()
    return role


def create_permission(db: Session, code: str, description: str | None) -> Permission:
    perm = Permission(code=code, description=description)
    db.add(perm)
    db.flush()
    return perm


def get_role(db: Session, role_id: int) -> Role | None:
    return db.query(Role).filter(Role.id == role_id).first()


def get_permission(db: Session, perm_id: int) -> Permission | None:
    return db.query(Permission).filter(Permission.id == perm_id).first()


def assign_role_to_user(db: Session, user_id: int, role_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not user or not role:
        return None
    if role not in user.roles:
        user.roles.append(role)
        db.flush()
    return user


def assign_permission_to_role(db: Session, role_id: int, perm_id: int) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not role or not perm:
        return None
    if perm not in role.permissions:
        role.permissions.append(perm)
        db.flush()
    return role


def list_roles(db: Session) -> list[Role]:
    return db.query(Role).all()


def list_permissions(db: Session) -> list[Permission]:
    return db.query(Permission).all()

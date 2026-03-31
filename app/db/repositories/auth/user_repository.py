from app.schemas.auth.user import UserCreate
from app.schemas.auth.auth import AuthStatus
from app.db.models.auth import User
from app.db.repositories.base import apply_limit_offset
from sqlalchemy.orm import Session
from sqlalchemy import exists, select, or_


def get_multi(
    db: Session,
    *,
    limit: int | None = None,
    offset: int | None = None,
    keyword: str | None = None,
):
    res = db.query(User)
    if keyword:
        pattern = f"%{keyword}%"
        res = res.filter(
            or_(
                User.username.ilike(pattern),
                User.email.ilike(pattern),
                User.first_name.ilike(pattern),
                User.last_name.ilike(pattern),
            )
        )
    res = apply_limit_offset(res, limit=limit, offset=offset)
    return res.all()


def get_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def create(db: Session, user_in: UserCreate) -> User:
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        status=AuthStatus.IDLE.value,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )

    db.add(new_user)
    db.flush()
    return new_user


def exists_email(db: Session, email_check: str) -> bool:
    stmt = db.query(exists().where(User.email == email_check)).scalar()
    return stmt


def get_by_email(db: Session, email: str) -> User | None:

    user = db.query(User).filter(User.email == email).first()
    return user


def update_status(db: Session, new_status: int, user: User) -> User:
    user.status = new_status

    db.flush()

    return user


def update_password(db: Session, id: int, new_pwd: str) -> bool:
    user = get_by_id(db=db, user_id=id)
    if not user:
        return False

    user.password = new_pwd

    db.flush()

    return True

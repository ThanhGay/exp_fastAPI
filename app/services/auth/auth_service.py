import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import create_access_token
from app.db.repositories.auth import user_repository as repo
from app.schemas.auth.auth import AuthLogin, AuthResponse, AuthStatus, ResetPassword
from app.utils.password import (
    encode_password,
    verify_password,
    generate_secure_password,
)


def login(db: Session, req: AuthLogin) -> AuthResponse:
    user = repo.get_by_email(db, req.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This email is not registered",
        )

    if not verify_password(req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )

    repo.update_status(db=db, new_stt=AuthStatus.CONNECT.value, user=user)

    access_token = create_access_token(
        subject=user.id,
        extra={"username": user.username},
    )

    res = AuthResponse(
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        access_token=access_token,
        refesh_token="...",
    )

    return res


def logout(db: Session, user_id: int) -> bool:
    user = repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    repo.update_status(db=db, new_stt=AuthStatus.CONNECT.value, user=user)

    return True


def change_password(
    db: Session, user_id: int, current_password: str, new_password: str
):
    """Nguoi dung tu thay doi mat khau"""

    user = repo.get_by_id(db=db, user_id=user_id)

    if not verify_password(pwd=current_password, hashed_pwd=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your current password is incorrect",
        )

    new_hashed_pwd = encode_password(new_password)

    result = repo.update_password(db=db, id=user_id, new_pwd=new_hashed_pwd)

    return result


def reset_password(db: Session, email: str):
    user = repo.get_by_email(db=db, email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    new_pwd = generate_secure_password()

    print(f"New password of user {user.id} is '{new_pwd}'")

    new_hashed_pwd = encode_password(new_pwd)

    result = repo.update_password(db=db, id=user.id, new_pwd=new_hashed_pwd)

    return result

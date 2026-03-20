from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.repositories.auth import user_repository as repo
from app.db.repositories.auth import token_repository as token_repo
from app.schemas.auth.auth import (
    AuthLogin,
    AuthResponse,
    AuthStatus,
    ResetPassword,
    AuthRefreshResponse,
    AuthRefreshCreate,
)
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

    refresh_token, jti, expire = create_refresh_token(
        subject=user.id, extra={"username": user.username}
    )

    request = AuthRefreshCreate(jti=jti, user_id=user.id, expire=expire)
    token_repo.add_ref_token(db=db, req=request)

    result = AuthResponse(
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        access_token=access_token,
        refesh_token=refresh_token,
    )

    return result


def refresh_token(db: Session, token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token"
        )

    payload = decode_token(token=token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jti = payload["jti"]
    user_id = payload["sub"]

    # revoke old refresh token
    revoked = token_repo.revoke(jti=jti)

    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Refesh token not found"
        )

    # create new refresh_token
    new_refresh_token, new_jti, new_expire = create_refresh_token(subject=user_id)

    # save new refresh_token into database
    request = AuthRefreshCreate(jti=new_jti, user_id=user_id, expire=new_expire)
    token_repo.add_ref_token(db=db, req=request)

    # create new access_token
    new_access_token = create_access_token(subject=user_id)

    return AuthRefreshResponse(
        access_token=new_access_token, refresh_token=new_refresh_token
    )


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


def reset_password(db: Session, req: ResetPassword):
    user = repo.get_by_email(db=db, email=req.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    new_pwd = generate_secure_password()

    print(f"New password of user {user.id} is '{new_pwd}'")

    new_hashed_pwd = encode_password(new_pwd)

    result = repo.update_password(db=db, id=user.id, new_pwd=new_hashed_pwd)

    return result

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import create_access_token
from app.db.repositories.auth import user_repository as repo
from app.schemas.auth.auth import AuthLogin, AuthResponse, AuthStatus
from app.utils.password import encode_password, verify_password


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

    user.status = AuthStatus.CONNECT.value
    db.commit()
    db.refresh(user)

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


def logout(db: Session, user_id: int):
    user = repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.status = AuthStatus.DISCONNECT.value

    db.commit()
    db.refresh(user)

    return {"message": "Logged out success"}


def change_password(db: Session, user_id: int, new_password):
    new_hashed_pwd = encode_password(new_password)

    result = repo.update_password(db=db, id=user_id, new_pwd=new_hashed_pwd)

    if result:
        return {"message": "Your password changed success"}

    return {"message": "Your password changed failure"}

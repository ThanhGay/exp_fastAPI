import re
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.core.security import create_access_token
from app.repositories.auth import user_repository as repo
from app.schemas.auth.user import UserCreate
from app.schemas.auth.auth import AuthLogin, AuthResponse, AuthStatus
from app.utils.password import encode_password, verify_password

def get_all_users(db: Session):
    return repo.get_multi(db)

def create_user(db: Session, user_in: UserCreate):
    if repo.exists_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )    
    
    user_in.password = encode_password(user_in.password)
    
    print(f"Data create user: {user_in}")
    
    return repo.create(db, user_in)


def login(db: Session, req: AuthLogin) -> AuthResponse:
    user = repo.get_by_email(db, req.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This email is not registered",
        )
        
    if not verify_password(req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
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
        access_token=access_token,
        refesh_token="..."
    )

    return res

def logout(db:Session, user_id: int):     
    user = repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.status = AuthStatus.DISCONNECT.value

    db.commit()
    db.refresh(user)

    return { "message": "Logged out success" }

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.repositories.auth import user_repository as repo
from app.schemas.auth.user import UserCreate
from app.schemas.common.query_params import BaseQueryParams
from app.utils.password import encode_password


def get_all_users(db: Session, query: BaseQueryParams | None = None):
    params = query or BaseQueryParams()
    return repo.get_multi(
        db,
        limit=params.limit,
        offset=params.offset,
        keyword=params.keyword,
    )

def create_user(db: Session, user_in: UserCreate):
    if repo.exists_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )    
    
    user_in.password = encode_password(user_in.password)
    
    print(f"Data create user: {user_in}")
    
    return repo.create(db, user_in)

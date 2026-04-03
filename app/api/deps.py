from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_db
from app.core.security import decode_token
from app.db.models.auth import User
from app.db.repositories.auth import user_repository as repo
from app.schemas.common.query_params import BaseQueryParams

security = HTTPBearer(auto_error=False)


def get_query_params(
    page: int = Query(1, ge=1, description="Trang"),
    limit: int = Query(10, ge=1, le=100, description="Số bản ghi mỗi trang"),
    keyword: str | None = Query(
        None,
        max_length=200,
        description="Từ khóa tìm kiếm",
    ),
) -> BaseQueryParams:
    """Dependency trả về query params dùng cho các API get_all."""
    kw = keyword.strip() if keyword else None
    if kw == "":
        kw = None
    return BaseQueryParams(page=page, limit=limit, keyword=kw)


def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> int:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(payload["sub"])


"""
================= Use OAuth2 =================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") 

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

"""


def get_current_user(
    db: Session = Depends(get_db),
    user_id: int | None = Depends(get_current_user_id),
) -> User:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def require_permission(code: str):
    def dep(
        current_user: User = Depends(get_current_user),
    ):
        print("Updating...")    

    return dep

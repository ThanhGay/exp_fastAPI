from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_query_params
from app.schemas.auth.user import UserCreate, UserView
from app.schemas.common.query_params import BaseQueryParams
from app.services.auth import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserView)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(user_in=user, db=db)


@router.get("/", response_model=list[UserView])
def get_all_users_(
    db: Session = Depends(get_db),
    query: BaseQueryParams = Depends(get_query_params),
):
    return user_service.get_all_users(db=db, query=query)

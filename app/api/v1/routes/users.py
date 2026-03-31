from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_query_params
from app.schemas.auth.user import UserCreate, UserView
from app.schemas.common import BaseQueryParams, ApiResponse
from app.services.auth import user_service
from app.utils.response import ok

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=ApiResponse[UserView], status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    new_user = await user_service.create_user(user_in=user, db=db)
    return ok(data=new_user, message="New user has been created.")


@router.get("/", response_model=ApiResponse[list[UserView]])
async def get_all_users_(
    db: Session = Depends(get_db),
    query: BaseQueryParams = Depends(get_query_params),
):
    items = await user_service.get_all_users(db=db, query=query)
    return ok(data=items)

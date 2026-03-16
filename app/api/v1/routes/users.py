from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.schemas.auth.user import UserCreate, UserView
from app.schemas.auth.auth import AuthLogin, AuthResponse
from app.services.auth import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserView)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(user_in=user, db=db)

@router.get("/", response_model=list[UserView])
def get_all_users_(db: Session = Depends(get_db)):
    return user_service.get_all_users(db=db)

@router.post("/login", response_model=AuthResponse)
async def login(req: AuthLogin, db: Session = Depends(get_db)):
    return user_service.login(db, req)

@router.post("/logout")
async def logout(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return user_service.logout(db, user_id)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.schemas.auth.auth import AuthLogin, AuthResponse, ChangePassword
from app.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse)
async def login(req: AuthLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, req)


@router.post("/logout")
async def logout(
    user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    return auth_service.logout(db, user_id)


@router.post("/change-password")
async def change_password(
    req: ChangePassword,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    return auth_service.change_password(
        db=db, user_id=current_id, new_password=req.password
    )

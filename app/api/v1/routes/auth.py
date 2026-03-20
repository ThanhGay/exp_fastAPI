from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.schemas.auth.auth import AuthLogin, AuthResponse, ChangePassword, ResetPassword, AuthRefreshResponse
from app.services.auth import auth_service
from app.schemas.common import ApiResponse
from app.utils.response import ok

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=ApiResponse[AuthResponse])
async def login(req: AuthLogin, db: Session = Depends(get_db)):
    data = auth_service.login(db, req)

    Response.set_cookie(
        key="refresh_token",
        value=data.refesh_token,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age= 3 * 24 * 60 * 60       # 3 days
    )

    return ok(data=data, message="Login successful.")


@router.post("/logout")
async def logout( 
    user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    data = auth_service.logout(db, user_id)
    return ok(data=data, message="Logout successful.")


@router.post("/change-password")
async def change_password(
    req: ChangePassword,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    data = auth_service.change_password(
        db=db,
        user_id=current_id,
        current_password=req.current_pwd,
        new_password=req.new_pwd,
    )

    return ok(data=data, message="Your password is updated")


@router.post("/reset-password")
async def reset_password(req: ResetPassword, db: Session = Depends(get_db)):
    data = auth_service.reset_password(db=db, req=req)
    return ok(data=data, message="Your password is reset")


@router.post("/refresh")
async def refresh_token_route(request: Request, db: Session = Depends(get_db) ):
    token = request.cookies.get("refresh_token")

    data = auth_service.refresh_token(db=db, token=token)

    Response.set_cookie(
        key="refresh_token",
        value=data.refresh_token,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age= 3 * 24 * 60 * 60       # 3 days
    )

    return ok(data=data, message="OKE")

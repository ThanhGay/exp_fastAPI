from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.core.config import settings
from app.schemas.auth.auth import (
    AuthLogin,
    AuthResponse,
    ChangePassword,
    ResetPassword,
    AuthRefreshResponse,
)
from app.services.auth import auth_service
from app.schemas.common import ApiResponse
from app.utils.response import ok, err

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE_NAME = "refresh_token"


def set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # seconds
        path="/",
    )


@router.post("/login", response_model=ApiResponse[AuthResponse])
async def login(req: AuthLogin, response: Response, db: Session = Depends(get_db)):
    data = auth_service.login(db, req)

    set_refresh_cookie(response=response, refresh_token=data.refesh_token)

    return ok(data=data, message="Login successful.")


@router.post("/logout", response_model=ApiResponse[bool])
async def logout(
    request: Request,
    response: Response,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    data = auth_service.logout(db=db, user_id=user_id, refresh_token=refresh_token)
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )
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


@router.post("/refresh", response_model=ApiResponse[AuthRefreshResponse])
async def refresh_token_route(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    token = request.cookies.get(REFRESH_COOKIE_NAME)

    try:

        data = auth_service.refresh_token(db=db, token=token)
        
        set_refresh_cookie(response=response, refresh_token=data.refresh_token)
        
        return ok(data=data, message="OK")
    
    except HTTPException as exc:
        response.delete_cookie(
                key=REFRESH_COOKIE_NAME,
                httponly=True,
                secure=True,
                samesite="strict",
                path="/",
            )
        
        response.status_code = exc.status_code
        
        return err(message=exc.detail, code=exc.status_code)


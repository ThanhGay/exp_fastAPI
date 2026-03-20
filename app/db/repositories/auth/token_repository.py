from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.schemas.auth.auth import AuthRefreshCreate
from app.db.models.auth import TokenManagement as RefToken


def get_by_jti(db: Session, jti: str) -> RefToken:
    """
    Tim kiem refresh token xem da dc su dung trong db hay chua
    """

    return (
        db.query(RefToken)
        .filter(RefToken.jti == jti, RefToken.is_deleted != True)
        .first()
    )


def add_ref_token(db: Session, req: AuthRefreshCreate) -> RefToken:
    """
    Them refresh_token vao db
    """

    new_ref_token = RefToken(jti=req.jti, user_id=req.user_id, expire_at=req.expire)

    db.add(new_ref_token)
    db.commit()

    return req


def revoke(db: Session, jti: str) -> bool:
    """
    Thu hoi refresh_token
    """

    ref_token = get_by_jti(db=db, jti=jti)

    if not ref_token:
        return False

    ref_token.is_deleted = True
    ref_token.deleted_at = datetime.now(tz=timezone.utc)

    db.commit()
    db.refresh(ref_token)

    return True

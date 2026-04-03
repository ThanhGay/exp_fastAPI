from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.repositories.auth import user_repository as repo
from app.schemas.auth.user import UserCreate
from app.schemas.common.query_params import BaseQueryParams
from app.utils.password import encode_password
from app.schemas.common.email import EmailTemplateSchema
from app.queue.tasks import send_template_email


def get_all_users(db: Session, query: BaseQueryParams | None = None):
    params = query or BaseQueryParams()
    return repo.get_multi(
        db,
        limit=params.limit,
        offset=params.offset,
        keyword=params.keyword,
    )


async def create_user(db: Session, user_in: UserCreate):
    if repo.exists_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    raw_pwd = user_in.password
    user_in.password = encode_password(user_in.password)

    print(f"Data create user: {user_in}")

    try:
        user = repo.create(db, user_in)

        data = EmailTemplateSchema(
            subject="Chuc mung dang ky thanh cong",
            recipients=[user.email],
            template_name="email/register_success.html",
            context={
                "fullname": user.fullname,
                "username": user.username,
                "password": raw_pwd,
            },
        )

        # save user into database
        db.commit()

        # then call send email in queue
        send_template_email.delay(payload=data.model_dump())

        return user
    except Exception:
        db.rollback()
        raise

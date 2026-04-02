from app.queue.celery import celery_app as app
from app.services.core.notification.email_service import email_service
from app.schemas.common.email import EmailTemplateSchema


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task(
    name="queue.send_template_email",
    autoretry_for=(Exception,),  # auto retry cho mọi loại lỗi
    retry_backoff=5,  # 5s, 10s, 20s, ...
    retry_backoff_max=60,  # max 60s
    retry_kwargs={"max_retries": 5},
    retry_jitter=True,  # tránh retry cùng lúc
)
def send_template_email(payload: dict):
    try:
        valid_payload = EmailTemplateSchema.model_validate(payload)

        email_service.send_template_email(data=valid_payload)
    except Exception as e:
        raise e

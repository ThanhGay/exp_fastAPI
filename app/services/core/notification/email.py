from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.schemas.common.email import EmailTextSchema, EmailTemplateSchema
from app.core.config import settings


class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_STARTTLS=settings.MAIL_TLS,
            MAIL_SSL_TLS=settings.MAIL_SSL,
            USE_CREDENTIALS=settings.USE_CREDENTIALS,
            VALIDATE_CERTS=settings.VALIDATE_CERTS,
        )
        self.fm = FastMail(self.conf)

        # Setup Jinja2
        template_dir = settings.TEMPLATE_DIR
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

    async def send_text_email(self, data: EmailTextSchema):
        message = MessageSchema(
            subject=data.subject,
            recipients=data.recipients,
            body=data.body,
            subtype=MessageType.plain,
        )

        await self.fm.send_message(message)

    async def send_html_email(self, data: EmailTextSchema):
        message = MessageSchema(
            subject=data.subject,
            recipients=data.recipients,
            body=data.body,
            subtype=MessageType.html,
        )

        await self.fm.send_message(message)

    def __render_template(self, template_name: str, context: dict) -> str:
        template = self.env.get_template(template_name)
        return template.render(**context)

    async def send_template_email(self, data: EmailTemplateSchema):
        html_content = self.__render_template(data.template_name, data.context)

        message = MessageSchema(
            subject=data.subject,
            recipients=data.recipients,
            body=html_content,
            subtype=MessageType.html,
        )

        await self.fm.send_message(message)


email_service = EmailService()

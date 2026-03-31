from typing import List
from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    subject: str
    recipients: List[EmailStr]

class EmailTextSchema(EmailSchema):
    body: str

class EmailTemplateSchema(EmailSchema):
    template_name: str
    context: dict

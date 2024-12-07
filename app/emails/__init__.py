from datetime import datetime
from pathlib import Path
from typing import List, Union
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr

from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME="",
    MAIL_PASSWORD="",
    MAIL_FROM="test@example.com",
    MAIL_PORT=settings.email_port,
    MAIL_SERVER=settings.email_server,
    MAIL_FROM_NAME="my name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


def create_email_html_message(
    recipients: List[EmailStr],
    template_body: dict[str, Union[str, int, float, bool]],
    subject: str = "",
):
    body = {"year": datetime.now().year, **template_body}
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        subtype=MessageType.html,
        template_body=body,
    )

    return message


fast_mail = FastMail(conf)

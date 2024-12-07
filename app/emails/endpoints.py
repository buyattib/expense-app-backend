from datetime import datetime
from fastapi import APIRouter, BackgroundTasks

from fastapi_mail import MessageSchema, MessageType
from app.emails import fast_mail

router = APIRouter(
    prefix="/emails",
    tags=["Emails"],
)


@router.get("/test")
async def test(background_tasks: BackgroundTasks):
    # html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=["recipient@exmaple.com"],
        subtype=MessageType.html,
        # body=html,
        template_body={
            "header_text": "Hello template",
            "recipient_name": "test recipient",
            "sender_name": "myself",
            "year": datetime.now().year,
        },
    )

    # background_tasks.add_task(fast_mail.send_message, message)
    background_tasks.add_task(
        fast_mail.send_message, message, template_name="test.html"
    )

    return {"message": "OK"}

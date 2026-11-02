import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from fastapi import HTTPException

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "default@yandex.ru"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "password"),
    MAIL_FROM=os.getenv("MAIL_FROM", "default@yandex.ru"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_reset_password_email(email_to: EmailStr, reset_token: str):
    reset_link = f"http://localhost:5173/reset-password?token={reset_token}"
    
    html = f"""
    <p>Вы запросили сброс пароля на платформе Interview Platform.</p>
    <p>Для создания нового пароля перейдите по ссылке:</p>
    <a href="{reset_link}">{reset_link}</a>
    <p>Если вы не запрашивали сброс, просто проигнорируйте это письмо.</p>
    """

    message = MessageSchema(
        subject="Сброс пароля",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        # ВЫВОДИМ ОШИБКУ В КОНСОЛЬ, ЧТОБЫ ПОНЯТЬ ПРИЧИНУ
        print(f"ОШИБКА SMTP: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка почты: {str(e)}")
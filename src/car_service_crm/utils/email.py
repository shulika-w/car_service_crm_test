"""Асинхронна відправка email через SMTP (підтвердження записів тощо)."""

import os
from dotenv import load_dotenv
from aiosmtplib import SMTP
from email.message import EmailMessage

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

async def send_email_async(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = SMTP_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        smtp = SMTP(
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            use_tls=False 
        )
        print(f"SMTP_HOST={SMTP_HOST}, SMTP_PORT={SMTP_PORT}")
        await smtp.connect()
        await smtp.login(SMTP_USER, SMTP_PASSWORD)
        await smtp.send_message(message)
        await smtp.quit()
        print("Email sent!")
    except Exception as e:
        print(f"Email sending failed: {e}")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import asyncio

MAIL_USERNAME = "prashantbhosale948@gmail.com"
MAIL_PASSWORD = "cyjr ccaj hyhl qoeq"   # App password
MAIL_FROM = "prashantbhosale948@gmail.com"
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_FROM_NAME = "M Organisation"


async def send_email(recipients: List[str]):
    """Send a registration confirmation email to the given list of recipients."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send_sync, recipients)


def _send_sync(recipients: List[str]):
    msg = MIMEMultipart()
    msg["Subject"] = "Registration Confirmation"
    msg["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM}>"
    msg["To"] = ", ".join(recipients)

    body = "Hi, thanks for registering with us! Our team will connect with you soon."
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_FROM, recipients, msg.as_string())

from typing import List

from app.db.settings import settings
from fastapi_mail import (ConnectionConfig, FastMail,  # type: ignore
                          MessageSchema)
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, EmailStr

email_template_env = Environment(loader=FileSystemLoader('app/core/templates'))


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, username: str, confirmation_token: bytes, email: List[EmailStr]):
        self.name = username
        self.email = email
        self.confirmation_token = confirmation_token
        pass

    async def sendMail(self):
        # Define the config
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.email_username,
            MAIL_PASSWORD=settings.email_password,
            MAIL_FROM=EmailStr(settings.email_from),
            MAIL_PORT=settings.email_port,
            MAIL_SERVER=settings.email_server,
            MAIL_TLS=False,
            MAIL_SSL=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            SUPPRESS_SEND=settings.suppress_send
        )
        # Generate the HTML template base on the template name
        template = email_template_env.get_template('base.html')
        html = template.render(
            url=f"{settings.api_URI}/v1/users/confirm_email/{self.confirmation_token.hex()}",
            first_name=self.name,
            subject="Your verification code Valid for 15min"
        )
        # Define the message options
        message = MessageSchema(
            subject="Your verification code is Valid for 15min",
            recipients=self.email,
            html=html,
            subtype="html"
        )
        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

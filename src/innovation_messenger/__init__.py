import smtplib
from dataclasses import dataclass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Callable, Dict, List, Optional, Union

from commom import logger
from commom.base_classes.base_sender import BaseMessenger
from innovation_messenger.config import config


@dataclass
class IEmailProperties:
    subject: str
    body: str
    recipient: Union[str, List[str]]
    file_name: Optional[str] = None


class Messenger(BaseMessenger):
    sender_email = config.EMAIL_ACCOUNT
    sender_password = ""

    def __init__(self) -> None:
        self.get_sender_password()
        pass

    def send_message(
        self,
        channel: str,
        **kwargs,
    ) -> Any:
        channels: Dict[str, Callable] = {"email": self._send_email}

        return channels[channel](**kwargs)

    def _send_email(self, email_properties: IEmailProperties, **kwargs) -> bool:
        message = MIMEMultipart()
        message["Subject"] = email_properties.subject
        message["From"] = self.sender_email
        messageTo: str

        if isinstance(email_properties.recipient, List):
            messageTo = ", ".join(email_properties.recipient)
        else:
            messageTo = email_properties.recipient

        message["To"] = messageTo
        html_part = MIMEText(email_properties.body)
        message.attach(html_part)

        if email_properties.file_name:
            with open(email_properties.file_name, "rb") as attachment:
                # Add the attachment to the message
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {email_properties.file_name}",
            )
            message.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            try:
                server.login(user=self.sender_email, password=self.sender_password)
                server.sendmail(self.sender_email, email_properties.recipient, message.as_string())
                return True
            except Exception as e:
                logger.error(e)
                return False

    def get_sender_password(self) -> None:
        password_list = config.EMAIL_PASSWORDS.split(",")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            for password in password_list:
                try:
                    server.login(user=config.EMAIL_ACCOUNT, password=password)
                    self.sender_password = password
                except smtplib.SMTPAuthenticationError:
                    print("Usuário ou senha incorretos.")

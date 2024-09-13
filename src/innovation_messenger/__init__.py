import smtplib
from dataclasses import dataclass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Callable, Dict, List, Optional, Union

from commom.base_classes.base_sender import BaseMessenger
from innovation_messenger.config import config


@dataclass
class IEmailProperties:
    subject: str
    body: str
    recipient: Union[str, List[str]]
    file_name: Optional[str] = None


class Messenger(BaseMessenger):
    def __init__(self) -> None:
        pass

    @classmethod
    def send_message(
        cls,
        channel: str,
        **kwargs,
    ) -> None:
        channels: Dict[str, Callable] = {"email": cls._send_email}

        channels[channel](**kwargs)

    @classmethod
    def _send_email(cls, email_properties: IEmailProperties, **kwargs):
        message = MIMEMultipart()
        sender_email = config.EMAIL_ACCOUNT
        message["Subject"] = email_properties.subject
        message["From"] = sender_email
        if isinstance(email_properties.recipient, List):
            message["To"] = ", ".join(email_properties.recipient)
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
            server.login(sender_email, config.EMAIL_PASSWORD)
            server.sendmail(sender_email, email_properties.recipient, message.as_string())

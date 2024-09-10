from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Optional, Callable, Dict
from dataclasses import dataclass, field

from innovation_messenger.base_classes.base_sender import BaseSender

@dataclass
class IEmailSender:
  file_name: Optional[str]
  subject: str
  body: str
  recipient: str

class Messenger(BaseSender):
  def __init__(self) -> None:
    pass
  
  @classmethod
  def _send_email(
      cls, 
      email_sender: IEmailSender,
      **kwargs
    ):
    message = MIMEMultipart()
    sender_email= 'inovacao@ammovarejo.com.br'
    message['Subject'] = email_sender.subject
    message['From'] = sender_email
    message['To'] = email_sender.recipient
    html_part = MIMEText(email_sender.body)
    message.attach(html_part)

    if email_sender.file_name:
        with open(email_sender.file_name, "rb") as attachment:
            # Add the attachment to the message
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {email_sender.file_name}",
        )
        message.attach(part)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, '@ed8Q124')
        server.sendmail(sender_email, email_sender.recipient, message.as_string())

  @classmethod
  def send_report(
    cls,
    report_channel: str,
    **kwargs,
  ) -> None:
    report_channels: Dict[str, Callable] = {
      'email': cls._send_email
    }

    report_channels[report_channel](**kwargs)
    
    

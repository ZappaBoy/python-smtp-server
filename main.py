import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from typing import List

from models.attachment import Attachment
from models.communication import Communication
from models.receiver import Receiver
from models.smtp_config_model import SMTPConfigModel


class SMTPService:
    use_initial_tls: bool = True

    def __init__(self, smtp_config: SMTPConfigModel):
        self.host = smtp_config.host
        self.port = smtp_config.port
        self.address = smtp_config.address
        self.password = smtp_config.password
        self.smtp_server = None

    def set_initial_tls(self, use_tls: bool):
        self.use_initial_tls = use_tls

    def send_communication(self, communication: Communication):
        self.send_multiple_plain_text_mail(communication.receivers, communication.title,
                                           communication.description)

    def send_communication_with_media(self, communication: Communication,
                                      media: List[Attachment]):
        self.send_multiple_mail_with_attachments(communication.receivers, communication.title,
                                                 communication.description, media)

    def _connect(self):
        if self.use_initial_tls:
            self.smtp_server = smtplib.SMTP_SSL(host=self.host, port=self.port)
            self.smtp_server.ehlo()
        else:
            self.smtp_server = smtplib.SMTP(host=self.host, port=self.port)
            self.smtp_server.starttls()
        self.smtp_server.login(self.address, self.password)

    def _create_plain_text_message(self, receiver: str, subject: str, text: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = self.address
        message["To"] = receiver
        message["Subject"] = subject
        message["Date"] = formatdate()
        message["Message-Id"] = make_msgid()
        message.attach(MIMEText(text, 'html'))
        return message

    @staticmethod
    def _add_attachments_to_message(message: MIMEMultipart, attachments) -> MIMEMultipart:
        for attachment in attachments:
            filename = attachment.filename
            part = MIMEApplication(
                attachment.file.read(),
                Name=filename
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % filename
            message.attach(part)
        return message

    @staticmethod
    def _add_attachments_to_multiple_messages(messages: List[MIMEMultipart], attachments: List[Attachment]) \
            -> List[MIMEMultipart]:
        for attachment in attachments:
            filename = attachment.filename
            part = MIMEApplication(
                attachment.file.read(),
                Name=filename
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % filename
            for message in messages:
                message.attach(part)
        return messages

    def _send_message(self, message: MIMEMultipart) -> bool:
        try:
            self._connect()
            self.smtp_server.send_message(message)
            del message

        except smtplib.SMTPException as e:
            print(e)
            return False
        else:
            self.smtp_server.quit()
            return True

    def _send_multiple_messages(self, messages: List[MIMEMultipart]) -> bool:
        try:
            self._connect()
            for message in messages:
                self.smtp_server.send_message(message)

        except smtplib.SMTPException as e:
            print(e)
            return False
        else:
            self.smtp_server.quit()
            return True

    def send_plain_text_mail(self, receiver: str, subject: str, message: str) -> bool:
        message = self._create_plain_text_message(receiver, subject, message)
        return self._send_message(message)

    def send_multiple_plain_text_mail(self, receivers: List[Receiver], subject: str, text: str) -> bool:
        messages: List[MIMEMultipart] = []
        for receiver in receivers:
            if receiver.email is not None:
                message = self._create_plain_text_message(receiver.email, subject, text)
                messages.append(message)
        return self._send_multiple_messages(messages) if len(messages) > 0 else False

    def send_mail_with_attachments(self, receiver: str, subject: str, message: str, attachments: List[Attachment]) \
            -> bool:
        message = self._create_plain_text_message(receiver, subject, message)
        message = self._add_attachments_to_message(message, attachments)
        return self._send_message(message)

    def send_multiple_mail_with_attachments(self, receivers: List[Receiver], subject: str, text: str,
                                            attachments: List[Attachment]) -> bool:
        messages = []
        for receiver in receivers:
            if receiver.email is not None:
                message = self._create_plain_text_message(receiver.email, subject, text)
                messages.append(message)
        messages = self._add_attachments_to_multiple_messages(messages, attachments)
        return self._send_multiple_messages(messages) if len(messages) > 0 else False


if __name__ == "__main__":
    configs = SMTPConfigModel(
        host=os.environ.get('ADMIN_SMTP_HOST'),
        port=os.environ.get('ADMIN_SMTP_PORT'),
        address=os.environ.get('ADMIN_SMTP_ADDRESS'),
        password=os.environ.get('ADMIN_SMTP_PASSWORD'),
    )
    print(configs)
    smtp_service = SMTPService(configs)
    receivers_list = [
        Receiver(
            name='Receiver name',
            last_name='Receiver last name',
            email='receiver@mail.com',
        )
    ]
    # Some services require TLS to be disabled when starting the connection.
    # Don't worry, TLS will start after the connection.
    smtp_service.set_initial_tls(False)
    smtp_service.send_multiple_plain_text_mail(receivers=receivers_list, subject='Test', text='This is a test mail.')

import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from ..models.send_mail_request_model import SendMailRequestModel
import logging

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',)

class MailService:
    @staticmethod
    async def send_mail(request: SendMailRequestModel):
        logging.info('sending mail')
        conf = get_conection_config()
        message = get_message(request)
        fm = FastMail(conf)
        await fm.send_message(message)
        logging.info('mail sended')


def get_conection_config():
    return ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM = os.getenv('MAIL_FROM'),
    MAIL_PORT = os.getenv('MAIL_PORT'),
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    TEMPLATE_FOLDER = os.getenv('MAIL_TEMPLATE_FOLDER_DIR'),
)

def get_message(request: SendMailRequestModel):
    print(request)
    if request.body_dict != None:
        return get_template_message(request)
    elif request.body.__contains__('<!DOCTYPE html>'):
        return get_html_message(request)
    else:
        return get_text_message(request)

def get_template_message(request: SendMailRequestModel):
    return MessageSchema(
        subject=request.subject,
        recipients=request.email,
        template_body=request.body_dict,
        subtype=MessageType.html,
        )

def get_html_message(request: SendMailRequestModel):
    return MessageSchema(
        subject= request.subject,
        recipients=request.email,
        body=request.body,
        subtype=MessageType.html,
        )

def get_text_message(request: SendMailRequestModel):
    return MessageSchema(
        subject= request.subject,
        recipients=request.email,
        body=request.body,
        subtype=MessageType.plain,
        )

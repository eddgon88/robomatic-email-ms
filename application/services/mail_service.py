import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from ..models.send_mail_request_model import SendMailRequestModel

class MailService:
    @staticmethod
    async def send_mail(request: SendMailRequestModel):
        conf = get_conection_config()
        print(conf)
        message = get_message(request)
        print(message)
        fm = FastMail(conf)
        print(type(fm))
        await fm.send_message(message)


def get_conection_config():
    return ConnectionConfig(
    #MAIL_USERNAME = os.environ('MAIL_USERNAME'),
    #MAIL_PASSWORD = os.environ('MAIL_PASSWORD'),
    #MAIL_FROM = os.environ('MAIL_FROM'),
    #MAIL_PORT = os.environ('MAIL_PORT'),
    #MAIL_SERVER = os.environ('MAIL_SERVER'),
    #MAIL_STARTTLS = True,
    #MAIL_SSL_TLS = False,
    #TEMPLATE_FOLDER = os.environ('MAIL_TEMPLATE_FOLDER_DIR'),
    MAIL_USERNAME = "edgarant.gonzalezbr@gmail.com",
    MAIL_PASSWORD = "obxfizkxrakipifc",
    MAIL_FROM = "edgarant.gonzalezbr@gmail.com",
    MAIL_PORT = "587",
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    TEMPLATE_FOLDER = "",
)

def get_message(request: SendMailRequestModel):
    if request.body_dict != None:
        return get_template_message(request)
    elif request.body.__contains__('<!DOCTYPE html>'):
        return get_html_message(request)
    else:
        return get_text_message(request)

def get_template_message(request: SendMailRequestModel):
    return MessageSchema(
        subject="Fastapi-Mail module",
        recipients=request.emailm,
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

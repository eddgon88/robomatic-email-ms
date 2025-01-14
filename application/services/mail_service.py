import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from ..models.send_mail_request_model import SendMailRequestModel
import logging
from pathlib import Path
from fastapi import HTTPException, UploadFile, BackgroundTasks
from typing import List
import requests
import io

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',)

class MailService:
    @staticmethod
    async def send_mail(request: SendMailRequestModel):
        logging.info('sending mail')
        conf = get_conection_config()
        message = get_message(request)
        if len(request.files) != 0:
            message.attachments = add_attachments(request.files, request.execution_id)
        fm = FastMail(conf)
        await fm.send_message(message)
        logging.info('mail sent')

    @staticmethod
    async def send_mail_background(request: SendMailRequestModel, background_tasks: BackgroundTasks):
        logging.info('sending mail')
        conf = get_conection_config()
        message = get_message(request)
        if len(request.files) != 0:
            add_attachments(request.files, request.execution_id)
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
        logging.info('mail task added to background')


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
    if request.body_dict:
        return get_template_message(request)
    elif '<!DOCTYPE html>' in request.body:
        return get_html_message(request)
    else:
        return get_text_message(request)

def get_template_message(request: SendMailRequestModel):
    return MessageSchema(
        subject=request.subject,
        recipients=request.email,
        template_body=get_templete(request.template_id, request.body_dict),
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

def get_templete(template_name: str, body_dict: dict):
    try:
        html_file_path = Path(os.getenv('MAIL_TEMPLATE_FOLDER_DIR') + '/' + template_name)
        if not html_file_path.exists():
            raise HTTPException(status_code=404, detail="File html not found")
            
        html_content = html_file_path.read_text(encoding="utf-8")

        for key, value in body_dict.items():
            #logging.info(key)
            html_content = html_content.replace('##'+key+'##', value)

        logging.info('sending html mail - ' + html_content) 

        return html_content       

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def add_attachments( attachmentArray: List[str], execution_id: str):
    attachments = []
    for attachment in attachmentArray:
        try:
            res = requests.get(f"{os.getenv('FILE_MANAGER_API_URL')}/{execution_id}/{attachment}")
            if res.status_code == 200:
                file_like = io.BytesIO(res.content)
                #attachments.append((file_like, attachment))
                file_path = os.path.join(os.getenv('EVIDENCE_FILE_DIR'), execution_id, attachment)
                logging.info(file_path)
                attachments.append({"file": file_path, "content": file_like})
            else:
                logging.error(f'File not found - {attachment}')
        except Exception as e:
            logging.error(f'Error fetching file - {attachment}: {e}')
    return attachments
        

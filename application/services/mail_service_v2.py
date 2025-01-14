import os
from ..models.send_mail_request_model import SendMailRequestModel
import logging
from pathlib import Path
from fastapi import HTTPException
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',)

class MailService:
    @staticmethod
    def send_mail(request: SendMailRequestModel):
        message = get_message(request)
        if len(request.files) != 0:
            add_attachments(request.files, request.execution_id, message)
        try:
            server = smtplib.SMTP(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT'))
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
            server.sendmail(message['From'], request.email, message.as_string())
            server.close()
            logging.info('Mail sent successfully')
        except smtplib.SMTPException as e:
            logging.error('Error sending mail: %s', e)

def get_message(request: SendMailRequestModel):
    print(request)
    if request.body_dict:
        return get_template_message(request)
    elif '<!DOCTYPE html>' in request.body:
        return get_html_message(request)
    else:
        return get_text_message(request)

def get_template_message(request: SendMailRequestModel):
    message = MIMEMultipart("alternative")
    message["Subject"] = request.subject
    message["From"] = os.getenv('MAIL_USERNAME')
    message["To"] = ", ".join(request.email)
    part = MIMEText(get_templete(request.template_id, request.body_dict), "html")
    message.attach(part)
    return message

def get_html_message(request: SendMailRequestModel):
    message = MIMEMultipart("alternative")
    message["Subject"] = request.subject
    message["From"] = os.getenv('MAIL_USERNAME')
    message["To"] = ", ".join(request.email)
    part = MIMEText(request.body, "html")
    message.attach(part)
    return message

def get_text_message(request: SendMailRequestModel):
    message = MIMEMultipart("alternative")
    message["Subject"] = request.subject
    message["From"] = os.getenv('MAIL_USERNAME')
    message["To"] = ", ".join(request.email)
    part = MIMEText(request.body, "plain")
    message.attach(part)
    return message

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
    
def add_attachments( attachmentArray: List[str], execution_id: str, message):
    attachments = []
    for attachment in attachmentArray:
        try:
            f = os.path.join(os.getenv('EVIDENCE_FILE_DIR'), execution_id, attachment)
            with open(f, "rb") as fil:
                file_part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            file_part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            message.attach(file_part)
        except Exception as e:
            logging.error(f'Error fetching file - {attachment}: {e}')
    return attachments
        

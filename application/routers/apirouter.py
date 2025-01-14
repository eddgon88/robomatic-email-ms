from fastapi import APIRouter, BackgroundTasks
import asyncio
#from ..services.mail_service import MailService
from ..services.mail_service_v2 import MailService
from ..models.send_mail_request_model import SendMailRequestModel
import threading

router = APIRouter(prefix="/email-api/v1")

async def some_callback(args):
    await MailService.send_mail(args)

def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(some_callback(args))
    loop.close()

#@router.post("/send-mail", status_code=200)
#async def consume(params: SendMailRequestModel):
#    threading_execution = threading.Thread(target=between_callback, args=(params,))
#    threading_execution.start()
#    #TestExecutorService.executeTest(params.dict())
#    return True

#@router.post("/send-mail")
#async def send_email(request: SendMailRequestModel, background_tasks: BackgroundTasks):
#    await MailService.send_mail_background(request, background_tasks)
#    return {"message": "Email sent"}

@router.post("/send-mail")
async def send_email(background_tasks: BackgroundTasks, request: SendMailRequestModel):
    background_tasks.add_task(MailService.send_mail, request)
    return {"message": "Email sent"}
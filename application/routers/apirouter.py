from fastapi import APIRouter
import asyncio
from ..services.mail_service import MailService
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

@router.post("/send-mail", status_code=200)
async def consume(params: SendMailRequestModel):
    threading_execution = threading.Thread(target=between_callback, args=(params,))
    threading_execution.start()
    #TestExecutorService.executeTest(params.dict())
    return True
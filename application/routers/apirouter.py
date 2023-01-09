from fastapi import APIRouter
import asyncio
from ..jms.jms_client import PikaClient
from ..services.mail_service import MailService

router = APIRouter(prefix="/emai/v1")

@router.on_event("startup")
async def startup():
    print("start")
    loop = asyncio.get_running_loop()
    pikaClient = PikaClient(MailService.send_mail)
    task = loop.create_task(pikaClient.consume(loop))
    await task
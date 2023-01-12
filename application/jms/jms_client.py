from ..services.mail_service import MailService
from ..models.send_mail_request_model import SendMailRequestModel
import pika
from aio_pika import connect_robust
import ast

class PikaClient:

    def __init__(self, process_callable):
        params = pika.URLParameters('amqp://admin:admin@127.0.0.1:5672')
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel() # start a channel
        self.channel.queue_declare(queue='tasks.send_mail') # Declare a queue
        self.response = None
        self.process_callable = process_callable
        print('Pika connection initialized')

    async def consume(self, loop):
        connection = await connect_robust(host="127.0.0.1",
                                        port=5672,
                                        login="admin",
                                        password="admin",
                                        loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue('tasks.send_mail')
        await queue.consume(self.process_incoming_message, no_ack=True)
        print('Established pika async listener')
        return connection

    async def process_incoming_message(self, message):
        message.ack()
        body = message.body
        print('Received message')
        print(body)
        if body:
            body_str = body.decode("UTF-8")
            content = ast.literal_eval(body_str)  
            print(type(content))
            request = SendMailRequestModel.parse_obj(content)
            print(type(request))
            await MailService.send_mail(request)
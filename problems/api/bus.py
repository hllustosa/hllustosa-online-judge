import json
import asyncio
import threading
import pika
from problems.settings import RABBITMQ
from aio_pika import connect, Message, DeliveryMode, ExchangeType, exchange
from django.forms.models import model_to_dict
from django.core import serializers

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


class Bus(threading.Thread):

    async def init(self):
        self.connection = await connect(RABBITMQ)
        self.channel = await self.connection.channel()
        self.runs_exchange = await self.channel.declare_exchange("runs", ExchangeType.FANOUT)

    async def send_run_async(self, run):

        await self.init()
        message_body = json.dumps(run)

        message = Message(
            message_body.encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT
        )

        # Sending the message
        await self.runs_exchange.publish(message, routing_key="runs")

    def send_run(self, run):
        asyncio.run(self.send_run_async(run))

    def get_connection(self):
        parameters = pika.URLParameters(RABBITMQ)
        return pika.BlockingConnection(parameters)

    def set_on_message(self, on_message):
        self.on_message = on_message

    def run(self):
        connection = self.get_connection()
        channel = connection.channel()

        channel.exchange_declare(exchange='notifications', exchange_type='fanout')
        channel.queue_declare(queue='notifications', exclusive=False)
        
        channel.queue_bind(exchange='notifications', queue='notifications')
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_message_callback=self.callback, queue='notifications', auto_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        self.on_message(body)
        pass
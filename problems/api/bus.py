import json
import asyncio
from problems.settings import RABBITMQ
from aio_pika import connect, Message, DeliveryMode, ExchangeType
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


class Bus():

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

import json
import asyncio
from runner.settings import RABBITMQ
from aio_pika import connect, Message, DeliveryMode, ExchangeType
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
        self.notifications_exchange = await self.channel.declare_exchange("notifications", ExchangeType.FANOUT)

    async def send_notifications_async(self, notification):

        await self.init()
        message_body = json.dumps(notification)

        message = Message(
            message_body.encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT
        )

        # Sending the message
        await self.notifications_exchange.publish(message, routing_key="notifcation")

    def send_notification(self, notification):
        asyncio.run(self.send_notifications_async(notification))

    async def register_message(self, on_message, loop):

        connection = await connect(
            RABBITMQ, loop=loop
        )

        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        logs_exchange = await channel.declare_exchange(
            "runs", ExchangeType.FANOUT
        )

        # Declaring queue
        queue = await channel.declare_queue(name="runs", exclusive=False)

        # Binding the queue to the exchange
        await queue.bind(logs_exchange)

        # Start listening the queue with name 'task_queue'
        await queue.consume(on_message)

from .settings import RABBITMQ
import asyncio
import json
from aio_pika import connect, IncomingMessage, ExchangeType

loop = asyncio.get_event_loop()


async def on_message(message: IncomingMessage):
    async with message.process():
        msg = json.loads(message.body)
        print(msg)


async def code_runner():

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
    queue = await channel.declare_queue(exclusive=True)

    # Binding the queue to the exchange
    await queue.bind(logs_exchange)

    # Start listening the queue with name 'task_queue'
    await queue.consume(on_message)

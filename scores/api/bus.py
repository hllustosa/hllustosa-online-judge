import asyncio
import threading
import pika
from scores.settings import RABBITMQ


class Bus(threading.Thread):

    def get_connection(self):
        parameters = pika.URLParameters(RABBITMQ)
        return pika.BlockingConnection(parameters)

    def set_on_message(self, on_message):
        self.on_message = on_message

    def run(self):
        connection = self.get_connection()
        channel = connection.channel()

        channel.exchange_declare(exchange='notifications', exchange_type='fanout')
        channel.queue_declare(queue='scores-notifications', exclusive=False)
        
        channel.queue_bind(exchange='notifications', queue='scores-notifications')
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_message_callback=self.callback, queue='scores-notifications', auto_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        self.on_message(body)
        pass
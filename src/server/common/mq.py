import pika


class RabbitQueue:

    def __init__(self):
        self._parameters = pika.ConnectionParameters('localhost')

    def __enter__(self):
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.close()
        self._connection.close()

    def create_queue(self, queue_identifier: str):
        self._channel.queue_declare(queue=queue_identifier, durable=True)

    def send_message(self, queue_identifier: str, message: str):
        self._channel.basic_publish(
            exchange='',
            routing_key=queue_identifier,
            body=message.encode()
        )

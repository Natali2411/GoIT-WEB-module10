import pika
from .rabbit_connect import make_exchange_queue_bind
import json


from authors_quotes.settings import (RABBITMQ_EXCHANGE, RABBITMQ_QUEUE)


def publish_author_info(author_name: str = None, author_part_link: str = None):
    channel, connection = make_exchange_queue_bind()
    message = {
        "name": author_name,
        "link": author_part_link
    }
    channel.basic_publish(
        exchange=RABBITMQ_EXCHANGE,
        routing_key=RABBITMQ_QUEUE,
        body=json.dumps(message).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
    print(" [x] Sent %r" % message)
    connection.close()



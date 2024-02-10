import json
import threading
from queue import Queue

from pika.adapters.blocking_connection import BlockingChannel


def read_rabbit_msg(channel: BlockingChannel, queue_name: str, result_queue: Queue,
                    locker: threading.RLock):
    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Received {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # Check the condition to stop consuming
        author_name, author_link = message.get("name"), message.get("link")
        if not (author_name and author_link):
            ch.stop_consuming()
        with locker:
            result_queue.put(message)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()

import pika
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

def monitor_progress(interval=5):
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD')
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue', durable=True)

    total_sent = 0
    total_failed = 0
    total_time = 0

    while True:
        queue_state = channel.queue_declare(queue='sms_queue', durable=True, passive=True)
        message_count = queue_state.method.message_count

        method_frame, header_frame, body = channel.basic_get('sms_queue', auto_ack=False)
        if method_frame:
            message = json.loads(body)
            total_sent += 1

            processing_time = message.get('processing_time', 0)
            total_time += processing_time

            if message.get('failed', False):
                total_failed += 1

            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        average_time = total_time / total_sent if total_sent > 0 else 0

        print(f"Messages in queue: {message_count}")
        print(f"Total messages sent: {total_sent}")
        print(f"Total messages failed: {total_failed}")
        print(f"Average time per message: {average_time:.2f} seconds")

        time.sleep(interval)

if __name__ == "__main__":
    interval = int(os.getenv('MONITOR_INTERVAL', 5))
    monitor_progress(interval)

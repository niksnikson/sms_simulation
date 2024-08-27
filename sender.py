import pika
import json
import random
import time
import sys
from dotenv import load_dotenv
import os
import redis

load_dotenv()

def send_message(ch, method, properties, body, r, mean_time, failure_rate):
    message = json.loads(body)

    mean_time = float(os.getenv('SENDER_MEAN_TIME', mean_time))
    failure_rate = float(os.getenv('SENDER_FAILURE_RATE', failure_rate))

    start_time = time.time()
    time.sleep(random.expovariate(1 / mean_time))
    processing_time = time.time() - start_time

    message['processing_time'] = processing_time
    message['failed'] = random.random() < failure_rate

    if message['failed']:
        print(f"Failed to send message to {message['phone_number']}")
        r.incr('failed_count')
    else:
        print(f"Successfully sent message to {message['phone_number']}")

    r.incr('sent_count')
    r.incrbyfloat('total_time', processing_time)

    # Ensure that method and delivery_tag are valid before calling basic_ack
    if method and hasattr(method, 'delivery_tag'):
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print("Warning: method or delivery_tag is None")

def start_sending(mean_time, failure_rate):
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD')
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), credentials=credentials)
    )
    channel = connection.channel()

    r = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, db=0)

    channel.queue_declare(queue='sms_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sms_queue', on_message_callback=lambda ch, method, properties, body: send_message(ch, method, properties, body, r, mean_time, failure_rate))

    print(f'[*] Waiting for messages with mean time: {mean_time}s and failure rate: {failure_rate*100}%. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    # Get mean time and failure rate from command-line arguments or default values
    mean_time = float(sys.argv[1]) if len(sys.argv) > 1 else float(os.getenv('SENDER_MEAN_TIME', 1.0))
    failure_rate = float(sys.argv[2]) if len(sys.argv) > 2 else float(os.getenv('SENDER_FAILURE_RATE', 0.1))

    start_sending(mean_time, failure_rate)

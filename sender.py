import pika
import json
import random
import time
import sys
from dotenv import load_dotenv
import os

load_dotenv()

def send_message(ch, method, properties, body):
    message = json.loads(body)
    mean_time = float(os.getenv('SENDER_MEAN_TIME', 1.0))
    failure_rate = float(os.getenv('SENDER_FAILURE_RATE', 0.1))

    start_time = time.time()
    time.sleep(random.expovariate(1 / mean_time))
    processing_time = time.time() - start_time

    message['processing_time'] = processing_time
    message['failed'] = random.random() < failure_rate

    if message['failed']:
        print(f"Failed to send message to {message['phone_number']}")
    else:
        print(f"Successfully sent message to {message['phone_number']}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_sending():
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD')
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sms_queue', on_message_callback=send_message)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_sending()

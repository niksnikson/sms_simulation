import pika
import json
import random
import string
import sys
from dotenv import load_dotenv
import os

load_dotenv()

def generate_message():
    phone_number = ''.join(random.choice(string.digits) for _ in range(10))
    message = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(100))
    return {
        "phone_number": phone_number,
        "message": message
    }

def produce_messages(count=1000):
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD')
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue', durable=True)

    for _ in range(count):
        message = generate_message()
        channel.basic_publish(
            exchange='',
            routing_key='sms_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    connection.close()

if __name__ == "__main__":
    count = int(os.getenv('MESSAGE_COUNT', 1000))
    produce_messages(count)

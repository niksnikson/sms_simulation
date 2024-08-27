import time
import os
import redis
from dotenv import load_dotenv

load_dotenv()

def monitor_progress(interval=5, iterations=None):
    r = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, db=0)

    current_iteration = 0
    while iterations is None or current_iteration < iterations:
        sent_count = int(r.get('sent_count') or 0)
        failed_count = int(r.get('failed_count') or 0)
        total_time = float(r.get('total_time') or 0.0)

        average_time = total_time / sent_count if sent_count > 0 else 0

        print(f"Total messages sent: {sent_count}")
        print(f"Total messages failed: {failed_count}")
        print(f"Average time per message: {average_time:.2f} seconds")

        time.sleep(interval)
        current_iteration += 1

if __name__ == "__main__":
    interval = int(os.getenv('MONITOR_INTERVAL', 5))
    monitor_progress(interval)

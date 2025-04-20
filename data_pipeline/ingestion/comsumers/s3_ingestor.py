import os
import json 
from confluent_kafka import Consumer
import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client("s3")

conf = {
    'bootstrap.servers':os.getenv("KAKFA_BOOTSTRAP_SERVERS"),
}
consumer = Consumer(conf)


for message in consumer:
    try: 
        data = message.value
        s3.put_object()
    except Exception as e: 
        print(f"Error processing message: {e}")

import os
import json 
import datetime 
import random
import time
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

def generate_mock_response(num_records:int=1) -> None:
    """Generates mock stock data."""
    data = []

    now = datetime.datetime.now()
    for _ in range(num_records):
        record = {
            "Symbol": random.choice(["AAA","BBB","CCC"]),
            "Value": str(random.randint(29000, 30000)),  # Simulate price fluctuations
            "TradingDate": now.strftime("%d/%m/%Y"),
            "Time": now.strftime("%H:%M:%S"),
            "Open": str(random.randint(29000, 30000)),
            "High": str(random.randint(29000, 30000)),
            "Low": str(random.randint(29000, 30000)),
            "Close": str(random.randint(29000, 30000)),
            "Volume": str(random.randint(100000, 1000000)),
        }
        data.append(record)
        time.sleep(0.1)

    message = {
        "data": data,
        "message": "Success",
        "status": "Success",
        "totalRecord": len(data),
    }
    return message

def run_mock_producer():
    """Runs the mock Kafka producer."""
    conf = {
        'bootstrap.servers':os.getenv("KAKFA_BOOTSTRAP_SERVERS")
    }
    producer = Producer(conf)

    while True:
        mock_data = generate_mock_response()
        print(f"Sending data: {mock_data}")
        producer.produce("stock_data", value=json.dumps(mock_data).encode('utf-8'))
        producer.flush()
        time.sleep(5)




if __name__ == "__main__":
    run_mock_producer()







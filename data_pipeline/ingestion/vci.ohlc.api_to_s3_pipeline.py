import os
import logging
import threading
import argparse
from dotenv import load_dotenv
from data_pipeline.ingestion.utils.kakfa.producers import ApiProducer
from data_pipeline.ingestion.utils.kakfa.consumers import S3Consumer

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = "stock.vci.ohlc.v1"
S3_BUCKET = "dev-new-money"

def run_producer(symbol:str, from_ts: int, to_ts: int):
    """Run the API producer"""
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'client.id': 'stock.vci.producer'
    }
    
    api_url = os.getenv("VCI_BASE_URL") + "chart/OHLCChart/gap"
    payload = {
        "timeFrame": "ONE_HOUR",
        "symbols": [symbol],
        "from": from_ts,
        "to": to_ts
    }
    producer = ApiProducer(api_url, producer_config, KAFKA_TOPIC,payload)
    producer.run(poll_interval=60*15)

def run_consumer(symbol: str):
    """Run the S3 consumer"""
    consumer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': f'stock.vci.ohlc.{symbol}.consumers',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = S3Consumer(consumer_config, KAFKA_TOPIC, S3_BUCKET)
    consumer.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Kafka API to S3 pipeline')
    parser.add_argument('--mode', choices=['producer', 'consumer', 'both'], default='both', help='Which component to run')
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--from', required=True)
    parser.add_argument('--to', required=True)
    
    args = parser.parse_args()
    
    if args.mode == 'producer':
        run_producer()
    elif args.mode == 'consumer':
        run_consumer()
    elif args.mode == 'both':
        # Create threads for producer and consumer
        producer_thread = threading.Thread(target=run_producer, name="producer-thread")
        consumer_thread = threading.Thread(target=run_consumer, name="consumer-thread")

        # Start both threads
        producer_thread.start()
        consumer_thread.start()

        # Wait for both threads to complete
        producer_thread.join()
        consumer_thread.join()
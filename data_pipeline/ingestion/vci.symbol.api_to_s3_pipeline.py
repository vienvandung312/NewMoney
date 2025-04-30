import os
import logging
import argparse
import threading
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
KAFKA_TOPIC = "stock.vci.symbols.v1"
S3_BUCKET = "dev-new-money"

def run_producer():
    """Run the API producer"""
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'client.id': 'stock.vci.producer'
    }
    
    api_url = os.getenv("VCI_BASE_URL") + "price/symbols/getAll"
    
    producer = ApiProducer(api_url, producer_config, KAFKA_TOPIC)
    producer.run(poll_interval=15)

def run_consumer():
    """Run the S3 consumer"""
    consumer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'stock.vci.symbols.consumers',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = S3Consumer(consumer_config, KAFKA_TOPIC, S3_BUCKET)
    consumer.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Kafka API to S3 pipeline')
    parser.add_argument('--mode', choices=['producer', 'consumer', 'both'], 
                        default='both', help='Which component to run')
    
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
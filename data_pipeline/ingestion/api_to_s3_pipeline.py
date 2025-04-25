import os
import logging
import argparse
import threading
from data_pipeline.ingestion.utils.kakfa.producers import ApiProducer
from data_pipeline.ingestion.utils.kakfa.consumers import S3Consumer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = "dev"
S3_BUCKET = "dev-s3"

def run_producer():
    """Run the API producer"""
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'client.id': 'api-producer'
    }
    
    # Mock API URL - replace with your actual API
    api_url = "https://jsonplaceholder.typicode.com/posts"
    
    producer = ApiProducer(api_url, producer_config, KAFKA_TOPIC)
    producer.run()

def run_consumer():
    """Run the S3 consumer"""
    consumer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 's3-consumer-group',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = S3Consumer(consumer_config, KAFKA_TOPIC, S3_BUCKET)
    consumer.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Kafka API to S3 pipeline')
    parser.add_argument('--mode', choices=['producer', 'consumer', 'both'], 
                        default='both', help='Which component to run')
    
    args = parser.parse_args()
    
    if args.mode in ['producer', 'both']:
        producer_thread = threading.Thread(target=run_producer)
        producer_thread.daemon = True
        producer_thread.start()
    
    if args.mode in ['consumer', 'both']:
        run_consumer()
import os 
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()


def produce_to_kafka(topic: str, key: str, value: str) -> None:
    """
    Produce data to Kafka.
    
    Args:
        producer (Producer): The Kafka producer instance.
        topic (str): The Kafka topic to produce to.
        key (str): The key for the message.
        value (str): The value for the message.
    """
    conf = {
        'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    }
    try:
        producer = Producer(conf)
        producer.produce(topic, key=key, value=value.encode("utf-8"))
        producer.flush(30)
        print(f"Produced message to {topic} with key {key}")
    except Exception as e:
        print(f"Error producing to Kafka: {e}")
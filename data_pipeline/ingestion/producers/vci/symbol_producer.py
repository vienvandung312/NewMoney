import os 
import datetime
import hashlib
from confluent_kafka import Producer 
from dotenv import load_dotenv
from data_pipeline.ingestion.producers.vci.common import get_all_symbols
import redis
load_dotenv()

def _get_hash(string: str) -> str:
    """
    Generate a hash for the given data.
    
    Returns:
        str: The hash of the data.
    """
    return hashlib.sha256(string.encode()).hexdigest()

def _produce_to_kafka(topic: str, key: str, value: str) -> None:
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
    producer = Producer(conf)
    producer.produce(topic, key=key, value=value.encode("utf-8"))
    producer.flush()

if __name__ == "__main__":
        
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", ""),
        db=int(os.getenv("REDIS_DB", 0))
    )

    new_symbols = get_all_symbols()
    symbols_key = "stock_symbols_cache"
    
    # Check if cache exists and compare with new symbols
    if redis_client.exists(symbols_key):
        cached_symbols = redis_client.get(symbols_key).decode("utf-8")
        if _get_hash(cached_symbols) == _get_hash(new_symbols):
            print("No new symbols found.")
        else:
            print("New symbols found.")
            redis_client.set(symbols_key, new_symbols)
            _produce_to_kafka(topic="stock.vci.symbols.v1",
                              key=f"symbols_{str(datetime.datetime.now().timestamp())}",
                              value=new_symbols
                              )
    else:
        print("No cache found. Storing new symbols.")
        redis_client.set(symbols_key, new_symbols)
        _produce_to_kafka(topic="stock.vci.symbols.v1",
                            key=f"symbols_{str(datetime.datetime.now().timestamp())}",
                            value=new_symbols
                            )




    
    
    
    
    

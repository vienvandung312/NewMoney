from abc import ABC, abstractmethod
import json
import logging
from confluent_kafka import Consumer, Producer
from typing import Dict, Any, Callable, Optional, Tuple

class KafkaClientBase(ABC):
    """Base class for Kafka clients with common configuration functionality"""
    
    def __init__(self, config: Dict[str, Any], topic: str, logger=None):
        self.config = config
        self.topic = topic
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self._setup()
    
    def _setup(self):
        """Set up the Kafka client with configuration"""
        self.logger.info(f"Initializing Kafka client for topic: {self.topic}")
    
    def close(self):
        """Clean up resources"""
        self.logger.info("Closing Kafka client")


class KafkaProducerBase(KafkaClientBase):
    """Base producer class that handles Kafka producer boilerplate"""
    
    def __init__(self, config: Dict[str, Any], topic: str, logger=None):
        super().__init__(config, topic, logger)
        self.producer = Producer(self.config)
    
    def _setup(self):
        super()._setup()
        self.logger.info("Producer configured")
    
    def produce(self, key: str, value: Dict[str, Any]):
        """Produce message to Kafka topic"""
        try:
            self.producer.produce(
                self.topic,
                key=key.encode('utf-8') if key else None,
                value=json.dumps(value).encode('utf-8'),
                callback=self._delivery_report
            )
            self.producer.poll(0)  # Trigger delivery reports
        except Exception as e:
            self.logger.error(f"Error producing message: {e}")
            raise
    
    def _delivery_report(self, err, msg):
        """Callback for message delivery reports"""
        if err:
            self.logger.error(f"Message delivery failed: {err}")
        else:
            self.logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")
    
    def flush(self, timeout=10):
        """Flush producer queue"""
        self.producer.flush(timeout)
    
    def close(self):
        """Close producer connection"""
        self.flush()
        super().close()
    
    def run(self, poll_interval: int = 1, max_iterations: Optional[int] = None):
        """Run producer in a loop"""
        iteration = 0
        try:
            while max_iterations is None or iteration < max_iterations:
                key, value = self.produce_logic()
                if value:
                    self.produce(key, value)
                iteration += 1
        except KeyboardInterrupt:
            self.logger.info("Producer interrupted")
        finally:
            self.close()
    
    @abstractmethod
    def produce_logic(self) -> Tuple[str, Dict[str, Any]]:
        """Business logic for producing messages, to be implemented by subclasses"""
        pass


class KafkaConsumerBase(KafkaClientBase):
    """Base consumer class that handles Kafka consumer boilerplate"""
    
    def __init__(self, config: Dict[str, Any], topic: str, logger=None, 
                 error_handler: Optional[Callable] = None):
        # Ensure group.id is set
        if 'group.id' not in config:
            raise ValueError("Consumer config must include 'group.id'")
            
        super().__init__(config, topic, logger)
        self.consumer = Consumer(self.config)
        self.consumer.subscribe([self.topic])
        self.error_handler = error_handler or self._default_error_handler
    
    def _setup(self):
        super()._setup()
        self.logger.info(f"Consumer subscribed to topic: {self.topic}")
    
    def _default_error_handler(self, error, message=None):
        """Default error handler"""
        self.logger.error(f"Consumer error: {error}, message: {message}")
    
    def poll(self, timeout=1.0):
        """Poll for messages"""
        self.consumer.poll(timeout)
    
    def process_message(self, message):
        """Process a message"""
        if message is None:
            return
        
        if message.error():
            self.error_handler(message.error(), message)
            return
        
        try:
            # Decode message
            key = message.key().decode('utf-8') if message.key() else None
            value = json.loads(message.value().decode('utf-8'))
            
            # Process the message with business logic
            self.consume_logic(key, value)
            
            # Commit the offset
            self.consumer.commit(message)
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            # Don't commit offset on error
    
    def close(self):
        """Close consumer connection"""
        self.consumer.close()
        super().close()
    
    def run(self, poll_interval: float = 1.0, max_iterations: Optional[int] = None):
        """Run consumer in a loop"""
        iteration = 0
        try:
            while max_iterations is None or iteration < max_iterations:
                message = self.poll(poll_interval)
                self.process_message(message)
                iteration += 1 if message is not None else 0
        except Exception as e:
            self.logger.info(f"Consumer interrupted: {e}")
        finally:
            self.close()
    
    @abstractmethod
    def consume_logic(self, key: str, value: Dict[str, Any]):
        """Business logic for consuming messages, to be implemented by subclasses"""
        pass
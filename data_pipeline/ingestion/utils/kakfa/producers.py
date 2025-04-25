



class KafkaProducerBase(KafkaClientBase):
    """Base producer class that handles Kafka producer boilerplate"""

    def __init__(self, config: Dict[str, Any], topic: str, logger=None):
        super().__init__(config, topic, logger)
        self.producer = Producer(self.config)

 

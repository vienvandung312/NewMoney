
import os
import logging
import uuid
from typing import Dict, Any, Tuple
import requests
from data_pipeline.ingestion.utils.kakfa.base import KafkaProducerBase
from data_pipeline.ingestion.utils.requests import spoofed_requests


class ApiProducer(KafkaProducerBase):
    """Producer that fetches data from API and sends to Kafka"""
    
    def __init__(self, api_url: str, config: Dict[str, Any], topic: str):
        super().__init__(config, topic)
        self.api_url = api_url
        self.logger.info(f"API Producer initialized with URL: {self.api_url}")
    
    def fetch_data_from_api(self) -> Dict[str, Any]:
        """Fetch data from API"""
        try:
            response = spoofed_requests(url=self.api_url, timeout=10)
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return {}
    
    def produce_logic(self) -> Tuple[str, Dict[str, Any]]:
        """Implement the logic to get data and return as key-value pair"""
        data = self.fetch_data_from_api()
        if not data:
            self.logger.warning("No data fetched from API")
            return None, None
        
        # Generate a unique key for the message
        key = f"api-data-{uuid.uuid4()}"
        
        self.logger.info(f"Produced message with key: {key}")
        return key, data
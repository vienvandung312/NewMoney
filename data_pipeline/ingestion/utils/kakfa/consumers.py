import json
import time
import boto3
from data_pipeline.ingestion.utils.kakfa.base import KafkaConsumerBase
from typing import Dict, Any


class S3Consumer(KafkaConsumerBase):
    """Consumer that reads from Kafka and writes to S3"""
    
    def __init__(self, config: Dict[str, Any], topic: str, bucket_name: str):
        super().__init__(config, topic)
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
        self.logger.info(f"S3 Consumer initialized with bucket: {self.bucket_name}")
    
    def consume_logic(self, key: str, value: Dict[str, Any]):
        """Process consumed message and write to S3"""
        if not key or not value:
            self.logger.warning("Received empty message, skipping")
            return
        
        try:
            # Create S3 object key with timestamp for partitioning
            timestamp = time.strftime("%Y-%m-%d/%H")
            s3_key = f"data/{timestamp}/{key}.json"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json.dumps(value).encode('utf-8'),
                ContentType='application/json'
            )
            
            self.logger.info(f"Successfully wrote message to S3: {s3_key}")
        except Exception as e:
            self.logger.error(f"Failed to write to S3: {e}")
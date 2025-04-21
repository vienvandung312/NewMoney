import os 
import datetime
from dotenv import load_dotenv
from data_pipeline.ingestion.utils.requests import spoofed_requests
from data_pipeline.ingestion.utils.kafka import produce_to_kafka

load_dotenv()

if __name__ == "__main__":
        
    response = spoofed_requests(url="http://api.btmc.vn/api/BTMCAPI/getpricebtmc?key={}".format(os.getenv("BTMC_API_KEY")),
                                    method="GET",
                                )
    produce_to_kafka(topic="gold.btmc.price.v1",
                        key=f"price_{str(datetime.datetime.now().timestamp())}",
                        value=response.text
                        )
    
    
import os 
import datetime
from confluent_kafka import Producer 
from dotenv import load_dotenv
from data_pipeline.ingestion.producers.vci.common import get_ohlc
load_dotenv()

if __name__ == "__main__":
    start_date = 1712275200
    end_date = 1712361599
    data = get_ohlc(start_date=start_date, end_date=end_date, symbols="ACB")

    conf = {
        'bootstrap.servers':os.getenv("KAKFA_BOOTSTRAP_SERVERS")
    }

    producer = Producer(conf)
    producer.produce("stock-data", key=f"ACB_{start_date}_{str(datetime.datetime.now().timestamp())}", value=data.encode("utf-8"))
    producer.flush()

    print(data)
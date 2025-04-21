import os 
import datetime
from confluent_kafka import Producer 
from dotenv import load_dotenv
from data_pipeline.ingestion.producers.vci.common import get_ohlc
load_dotenv()

if __name__ == "__main__":
    start_ts = datetime.datetime.now().timestamp() - (60*60*24*7)
    end_ts = datetime.datetime.now().timestamp()
    data = get_ohlc(start_ts=start_ts, end_ts=end_ts, symbols="ACB")

    conf = {
        'bootstrap.servers':os.getenv("KAKFA_BOOTSTRAP_SERVERS")
    }

    producer = Producer(conf)
    producer.produce("stock-data", key=f"ACB_{start_date}_{str(datetime.datetime.now().timestamp())}", value=data.encode("utf-8"))
    producer.flush()

    print(data)
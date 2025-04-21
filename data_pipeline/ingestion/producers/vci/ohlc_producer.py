import datetime
import argparse
from data_pipeline.ingestion.producers.vci.common import get_ohlc
from data_pipeline.ingestion.utils.kafka import produce_to_kafka

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch OHLC data for a stock symbol.")
    parser.add_argument("symbol", help="Stock symbol to fetch OHLC data for")
    args = parser.parse_args()

    symbol = args.symbol
    start_ts = int(datetime.datetime.now().timestamp() - (60*60*24*7))
    end_ts = int(datetime.datetime.now().timestamp())
    data = get_ohlc(start_ts, end_ts, symbol)

    produce_to_kafka(topic="stock.vci.ohlc.v1",
                        key=f"ohlc_{symbol}_{str(datetime.datetime.now().timestamp())}",
                        value=data
                        )



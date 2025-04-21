import os
from dotenv import load_dotenv
from data_pipeline.ingestion.utils.requests import spoofed_requests

load_dotenv()

def get_all_symbols() -> str:
    response = spoofed_requests(url=os.getenv("VCI_BASE_URL") + "price/symbols/getAll",
                                    method="GET",
                                )
    return response.text

def get_icb() -> str:
    pass

def get_ohlc( start_ts:int|str, end_ts:int|str, symbols:str, intervals: str = "ONE_HOUR" ) -> str:
    payload = {
        "timeFrame": intervals,
        "symbols": [symbols],
        "from": int(start_ts),
        "to": int(end_ts)
    }
    
    response = spoofed_requests(url=os.getenv("VCI_BASE_URL") + "chart/OHLCChart/gap", 
                                method="POST",
                                data=payload,
                                )
    return response.text
    
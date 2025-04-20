import os
import random
import requests 
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_all_symbols() -> str:
    try: 
        response = requests.get(os.getenv("VCI_BASE_URL") + "price/symbols/getAll")
        return response.text
    except Exception as e:
        print("Encountered error: "+ e)
    
def get_icb() -> str:
    pass

def get_ohlc( start_date:int|str, end_date:int|str, symbols:str, intervals: str = "ONE_HOUR" ) -> str:
    try: 
        headers = {
            'Content-Type': 'application/json',
            'X-Mly-Id': str(uuid.uuid4()),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://trading.vietcap.com.vn',
            'Referer': 'https://trading.vietcap.com.vn/'
        }

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
        ]
        headers['User-Agent'] = random.choice(user_agents)
        payload = {
            "timeFrame": intervals,
            "symbols": [symbols],
            "from": int(start_date),
            "to": int(end_date)
        }
        
        response = requests.post(os.getenv("VCI_BASE_URL") + "chart/OHLCChart/gap", json=payload, headers=headers)
        return response.text
    except Exception as e:
        print("Encountered error: "+ e)
    
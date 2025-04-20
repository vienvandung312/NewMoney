import os
import requests 
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

def get_all_symbols() -> str:
    try: 
        response = requests.get(os.getenv("VCI_BASE_URL") + "price/symbols/getAll")
        return response.text
    except Exception as e:
        print("Encountered error: "+ e)
    


    
    
    
from src.config.worker import celery
from celery import shared_task
import requests
@celery.task
def fetch_stock_data(symbol: str, interval:int, api_key:str, sorted_by:str) -> str:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&apikey=demo'
    try:
        r = requests.get(url)
        data = r.json()
        return {"status":"success","data":data}
    except:
        return {"status":"failed", "data": {}}
    
@shared_task
def web_socket_stock(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=demo'
    try:
        r = requests.get(url)
        data = r.json()
        return {"status":"success","data":data}
    except:
        return {"status":"failed", "data": {}}
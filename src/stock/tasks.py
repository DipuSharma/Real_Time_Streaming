from src.config.worker import celery
from src.database.models import StockData
import random
from celery import shared_task
from src.config.database import SessionLocal
db = SessionLocal()
@celery.task
def fetch_stock_data(stock_ids):
    stock_data = []
    for id in stock_ids:
        price = random.uniform(10, 1000)
        exist_data = db.query(StockData).filter(StockData.stock_id == id).first()
        if not exist_data:
            print("Stock Record _______________________________1")
            stock_data.append({"stock_id": id, "price": price})
    data = [StockData(**res) for res in stock_data]
    db.add_all(data)
    db.commit()
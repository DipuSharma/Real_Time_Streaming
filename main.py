from fastapi import FastAPI
from src.stock import router as stock
from src.config.worker import celery

app = FastAPI()
app.include_router(stock.router)


from fastapi import FastAPI
from src.stock import router as stock
from src.config.worker import celery
from src.config.database import init_db


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()
app.include_router(stock.router)
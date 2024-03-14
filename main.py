from fastapi import FastAPI
from src.stock import router as stock
from src.config.worker import celery
from src.config.database import init_db
from src.stock.tasks import fetch_stock_data


app = FastAPI()


celery.conf.beat_schedule = {
    "run_every_five_sec": {
        "task": f"src.stock.tasks.fetch_stock_data",
        "schedule": 1.0,
    }
}

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(stock.router)
import json
import asyncio
import random
import websockets
from fastapi import Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import StreamingResponse, HTMLResponse
from src.stock.tasks import fetch_stock_data
from src.stock.schema import StockFilterSchema, UserRegistration
from src.config.database import get_db
from src.stock.service import user_registration, user_login

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def generate_stock_updates():
    while True:
        # Generate stock updates for 500 stocks
        updates = [{'stock_id': i, 'price': round(random.uniform(10, 1000), 2)} for i in range(500)]
        await asyncio.sleep(1)  # Simulate updates every second
        yield updates

@router.post("/signup")
async def registration(payload: UserRegistration,db: Session = Depends(get_db)):
    response, msg = await user_registration(db=db, payload=payload)
    return {"message": msg, "result": response}

@router.post("/signin")
async def login(payload: UserRegistration,db: Session = Depends(get_db)):
    response, msg = await user_login(db=db, payload=payload)
    return {"message": msg, "result": response}

@router.get("/", name="Push Stock in database")
async def data_streaming(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.websocket("/stocks")
async def get_stocks(websocket: WebSocket):
    # subscriptions = {}
    await websocket.accept()
    while True:
        async for updates in generate_stock_updates():
            for update in updates:
                stock_id = update['stock_id']
                try:
                    payload = json.dumps(update)
                    await websocket.send_json(json.loads(payload))
                except websockets.exceptions.ConnectionClosedError:
                    print("Client disconnected. Removing subscription.")
                # if stock_id in subscriptions:
                #     print("______________data______________2", update)
                #     for websocket in subscriptions[stock_id]:
                #         print("______________data______________3", update)
                #         try:
                #             payload = json.dumps(update)
                #             print(type(payload))
                #             await websocket.send_json(payload)
                #         except websockets.exceptions.ConnectionClosedError:
                #             print("Client disconnected. Removing subscription.")



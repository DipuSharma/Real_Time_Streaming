import json
import asyncio
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import StreamingResponse, HTMLResponse
from src.stock.tasks import fetch_stock_data
from src.stock.schema import StockFilterSchema, UserRegistration
from src.config.database import get_db
from src.stock.service import user_registration, user_login


router = APIRouter()

@router.post("/signup")
async def registration(payload: UserRegistration,db: Session = Depends(get_db)):
    response, msg = await user_registration(db=db, payload=payload)
    return {"message": msg, "result": response}


@router.post("/signin")
async def login(payload: UserRegistration,db: Session = Depends(get_db)):
    response, msg = await user_login(db=db, payload=payload)
    return {"message": msg, "result": response}

@router.get("/")
async def data_streaming(paylod: StockFilterSchema = Depends()):
    symbols_list = paylod.symbols.split(",")
    async def generate_stock_data():
        for symbol in symbols_list:
            result = fetch_stock_data.apply_async(args=[symbol, paylod.interval, paylod.api_key, paylod.sorted_by])
            while not result.ready():
                await asyncio.sleep(1)
            stock_data = result.get()
            yield json.dumps({"symbol": symbol, "data": f"{stock_data}\n"} )
    return StreamingResponse(content=generate_stock_data(), media_type="application/json")

@router.websocket("/stocks")
async def get_stocks(websocket: WebSocket, symbol: str="IBM"):
    await websocket.accept()
    while True:
        result = fetch_stock_data.delay(symbol)
        stock_data = result.get()
        await websocket.send_text(json.dumps(stock_data))
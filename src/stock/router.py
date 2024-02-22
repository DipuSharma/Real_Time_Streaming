import json
import asyncio
from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import StreamingResponse
from src.stock.tasks import fetch_stock_data, web_socket_stock
from src.stock.schema import StockFilterSchema


router = APIRouter()


@router.get("/")
async def data_streaming(paylod: StockFilterSchema = Depends()):
    symbols_list = paylod.symbols.split(",")
    async def generate_stock_data():
        for symbol in symbols_list:
            result = fetch_stock_data.apply_async(args=[symbol, paylod.interval, paylod.api_key, paylod.sorted_by])
            while not result.ready():
                await asyncio.sleep(1)
            stock_data = result.get()
            # if stock_data["data"]or stock_data.status == "failed":
            #     yield json.dumps({"status": stock_data["data"]["Information"]})
            yield json.dumps({"symbol": symbol, "data": f"{stock_data}\n"} )
    return StreamingResponse(content=generate_stock_data(), media_type="application/json")

@router.websocket("/stocks")
async def get_stocks(websocket: WebSocket, symbol: str="IBM"):
    await websocket.accept()
    while True:
        result = web_socket_stock.delay(symbol)
        stock_data = result.get()
        # if stock_data["data"]["Information"] or stock_data.status == "failed":
        #     yield json.dumps({"status": stock_data["data"]["Information"]})
        await websocket.send_text(json.dumps(stock_data))
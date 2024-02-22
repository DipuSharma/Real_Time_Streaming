from pydantic import BaseModel, Field

class StockFilterSchema(BaseModel):
    symbols: str = Field(description="Enter the symbol for streaming stock usign comma seperated eg: IBM,IMST, etc", default="IBM,")
    interval: int = Field(description="Enter the time interval", default=5)
    api_key: str = Field(description="Enter the  generated api-key by https://www.alphavantage.co/ ", default="demo")
    sorted_by : str = Field(description="Sorted Streaming", default="LATEST")
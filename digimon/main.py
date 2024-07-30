from fastapi import FastAPI

from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0.12
    tax: Optional[float] = None


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    return {"item_id": item_id}

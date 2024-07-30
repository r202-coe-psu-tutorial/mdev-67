from fastapi import FastAPI

from typing import Optional

from pydantic import BaseModel


class BaseItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0.12
    tax: Optional[float] = None


class CreatedItem(BaseItem):
    pass


class Item(BaseItem):
    id: int


class ItemList(BaseModel):
    items: list[Item]
    page: int
    page_size: int
    size_per_page: int


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/items")
async def created_item(item: CreatedItem) -> Item:
    print("created_item", item)
    data = item.dict()
    data["id"] = 1
    return Item.parse_obj(data)


@app.get("/items")
async def read_items() -> ItemList:
    return ItemList()


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    return Item()


@app.put("/items/{item_id}")
async def update_item(item_id: int) -> Item:
    return Item()


@app.delete("/items/{item_id}")
async def delete_item(item_id: int) -> Item:
    return Item()

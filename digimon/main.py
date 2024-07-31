from fastapi import FastAPI

from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session


class BaseItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0.12
    tax: Optional[float] = None


class CreatedItem(BaseItem):
    pass


class Item(BaseItem):
    id: int


class DBItem(Item, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemList(BaseModel):
    items: list[Item]
    page: int
    page_size: int
    size_per_page: int


connect_args = {}

engine = create_engine(
    "postgresql+pg8000://postgres:123456@localhost/digimondb",
    echo=True,
    connect_args=connect_args,
)


SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/items")
async def created_item(item: CreatedItem) -> Item:
    print("created_item", item)
    data = item.dict()
    dbitem = DBItem(**data)
    with Session(engine) as session:
        session.add(dbitem)
        session.commit()
    return Item.parse_obj(dbitem.dict())


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

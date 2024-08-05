from fastapi import APIRouter, HTTPException

from typing import Optional

from sqlmodel import Field, SQLModel, Session, select

from .. import models

router = APIRouter(prefix="/items")


@router.get("")
async def read_items() -> models.ItemList:
    items = []
    with Session(models.engine) as session:
        items = session.exec(select(models.DBItem)).all()

    return models.ItemList.from_orm(
        dict(items=items, page_size=0, page=0, size_per_page=0)
    )


@router.post("")
async def create_item(item: models.CreatedItem) -> models.Item | None:
    print("create_item", item)
    data = item.dict()
    dbitem = models.DBItem(**data)
    with Session(models.engine) as session:
        session.add(dbitem)
        session.commit()
        session.refresh(dbitem.merchant)
        print(">>>>>>>>>>>", dbitem)
        # print("xxxx", dbitem.merchant)

    return models.Item.from_orm(dbitem)


@router.get("/{item_id}")
async def read_item(item_id: int) -> models.Item:
    with Session(models.engine) as session:
        db_item = session.get(DBItem, item_id)
        if db_item:
            print(">>>", db_item)
            return models.Item.from_orm(db_item)

    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{item_id}")
async def update_item(item_id: int, item: models.UpdatedItem) -> models.Item:
    print("update_item", item)
    data = item.dict()
    with Session(models.engine) as session:
        db_item = session.get(DBItem, item_id)
        db_item.sqlmodel_update(data)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)

    return models.Item.from_orm(db_item)


@router.delete("/{item_id}")
async def delete_item(item_id: int) -> dict:
    with Session(models.engine) as session:
        db_item = session.get(DBItem, item_id)
        session.delete(db_item)
        session.commit()

    return dict(message="delete success")

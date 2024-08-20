from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import users


class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int | None = 0


class CreatedTransaction(BaseTransaction):
    pass


class UpdatedTransaction(BaseTransaction):
    pass


class Transaction(BaseTransaction):
    id: int


class DBTransaction(BaseTransaction, SQLModel, table=True):
    __tablename__ = "merchants"
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class TransactionList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    merchants: list[Transaction]
    page: int
    page_size: int
    size_per_page: int

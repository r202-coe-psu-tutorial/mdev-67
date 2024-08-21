from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

import decimal

from . import users


class BaseWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int | None = None
    money: float = 0


class CreatedWallet(BaseWallet):
    pass


class UpdatedWallet(BaseWallet):
    pass


class Wallet(BaseWallet):
    id: int


class DBWallet(BaseWallet, SQLModel, table=True):
    __tablename__ = "merchants"
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class WalletList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    merchants: list[Wallet]
    page: int
    page_size: int
    size_per_page: int

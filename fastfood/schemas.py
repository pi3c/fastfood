from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True


class Menu(MenuBase):
    id: UUID


class DishBase(MenuBase):
    price: str


class Dish(DishBase, Menu):
    pass

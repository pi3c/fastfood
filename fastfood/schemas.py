from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str | None

    class Config:
        from_attributes = True


class Menu(MenuBase):
    id: UUID


class MenuRead(Menu):
    submenus_count: int
    dishes_count: int


class SubMenuRead(Menu):
    dishes_count: int


class DishBase(MenuBase):
    price: str


class Dish(DishBase, Menu):
    pass


class Dish_db(MenuBase):
    price: float

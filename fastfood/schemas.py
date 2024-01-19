from decimal import Decimal

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str | None = None


class SubMenuBase(MenuBase):
    pass


class DishBase(MenuBase):
    price: Decimal


class Dish():
    id: int

    class Config:
        orm_mode = True


class SubMenu(SubMenuBase):
    id: int
    # dishes: list[Dish]

    class Config:
        orm_mode = True


class Menu(MenuBase):
    id: int
    # submenus: list[SubMenu]

    class Config:
        orm_mode = True

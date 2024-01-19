from decimal import Decimal
from typing import List, Annotated, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


intpk = Annotated[int, mapped_column(primary_key=True)]
str_25 = Annotated[str, 25]


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = "menu"

    id: Mapped[intpk]
    title: Mapped[str_25]
    description: Mapped[Optional[str]]
    submenus: Mapped[List["SubMenu"]] = relationship()


class SubMenu(Base):
    __tablename__ = "submenu"

    id: Mapped[intpk]
    title: Mapped[str_25]
    description: Mapped[Optional[str]]
    parent_menu: Mapped[int] = mapped_column(ForeignKey("menu.id"))
    dishes: Mapped[List["Dish"]] = relationship()


class Dish(Base):
    __tablename__ = "dish" 

    id: Mapped[intpk]
    title: Mapped[str_25]
    description: Mapped[Optional[str]]
    price: Mapped[Decimal]
    parent_submenu: Mapped[int] = mapped_column(ForeignKey("submenu.id"))

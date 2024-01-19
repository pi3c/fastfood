import uuid
from decimal import Decimal
from typing import Annotated, List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

uuidpk = Annotated[
    int,
    mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    ),
]
str_25 = Annotated[str, 25]


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = "menu"

    id: Mapped[uuidpk]
    title: Mapped[str_25]
    description: Mapped[Optional[str]]
    submenus: Mapped[List["SubMenu"]] = relationship()


class SubMenu(Base):
    __tablename__ = "submenu"

    id: Mapped[uuidpk]
    title: Mapped[str_25]
    description: Mapped[Optional[str]]
    parent_menu: Mapped[UUID] = mapped_column(ForeignKey("menu.id"))
    dishes: Mapped[List["Dish"]] = relationship()


class Dish(Base):
    __tablename__ = "dish"

    id: Mapped[uuidpk]
    title: Mapped[str_25]
    description: Mapped[Optional[str]]
    price: Mapped[Decimal]
    parent_submenu: Mapped[UUID] = mapped_column(ForeignKey("submenu.id"))

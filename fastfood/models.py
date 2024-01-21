import uuid
from typing import Annotated, List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

uuidpk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    ),
]
str_25 = Annotated[str, 25]


class Base(DeclarativeBase):
    id: Mapped[uuidpk]
    title: Mapped[str_25]
    description: Mapped[Optional[str]]


class Menu(Base):
    __tablename__ = "menu"

    submenus: Mapped[List["SubMenu"]] = relationship(
        "SubMenu", backref="menu", lazy='dynamic', cascade="all, delete",
    )


class SubMenu(Base):
    __tablename__ = "submenu"

    parent_menu: Mapped[uuid.UUID] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))
    dishes: Mapped[List["Dish"]] = relationship(
        "Dish", backref="submenu", lazy="dynamic", cascade="all, delete",
    )


class Dish(Base):
    __tablename__ = "dish"

    price: Mapped[float]
    parent_submenu: Mapped[uuid.UUID] = mapped_column(ForeignKey("submenu.id", ondelete="CASCADE"))

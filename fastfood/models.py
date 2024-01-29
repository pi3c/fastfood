import uuid
from copy import deepcopy
from typing import Annotated, List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.util import hybridproperty

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

    def __eq__(self, other):
        classes_match = isinstance(other, self.__class__)
        a, b = deepcopy(self.__dict__), deepcopy(other.__dict__)
        a.pop("_sa_instance_state", None)
        b.pop("_sa_instance_state", None)
        attrs_match = a == b
        return classes_match and attrs_match

    def __ne__(self, other):
        return not self.__eq__(other)


class Menu(Base):
    __tablename__ = "menu"

    submenus: Mapped[List["SubMenu"]] = relationship(
        "SubMenu",
        backref="menu",
        lazy="selectin",
        cascade="all, delete",
    )

    @hybridproperty
    def submenus_count(self):
        return len(self.submenus)

    @hybridproperty
    def dishes_count(self):
        counter = 0
        for sub in self.submenus:
            counter += len(sub.dishes)
        return counter


class SubMenu(Base):
    __tablename__ = "submenu"

    parent_menu: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("menu.id", ondelete="CASCADE")
    )
    dishes: Mapped[List["Dish"]] = relationship(
        "Dish",
        backref="submenu",
        lazy="selectin",
        cascade="all, delete",
    )

    @hybridproperty
    def dishes_count(self):
        return len(self.dishes)


class Dish(Base):
    __tablename__ = "dish"

    price: Mapped[float]
    parent_submenu: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("submenu.id", ondelete="CASCADE")
    )

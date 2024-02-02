from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from fastfood import models, schemas
from fastfood.dbase import get_async_session


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.db = session

    async def get_menus(self):
        query = select(models.Menu)
        menus = await self.db.execute(query)
        return menus.scalars().all()

    async def create_menu_item(self, menu: schemas.MenuBase):
        new_menu = models.Menu(**menu.model_dump())
        self.db.add(new_menu)
        await self.db.commit()
        await self.db.refresh(new_menu)
        return new_menu

    async def get_menu_item(self, menu_id: UUID):
        m = aliased(models.Menu)
        s = aliased(models.SubMenu)
        d = aliased(models.Dish)

        query = (
            select(
                m,
                func.count(distinct(s.id)).label('submenus_count'),
                func.count(distinct(d.id)).label('dishes_count'),
            )
            .join(s, s.parent_menu == m.id, isouter=True)
            .join(d, d.parent_submenu == s.id, isouter=True)
            .group_by(m.id)
            .where(m.id == menu_id)
        )
        menu = await self.db.execute(query)
        menu = menu.scalars().one_or_none()
        if menu is None:
            return None
        return menu

    async def update_menu_item(
        self,
        menu_id: UUID,
        menu: schemas.MenuBase,
    ):
        query = (
            update(models.Menu)
            .where(models.Menu.id == menu_id)
            .values(**menu.model_dump())
        )
        await self.db.execute(query)
        await self.db.commit()
        qr = select(models.Menu).where(models.Menu.id == menu_id)
        updated_menu = await self.db.execute(qr)
        return updated_menu

    async def delete_menu_item(self, menu_id: UUID):
        query = delete(models.Menu).where(models.Menu.id == menu_id)
        await self.db.execute(query)
        await self.db.commit()

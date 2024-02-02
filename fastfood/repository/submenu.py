from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from fastfood import models, schemas
from fastfood.dbase import get_async_session


class SubMenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.db = session

    async def get_submenus(self, menu_id: UUID):
        query = select(models.SubMenu).where(
            models.SubMenu.parent_menu == menu_id,
        )
        submenus = await self.db.execute(query)
        return submenus

    async def create_submenu_item(
        self,
        menu_id: UUID,
        submenu: schemas.MenuBase,
    ):
        new_submenu = models.SubMenu(**submenu.model_dump())
        new_submenu.parent_menu = menu_id
        self.db.add(new_submenu)
        await self.db.commit()
        await self.db.refresh(new_submenu)
        return new_submenu

    async def get_submenu_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ):
        s = aliased(models.SubMenu)
        d = aliased(models.Dish)
        query = (
            select(s, func.count(distinct(d.id)).label("dishes_count"))
            .join(d, s.id == d.parent_submenu, isouter=True)
            .group_by(s.id)
            .where(s.id == submenu_id)
        )
        submenu = await self.db.execute(query)
        submenu = submenu.scalars().one_or_none()
        if submenu is None:
            return None
        return submenu

    async def update_submenu_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu_data: schemas.MenuBase,
    ):
        query = (
            update(models.SubMenu)
            .where(models.SubMenu.id == submenu_id)
            .values(**submenu_data.model_dump())
        )
        await self.db.execute(query)
        await self.db.commit()
        qr = select(models.SubMenu).where(models.SubMenu.id == submenu_id)
        updated_submenu = await self.db.execute(qr)
        return updated_submenu

    async def delete_submenu_item(self, menu_id: UUID, submenu_id: UUID):
        query = delete(models.SubMenu).where(
            models.SubMenu.id == submenu_id,
        )
        await self.db.execute(query)
        await self.db.commit()

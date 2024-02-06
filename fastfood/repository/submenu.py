from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from fastfood.dbase import get_async_session
from fastfood.models import Dish, SubMenu
from fastfood.schemas import MenuBase


class SubMenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.db = session

    async def get_submenus(self, menu_id: UUID) -> list[SubMenu]:
        query = select(SubMenu).where(
            SubMenu.parent_menu == menu_id,
        )
        submenus = await self.db.execute(query)
        return [x for x in submenus.scalars().all()]

    async def create_submenu_item(
        self,
        menu_id: UUID,
        submenu: MenuBase,
    ) -> SubMenu:
        new_submenu = SubMenu(**submenu.model_dump())
        new_submenu.parent_menu = menu_id
        self.db.add(new_submenu)
        await self.db.commit()
        await self.db.refresh(new_submenu)

        full_sub = await self.get_submenu_item(menu_id, new_submenu.id)
        if full_sub is None:
            raise TypeError
        return full_sub

    async def get_submenu_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> SubMenu | None:
        s = aliased(SubMenu)
        d = aliased(Dish)
        query = (
            select(s, func.count(distinct(d.id)).label('dishes_count'))
            .join(d, s.id == d.parent_submenu, isouter=True)
            .group_by(s.id)
            .where(s.id == submenu_id)
        )
        submenu = await self.db.execute(query)
        submenu = submenu.scalars().one_or_none()
        return submenu

    async def update_submenu_item(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        submenu_data: MenuBase,
    ) -> SubMenu:
        query = (
            update(SubMenu)
            .where(SubMenu.id == submenu_id)
            .values(**submenu_data.model_dump())
        )
        await self.db.execute(query)
        await self.db.commit()
        qr = select(SubMenu).where(SubMenu.id == submenu_id)
        updated_submenu = await self.db.execute(qr)
        return updated_submenu.scalar_one()

    async def delete_submenu_item(self, menu_id: UUID, submenu_id: UUID) -> None:
        query = delete(SubMenu).where(
            SubMenu.id == submenu_id,
        )
        await self.db.execute(query)
        await self.db.commit()

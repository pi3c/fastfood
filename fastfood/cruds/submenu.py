from uuid import UUID

from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from fastfood import models, schemas


class SubMenuCrud:
    @staticmethod
    async def get_submenus(menu_id: UUID, session: AsyncSession):
        async with session:
            query = select(models.SubMenu).where(models.SubMenu.parent_menu == menu_id)
            submenus = await session.execute(query)
        return submenus

    @staticmethod
    async def create_submenu_item(
        menu_id: UUID,
        submenu: schemas.MenuBase,
        session: AsyncSession,
    ):
        async with session:
            new_submenu = models.SubMenu(**submenu.model_dump())
            new_submenu.parent_menu = menu_id
            session.add(new_submenu)
            await session.flush()
            await session.commit()
        return new_submenu

    @staticmethod
    async def get_submenu_item(
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession,
    ):
        async with session:
            s = aliased(models.SubMenu)
            d = aliased(models.Dish)
            query = (
                select(s, func.count(distinct(d.id)))
                .join(d, s.id == d.parent_submenu, isouter=True)
                .group_by(s.id)
                .where(s.id == submenu_id)
            )
            submenu = await session.execute(query)
            submenu = submenu.scalars().one_or_none()
            if submenu is None:
                return None
        return submenu

    @staticmethod
    async def update_submenu_item(
        submenu_id: UUID,
        submenu: schemas.MenuBase,
        session: AsyncSession,
    ):
        async with session:
            query = (
                update(models.SubMenu)
                .where(models.SubMenu.id == submenu_id)
                .values(**submenu.model_dump())
            )
            await session.execute(query)
            await session.commit()
            qr = select(models.SubMenu).where(models.SubMenu.id == submenu_id)
            updated_submenu = await session.execute(qr)
        return updated_submenu

    @staticmethod
    async def delete_submenu_item(submenu_id: UUID, session: AsyncSession):
        async with session:
            query = delete(models.SubMenu).where(models.SubMenu.id == submenu_id)
            await session.execute(query)
            await session.commit()

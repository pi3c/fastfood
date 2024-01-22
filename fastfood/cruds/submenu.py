from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import models, schemas


class SubMenuCrud:
    @staticmethod
    async def get_submenus(menu_id: UUID, session: AsyncSession):
        async with session:
            query = select(models.SubMenu).where(models.SubMenu.parent_menu == menu_id)
            submenus = await session.execute(query)
            return submenus.scalars().all()

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
            query = select(models.SubMenu).where(models.SubMenu.id == submenu_id)
            submenu = await session.execute(query)
            submenu = submenu.scalars().one_or_none()
            if submenu is None:
                return None

            dish_query = (
                select(func.count(models.Dish.id))
                .join(models.SubMenu)
                .filter(models.Dish.parent_submenu == models.SubMenu.id)
            )
            dishes = await session.execute(dish_query)
            submenu.dishes_count = dishes.scalars().one_or_none()

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
            return updated_submenu.scalars().one()

    @staticmethod
    async def delete_submenu_item(submenu_id: UUID, session: AsyncSession):
        async with session:
            query = delete(models.SubMenu).where(models.SubMenu.id == submenu_id)
            await session.execute(query)
            await session.commit()

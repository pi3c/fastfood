from uuid import UUID
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import models, schemas


class MenuCrud:
    @staticmethod
    async def get_menus(session: AsyncSession):
        async with session:
            query = select(models.Menu)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def create_menu_item(menu: schemas.MenuBase, session: AsyncSession):
        async with session:
            new_menu = models.Menu(**menu.model_dump())
            session.add(new_menu)
            await session.commit()
            await session.refresh(new_menu)
            return new_menu

    @staticmethod
    async def get_menu_item(menu_id: UUID, session: AsyncSession):
        async with session:
            query = select(models.Menu).where(models.Menu.id == menu_id)
            menu = await session.execute(query)
            menu = menu.scalars().one_or_none()
            if menu is None:
                return None
            submenu_query = select(func.count(models.SubMenu.id).label("counter")).filter(models.SubMenu.parent_menu == menu_id)
            counter = await session.execute(submenu_query)

            dish_query = (
                select(func.count(models.Dish.id))
                .join(models.SubMenu)
                .filter(models.Dish.parent_submenu == models.SubMenu.id)
                .filter(models.SubMenu.parent_menu == menu_id)
            )
            dishes = await session.execute(dish_query)
            menu.submenus_count = counter.scalars().one_or_none()
            menu.dishes_count = dishes.scalars().one_or_none()
            return menu

    @staticmethod
    async def update_menu_item(menu_id: UUID,
                               menu: schemas.MenuBase,
                               session: AsyncSession,
                               ):
        async with session:
            query = update(models.Menu).where(models.Menu.id == menu_id).values(**menu.model_dump())
            await session.execute(query)
            await session.commit()
            qr = select(models.Menu).where(models.Menu.id == menu_id)
            updated_menu = await session.execute(qr)
            return updated_menu.scalars().one()

    @staticmethod
    async def delete_menu_item(menu_id: UUID, session: AsyncSession):
        async with session:
            query = delete(models.Menu).where(models.Menu.id == menu_id)
            await session.execute(query)
            await session.commit()



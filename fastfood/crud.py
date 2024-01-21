from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import models, schemas
from fastfood.dbase import async_engine


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


class Crud:
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
            return menu.scalars().one_or_none()

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

    @staticmethod
    async def get_submenus(menu_id: UUID, session: AsyncSession):
        async with session:
            query = select(models.SubMenu).where(models.SubMenu.parent_menu == menu_id)
            submenus = await session.execute(query)
            return submenus.scalars().all()

    @staticmethod
    async def create_submenu_item(
        menu_id: UUID, submenu: schemas.MenuBase, session: AsyncSession,
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
        menu_id: UUID, submenu_id: UUID, session: AsyncSession,
    ):
        async with session:
            query = select(models.SubMenu).where(models.SubMenu.id == submenu_id)
            submenu = await session.execute(query)
            return submenu.scalars().one_or_none()

    @staticmethod
    async def update_submenu_item(
        submenu_id: UUID,
        submenu: schemas.MenuBase,
        session: AsyncSession,
    ):
        async with session:
            query = update(models.SubMenu).where(models.SubMenu.id == submenu_id).values(**submenu.model_dump())
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

    @staticmethod
    async def get_dishes(submenu_id: UUID, session: AsyncSession):
        async with session:
            query = select(models.Dish).where(models.Dish.parent_submenu == submenu_id)
            dishes = await session.execute(query)
            return dishes.scalars().all()

    @staticmethod
    async def create_dish_item(
        submenu_id: UUID, dish: schemas.DishBase, session: AsyncSession,
    ):
        async with session:
            new_dish = models.Dish(**dish.model_dump())
            new_dish.parent_submenu = submenu_id
            session.add(new_dish)
            await session.flush()
            await session.commit()
            return new_dish

    @staticmethod
    async def get_dish_item(
        dish_id: UUID, session: AsyncSession,
    ):
        async with session:
            query = select(models.Dish).where(models.Dish.id == dish_id)
            submenu = await session.execute(query)
            return submenu.scalars().one_or_none()

    @staticmethod
    async def update_dish_item(
        dish_id: UUID,
        dish: schemas.DishBase,
        session: AsyncSession,
    ):
        async with session:
            query = update(models.Dish).where(models.Dish.id == dish_id).values(**dish.model_dump())
            await session.execute(query)
            await session.commit()
            qr = select(models.Dish).where(models.Dish.id == dish_id)
            updated_submenu = await session.execute(qr)
            return updated_submenu.scalars().one()

    @staticmethod
    async def delete_dish_item(dish_id: UUID, session: AsyncSession):
        async with session:
            query = delete(models.Dish).where(models.Dish.id == dish_id)
            await session.execute(query)
            await session.commit()



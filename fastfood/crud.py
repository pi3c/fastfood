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

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import models, schemas
from fastfood.dbase import async_engine, async_session_maker


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
            return result.mappings().all()

    @staticmethod
    async def add_menu(menu: schemas.Menu):
        async with async_session_maker() as session:
            new_menu_item = models.Menu(
                title=menu.title,
                description=menu.description,
            )
            session.add(new_menu_item)
            await session.commit()
            return new_menu_item

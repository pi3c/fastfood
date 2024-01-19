from sqlalchemy import select

from fastfood.dbase import async_session_maker, async_engine
from fastfood import models, schemas


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


class Crud:
    @staticmethod
    async def get_menus():
        async with async_session_maker() as session:
            query = select(models.Menu)
            result = await session.execute(query)
            return result.scalars().all()


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

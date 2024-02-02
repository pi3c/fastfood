from fastfood import models
from fastfood.dbase import async_engine

from .dish import DishRepository
from .menu import MenuRepository
from .submenu import SubMenuRepository


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


class Repository(MenuRepository, SubMenuRepository, DishRepository):
    pass


ropo = Repository()

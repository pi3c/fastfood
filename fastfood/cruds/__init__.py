from fastfood import models
from fastfood.dbase import async_engine
from .menu import MenuCrud
from .submenu import SubMenuCrud
from .dish import DishCrud


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


class Crud(MenuCrud, SubMenuCrud, DishCrud):
    pass


crud = Crud()

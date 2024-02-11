import os
import pickle
from uuid import UUID

import openpyxl
import redis.asyncio as redis  # type: ignore
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastfood.config import settings
from fastfood.models import Dish, Menu, SubMenu

file = os.path.join(os.path.curdir, 'admin', 'Menu.xlsx')

redis = redis.Redis.from_url(url=settings.REDIS_URL)

async_engine = create_async_engine(settings.DATABASE_URL_asyncpg)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def refresh_cache(disconts: dict) -> None:
    """Очищает кэш при обновлении БД и ставит отметку времени обновления
    и сохраняет данные скидок на товар
    """
    await redis.flushall()

    for key in disconts.keys():
        await redis.set(f'DISCONT:{str(key)}', pickle.dumps(disconts[key]))

    await redis.set('XLSX_MOD_TIME', pickle.dumps(os.path.getmtime(file)))


async def is_changed_xls() -> bool:
    """Проверяет, изменен ли файл с последнего запуска таска."""
    if not os.path.exists(file):
        return False

    mod_time = os.path.getmtime(file)
    cached_time = await redis.get('XLSX_MOD_TIME')

    if cached_time is not None:
        cached_time = pickle.loads(cached_time)

    if mod_time == cached_time:
        return False

    return True


async def xlsx_to_dict() -> dict:
    """Парсит Menu.xlsx в словарь"""
    wb = openpyxl.load_workbook(file).worksheets[0]

    data = {}

    menu = None
    submenu = None
    dish = None

    for row in wb.iter_rows(values_only=True):
        if row[0] is not None:
            menu = row[0]
            data[menu] = {
                'id': None,
                'title': row[1],
                'description': row[2],
                'submenus': dict(),
            }
        elif row[1] is not None:
            submenu = row[1]
            data[menu]['submenus'][submenu] = {
                'id': None,
                'title': row[2],
                'description': row[3],
                'dishes': dict(),
            }
        elif row[2] is not None:
            dish = row[2]
            data[menu]['submenus'][submenu]['dishes'][dish] = {
                'id': None,
                'title': row[3],
                'description': row[4],
                'price': row[5],
                'discont': row[6],
            }
    return data


async def refresh_all_data(data: dict) -> dict[UUID, int | float]:
    """Удаляет старые данные и сохраняет новые.
    Создает и возвращает список со скидками с привязкой по UUID товара
    """

    disconts = {}

    async with async_session_maker() as session:
        await session.execute(delete(Menu))
        await session.commit()

        for menu_key in data.keys():
            menu = Menu(
                title=data[menu_key].get('title'),
                description=data[menu_key].get('description'),
            )
            session.add(menu)
            await session.flush()

            submenus = data[menu_key]['submenus']
            for sub_key in submenus.keys():
                submenu = SubMenu(
                    title=submenus[sub_key]['title'],
                    description=submenus[sub_key]['description'],
                    parent_menu=menu.id,
                )
                session.add(submenu)
                await session.flush()

                dishes = data[menu_key]['submenus'][sub_key]['dishes']
                print(dishes)
                for dish_key in dishes.keys():
                    dish = Dish(
                        title=dishes[dish_key]['title'],
                        description=dishes[dish_key]['description'],
                        price=dishes[dish_key]['price'],
                        parent_submenu=submenu.id,
                    )
                    session.add(dish)
                    await session.flush()
                    if dishes[dish_key]['discont'] is not None:
                        disconts[dish.id] = dishes[dish_key]['discont']

        await session.commit()
        return disconts


async def main() -> None:
    """Главная функция фоновой задачи"""
    changed = await is_changed_xls()
    if changed:
        menu_data = await xlsx_to_dict()
        discont_data = await refresh_all_data(menu_data)
        await refresh_cache(discont_data)

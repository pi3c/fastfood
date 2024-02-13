import os
import pickle

import redis.asyncio as redis  # type: ignore
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastfood.config import settings
from fastfood.models import Dish, Menu, SubMenu

from .parser import file, gsheets_to_rows, local_xlsx_to_rows, rows_to_dict

redis = redis.Redis.from_url(url=settings.REDIS_URL)

async_engine = create_async_engine(settings.DATABASE_URL_asyncpg)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def clear_cache(pattern: str) -> None:
    keys = [key async for key in redis.scan_iter(pattern)]
    if keys:
        await redis.delete(*keys)


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


async def on_menu_change(new_menu: dict, old_menu: dict, session: AsyncSession) -> dict:
    """Изменение, удаление или создание меню"""
    if new_menu and not old_menu:
        # Создаем меню
        menu = Menu(
            title=new_menu['data']['title'],
            description=new_menu['data']['description'],
        )
        session.add(menu)
        await session.flush()
        new_menu['id'] = str(menu.id)

    elif new_menu and old_menu:
        # Обновляем меню
        await session.execute(
            update(Menu).where(Menu.id == old_menu['id']).values(**(new_menu['data']))
        )
        new_menu['id'] = old_menu['id']

    else:
        # Удаляем меню
        await session.execute(delete(Menu).where(Menu.id == old_menu['id']))

    await session.commit()
    return new_menu


async def menus_updater(menus: dict, session: AsyncSession) -> None:
    """Проверяет пункты меню на изменения
    При необходимости запускае обновление БД
    через фенкцию on_menu_change
    """
    cached_menus = await redis.get('ALL_MENUS')

    if cached_menus is not None:
        cached_menus = pickle.loads(cached_menus)
    else:
        cached_menus = {}

    for key in menus.keys():
        if key not in cached_menus.keys():
            # Создание меню
            menu = await on_menu_change(menus[key], {}, session)
            menus[key] = menu
        elif key in cached_menus.keys():
            # Обновление меню
            if menus[key].get('data') != cached_menus[key].get('data'):
                menu = await on_menu_change(menus[key], cached_menus[key], session)
                menus[key] = menu
            else:
                menus[key]['id'] = cached_menus[key]['id']

    for key in {k: cached_menus[k] for k in set(cached_menus) - set(menus)}:
        # Проверяем на удаленные меню
        await on_menu_change({}, cached_menus.pop(key), session)

    await redis.set('ALL_MENUS', pickle.dumps(menus))


async def on_submenu_change(
    new_sub: dict, old_sub: dict, session: AsyncSession
) -> dict:
    if new_sub and not old_sub:
        # Создаем подменю
        submenu = SubMenu(
            title=new_sub['data']['title'],
            description=new_sub['data']['description'],
        )
        submenu.parent_menu = new_sub['parent_menu']

        session.add(submenu)
        await session.flush()
        new_sub['id'] = str(submenu.id)
        new_sub['parent_menu'] = str(submenu.parent_menu)

    elif new_sub and old_sub:
        # Обновляем подменю
        await session.execute(
            update(SubMenu)
            .where(SubMenu.id == old_sub['id'])
            .values(**(new_sub['data']))
        )
        new_sub['id'] = old_sub['id']
        new_sub['parent_menu'] = old_sub['parent_menu']

    else:
        # Удаляем подменю
        await session.execute(delete(SubMenu).where(SubMenu.id == old_sub['id']))

    await session.commit()
    return new_sub


async def submenus_updater(submenus: dict, session: AsyncSession) -> None:
    """Проверяет пункты подменю на изменения
    При необходимости запускае обновление БД
    """
    # Получаем меню из кэша для получения их ID по померу в таблице
    cached_menus = await redis.get('ALL_MENUS')
    if cached_menus is not None:
        cached_menus = pickle.loads(cached_menus)
    else:
        cached_menus = {}

    # Получаем подмен из кэша
    cached_sub = await redis.get('ALL_SUBMENUS')

    if cached_sub is not None:
        cached_sub = pickle.loads(cached_sub)
    else:
        cached_sub = {}

    for key in submenus.keys():
        parent = cached_menus[submenus[key]['parent_num']]['id']
        submenus[key]['parent_menu'] = parent

        if key not in cached_sub.keys():
            # Получаем и ставим UUID parent_menu
            submenus[key]['parent_menu'] = parent

            submenu = await on_submenu_change(submenus[key], {}, session)
            submenus[key] = submenu
        elif key in cached_sub.keys():
            # Обновление меню
            if submenus[key].get('data') != cached_sub[key].get('data'):
                submenu = await on_submenu_change(
                    submenus[key], cached_sub[key], session
                )
                submenus[key] = submenu
            else:
                submenus[key]['id'] = cached_sub[key]['id']
                submenus[key]['parent_menu'] = cached_sub[key]['parent_menu']

    for key in {k: cached_sub[k] for k in set(cached_sub) - set(submenus)}:
        # Проверяем на удаленные меню
        await on_submenu_change({}, cached_sub.pop(key), session)

    await redis.set('ALL_SUBMENUS', pickle.dumps(submenus))


async def on_dish_change(new_dish: dict, old_dish, session: AsyncSession) -> dict:
    if new_dish and not old_dish:
        dish = Dish(
            title=new_dish['data']['title'],
            description=new_dish['data']['description'],
            price=new_dish['data']['price'],
        )
        dish.parent_submenu = new_dish['parent_submenu']

        session.add(dish)
        await session.flush()
        new_dish['id'] = str(dish.id)
        new_dish['parent_submenu'] = str(dish.parent_submenu)
        new_dish['data']['price'] = str(dish.price)
    elif new_dish and old_dish:
        # Обновляем блюдо
        await session.execute(
            update(Dish).where(Dish.id == old_dish['id']).values(**(new_dish['data']))
        )
        new_dish['id'] = old_dish['id']
        new_dish['parent_submenu'] = old_dish['parent_submenu']
        new_dish['data']['price'] = old_dish['data']['price']

    else:
        # Удаляем блюдо
        await session.execute(delete(Dish).where(Dish.id == old_dish['id']))

    await session.commit()
    return new_dish


async def dishes_updater(dishes: dict, session: AsyncSession) -> None:
    """Проверяет блюда на изменения
    При необходимости запускае обновление БД
    """
    cached_submenus = await redis.get('ALL_SUBMENUS')
    if cached_submenus is not None:
        cached_submenus = pickle.loads(cached_submenus)
    else:
        cached_submenus = {}

    # Получаем блюда из кэша
    cached_dishes = await redis.get('ALL_DISHES')

    if cached_dishes is not None:
        cached_dishes = pickle.loads(cached_dishes)
    else:
        cached_dishes = {}

    await clear_cache('DISCONT*')

    for key in {k: cached_dishes[k] for k in set(cached_dishes) - set(dishes)}:
        # Проверяем на удаленные блюда и обновляемся
        await on_dish_change({}, cached_dishes.pop(key), session)

    for key in dishes.keys():
        parent = cached_submenus[dishes[key]['parent_num']]['id']
        dishes[key]['parent_submenu'] = parent

        if key not in cached_dishes.keys():
            # Получаем и ставим UUID parent_submenu
            dishes[key]['parent_submenu'] = parent

            dish = await on_dish_change(dishes[key], {}, session)
            dishes[key] = dish
        elif key in cached_dishes.keys():
            # Обновление блюда
            if dishes[key].get('data') != cached_dishes[key].get('data'):
                dish = await on_dish_change(dishes[key], cached_dishes[key], session)
                dishes[key] = dish
            else:
                dishes[key]['id'] = cached_dishes[key]['id']
                dishes[key]['parent_submenu'] = cached_dishes[key]['parent_submenu']

        if dishes[key]['discont'] is not None:
            await redis.set(
                f"DISCONT:{dishes[key]['id']}", pickle.dumps(dishes[key]['discont'])
            )

    await redis.set('ALL_DISHES', pickle.dumps(dishes))


async def updater(rows) -> None:
    menus, submenus, dishes = await rows_to_dict(rows)
    async with async_session_maker() as session:
        await menus_updater(menus, session)
        await submenus_updater(submenus, session)
        await dishes_updater(dishes, session)
    # Чистим кэш
    await clear_cache('MENUS*')
    await clear_cache('summary')


async def main() -> None:
    """Главная функция фоновой задачи"""
    changed = await is_changed_xls()
    if changed:
        rows = await local_xlsx_to_rows()
        await updater(rows)


async def main_gsheets() -> None:
    """Главная функция фоновой задачи для работы с Google"""
    rows = await gsheets_to_rows()
    await updater(rows)

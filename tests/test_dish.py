import pytest
from httpx import AsyncClient

from .repository import Repository as Repo


@pytest.mark.asyncio
async def test_dishes_get_all(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        'title': 'Menu',
        'description': 'main menu',
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Проверяем все блюда в подменю
    code, rspn = await Repo.Dish.read_all(client, menu, submenu)
    assert code == 200
    assert rspn == []

    # Добавляем блюдо
    dish = {
        'title': 'dish',
        'description': 'some dish',
        'price': '12.5',
        'parent_submenu': submenu['id'],
    }
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)
    assert code == 201
    dish.update(rspn)

    code, upd_rspn = await Repo.Dish.read_all(client, menu, submenu)

    assert code == 200

    # удаляем сопутствующее
    await Repo.Dish.delete(client, menu, submenu, dish)
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_dishes_add(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        'title': 'Menu',
        'description': 'main menu',
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Добавляем блюдо
    dish = {
        'title': 'dish',
        'description': 'some dish',
        'price': '12.5',
        'parent_submenu': submenu['id'],
    }
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)
    assert code == 201
    dish.update(rspn)

    # Получаем блюдо
    code, rspn = await Repo.Dish.get(client, menu, submenu, dish)
    assert code == 200
    assert rspn['title'] == dish['title']

    # удаляем сопутствующее
    await Repo.Dish.delete(client, menu, submenu, dish)
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_dishes_update(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        'title': 'Menu',
        'description': 'main menu',
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Добавляем блюдо
    dish = {
        'title': 'dish',
        'description': 'some dish',
        'price': '12.5',
        'parent_submenu': submenu['id'],
    }
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)
    dish.update(rspn)

    # Обновляем блюдо и проверяем
    dish['title'] = 'updated_dish'
    code, rspn = await Repo.Dish.update(client, menu, submenu, dish)
    assert code == 200
    assert dish['title'] == rspn['title']
    dish.update(rspn)

    # удаляем сопутствующее
    await Repo.Dish.delete(client, menu, submenu, dish)
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_dishes_delete(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        'title': 'Menu',
        'description': 'main menu',
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Добавляем блюдо
    dish = {
        'title': 'dish',
        'description': 'some dish',
        'price': '12.5',
        'parent_submenu': submenu['id'],
    }
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)
    dish.update(rspn)

    # Удаляем подменю
    code = await Repo.Dish.delete(client, menu, submenu, dish)
    assert code == 200

    # Проверяем удаленное блюдо
    code, rspn = await Repo.Dish.get(client, menu, submenu, dish)
    assert code == 404

    # удаляем сопутствующее
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)

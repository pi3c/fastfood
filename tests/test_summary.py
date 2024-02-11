import pytest
from httpx import AsyncClient

from .repository import Repository as Repo


@pytest.mark.asyncio
async def test_summary_with_menu(client: AsyncClient) -> None:
    # Проверяем пустое summary
    code, rspn = await Repo.Summary.read_summary(client)
    assert code == 200
    assert rspn == []

    # Создаем меню и проверяем ответ
    menu = {
        'title': 'Menu',
        'description': 'main menu',
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Удалим ненужные ключи, тк в модели они не используются
    del menu['submenus_count']
    del menu['dishes_count']
    menu.__setattr__('submenus', list())

    # Проверяем summary c меню
    code, rspn = await Repo.Summary.read_summary(client)
    assert code == 200
    assert rspn == [menu]

    # удаляем сопутствующее
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_summary_with_submenus(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        'title': 'Menu',
        'description': 'main menu',
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    del menu['submenus_count']
    del menu['dishes_count']
    menu.__setattr__('submenus', list())

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)
    submenu.__setattr__('dishes', list())
    del submenu['dishes_count']
    del submenu['parent_menu']

    menu.__setattr__('submenus', [submenu])

    # Получаем блюдо
    code, rspn = await Repo.Summary.read_summary(client)
    assert code == 200
    assert rspn == [menu]

    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_summary_with_dishes(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        'title': 'Menu',
        'description': 'main menu',
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    del menu['submenus_count']
    del menu['dishes_count']
    menu.__setattr__('submenus', list())

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)
    submenu.__setattr__('dishes', list())
    del submenu['dishes_count']
    del submenu['parent_menu']

    # Добавляем блюдо
    dish = {
        'title': 'dish',
        'description': 'some dish',
        'price': '12.5',
        'parent_submenu': submenu['id'],
    }
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)
    dish.update(rspn)
    del dish['parent_submenu']
    del dish['id']

    submenu.__setattr__('dishes', dish)
    menu.__setattr__('submenus', submenu)

    code, rspn = await Repo.Summary.read_summary(client)
    assert code == 200
    assert rspn == [menu]

    await Repo.Menu.delete(client, menu)

import pytest
from httpx import AsyncClient

from .repository import Repository as Repo


@pytest.mark.asyncio
async def test_01(client: AsyncClient, session_data: dict):
    """Проверяет создание меню"""
    menu = {'title': 'Menu', 'description': 'some_menu_desc'}
    code, rspn = await Repo.Menu.write(client, menu)

    assert code == 201
    code, rspn = await Repo.Menu.get(client, rspn)
    session_data['target_menu_id'] = rspn.get('id')
    session_data['target_menu_title'] = rspn.get('title')
    session_data['target_menu_description'] = rspn.get('description')

    assert code == 200
    assert 'id' in rspn
    assert 'title' in rspn
    assert 'description' in rspn
    assert 'submenus_count' in rspn
    assert 'dishes_count' in rspn
    assert rspn['title'] == menu.get('title')
    assert rspn.get('description') == menu.get('description')


@pytest.mark.asyncio
async def test_02(client: AsyncClient, session_data: dict):
    submenu = {'title': 'Submenu', 'description': 'submenu_descr'}
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }

    code, rspn = await Repo.Submenu.write(client, menu, submenu)

    assert code == 201
    assert 'id' in rspn
    assert 'title' in rspn
    assert 'description' in rspn
    assert 'dishes_count' in rspn
    assert rspn['title'] == submenu.get('title')
    assert rspn.get('description') == submenu.get('description')

    session_data['target_submenu_id'] = rspn.get('id')
    session_data['target_submenu_title'] = rspn.get('title')
    session_data['target_submenu_description'] = rspn.get('description')


@pytest.mark.asyncio
async def test_03_dish1(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    submenu = {
        'id': session_data.get('target_submenu_id'),
        'title': session_data.get('target_submenu_title'),
        'description': session_data.get('target_submenu_description'),
    }
    dish = {'title': 'dish_1', 'description': 'dish 1 descr', 'price': '12.5'}
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)

    assert code == 201
    assert 'id' in rspn
    assert 'title' in rspn
    assert 'description' in rspn
    assert 'price' in rspn
    assert rspn['title'] == dish.get('title')
    assert rspn.get('description') == dish.get('description')
    assert rspn.get('price') == dish.get('price')

    session_data['target_dish_id'] = rspn.get('id')
    session_data['target_dish_title'] = rspn.get('title')
    session_data['target_dish_description'] = rspn.get('description')
    session_data['target_dish_price'] = rspn.get('price')


@pytest.mark.asyncio
async def test_04_dish2(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    submenu = {
        'id': session_data.get('target_submenu_id'),
        'title': session_data.get('target_submenu_title'),
        'description': session_data.get('target_submenu_description'),
    }
    dish = {'title': 'dish_2', 'description': 'dish 2 descr', 'price': '13.5'}
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)

    assert code == 201
    assert 'id' in rspn
    assert 'title' in rspn
    assert 'description' in rspn
    assert 'price' in rspn
    assert rspn['title'] == dish.get('title')
    assert rspn.get('description') == dish.get('description')
    assert rspn.get('price') == dish.get('price')

    session_data['target_dish1_id'] = rspn.get('id')
    session_data['target_dish1_title'] = rspn.get('title')
    session_data['target_dish1_description'] = rspn.get('description')
    session_data['target_dish1_price'] = rspn.get('price')


@pytest.mark.asyncio
async def test_05_check_menu(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    code, rspn = await Repo.Menu.get(client, menu)

    assert code == 200
    assert 'id' in rspn
    assert 'title' in rspn
    assert 'description' in rspn
    assert rspn.get('submenus_count') == 1
    assert rspn.get('dishes_count') == 2


@pytest.mark.asyncio
async def test_06_check_submenu(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    submenu = {
        'id': session_data.get('target_submenu_id'),
        'title': session_data.get('target_submenu_title'),
        'description': session_data.get('target_submenu_description'),
    }
    code, rspn = await Repo.Submenu.get(client, menu, submenu)

    assert code == 200
    assert 'id' in rspn
    assert 'title' in rspn
    assert 'description' in rspn
    assert rspn.get('dishes_count') == 2


@pytest.mark.asyncio
async def test_07_del_submenu(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    submenu = {
        'id': session_data.get('target_submenu_id'),
        'title': session_data.get('target_submenu_title'),
        'description': session_data.get('target_submenu_description'),
    }
    code = await Repo.Submenu.delete(client, menu, submenu)

    assert code == 200


@pytest.mark.asyncio
async def test_07_check_submenus(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    code, rspn = await Repo.Submenu.read_all(client, menu)

    assert code == 200
    assert rspn == []


@pytest.mark.asyncio
async def test_08_check_dishes(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    submenu = {
        'id': session_data.get('target_submenu_id'),
        'title': session_data.get('target_submenu_title'),
        'description': session_data.get('target_submenu_description'),
    }
    code, rspn = await Repo.Dish.read_all(client, menu, submenu)

    assert code == 200
    assert rspn == []


@pytest.mark.asyncio
async def test_09_check_menu(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    code, rspn = await Repo.Menu.get(client, menu)

    assert code == 200
    assert 'id' in rspn
    assert 'title' in rspn
    assert 'description' in rspn
    assert rspn.get('submenus_count') == 0
    assert rspn.get('dishes_count') == 0


@pytest.mark.asyncio
async def test_10_del_menu(client: AsyncClient, session_data: dict):
    menu = {
        'id': session_data.get('target_menu_id'),
        'title': session_data.get('target_menu_title'),
        'description': session_data.get('target_menu_description'),
    }
    code = await Repo.Menu.delete(client, menu)

    assert code == 200


@pytest.mark.asyncio
async def test_11_check_menus(client: AsyncClient, session_data: dict):
    code, rspn = await Repo.Menu.read_all(client)

    assert code == 200
    assert rspn == []

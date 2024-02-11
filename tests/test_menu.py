import pytest
from httpx import AsyncClient

from .repository import Repository as Repo


@pytest.mark.asyncio
async def test_menu_crud_empty(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    code, rspn = await Repo.Menu.read_all(client)
    assert code == 200
    assert rspn == []


@pytest.mark.asyncio
async def test_menu_crud_add(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    data = {'title': 'Menu', 'description': None}
    code, rspn = await Repo.Menu.write(client, data)
    assert code == 201
    assert rspn['title'] == 'Menu'
    assert rspn['description'] is None
    await Repo.Menu.delete(client, rspn)


@pytest.mark.asyncio
async def test_menu_crud_get(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    data = {'title': 'Menu', 'description': None}
    code, rspn = await Repo.Menu.write(client, data)
    code, menu = await Repo.Menu.get(client, {'id': rspn.get('id')})
    assert code == 200
    assert menu['title'] == rspn['title']
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_menu_crud_update(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    data = {'title': 'Menu', 'description': None}
    code, rspn = await Repo.Menu.write(client, data)

    upd_data = {
        'id': rspn.get('id'),
        'title': 'upd Menu',
        'description': '',
    }
    code, upd_rspn = await Repo.Menu.update(client, upd_data)
    assert code == 200
    assert upd_rspn['title'] == 'upd Menu'
    await Repo.Menu.delete(client, upd_rspn)


@pytest.mark.asyncio
async def test_menu_crud_delete(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    data = {'title': 'Menu', 'description': None}
    code, rspn = await Repo.Menu.write(client, data)

    code = await Repo.Menu.delete(client, rspn)
    assert code == 200

    code, rspn = await Repo.Menu.get(client, {'id': rspn.get('id')})
    assert code == 404


@pytest.mark.asyncio
async def test_menu_crud_get_all(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    code, rspn = await Repo.Menu.read_all(client)
    assert code == 200
    assert rspn == []

    data = {'title': 'Menu', 'description': None}
    code, rspn = await Repo.Menu.write(client, data)

    code, upd_rspn = await Repo.Menu.read_all(client)
    assert code == 200
    assert upd_rspn == [rspn]
    await Repo.Menu.delete(client, rspn)

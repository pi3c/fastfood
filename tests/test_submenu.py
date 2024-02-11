import pytest

from .repository import Repository as Repo


@pytest.mark.asyncio
async def test_submenus_get_all(client) -> None:
    # Создаем меню и проверяем ответ
    menu = {'title': 'Menu', 'description': 'main menu'}
    code, rspn = await Repo.Menu.write(client, menu)
    assert code == 201
    menu.update(rspn)

    # Проверяем наличие подменю
    code, rspn = await Repo.Submenu.read_all(client, menu)
    assert code == 200
    assert rspn == []

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Проверяем наличие подменю
    code, upd_rspn = await Repo.Submenu.read_all(client, menu)
    assert code == 200
    assert upd_rspn == [rspn]

    # удаляем сопутствующее
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_submenus_add(client) -> None:
    # Создаем меню и проверяем ответ
    menu = {'title': 'Menu', 'description': 'main menu'}
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        'title': 'Submenu',
        'description': 'submenu',
        'parent_menu': menu['id'],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    assert code == 201
    submenu.update(rspn)

    # удаляем сопутствующее
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_submenus_update(client) -> None:
    # Создаем меню и проверяем ответ
    menu = {'title': 'Menu', 'description': 'main menu'}
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

    # Обновляем подменю и проверяем
    submenu['title'] = 'updated_submenu'
    code, rspn = await Repo.Submenu.update(client, menu, submenu)
    assert code == 200
    assert submenu['title'] == rspn['title']
    submenu.update(rspn)

    # удаляем сопутствующее
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_submenus_delete(client) -> None:
    # Создаем меню и проверяем ответ
    menu = {'title': 'Menu', 'description': 'main menu'}
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

    # Удаляем подменю
    code = await Repo.Submenu.delete(client, menu, submenu)
    assert code == 200

    # Проверяем удаленное подменю
    code, rspn = await Repo.Submenu.get(client, menu, submenu)
    assert code == 404

    # удаляем сопутствующее
    await Repo.Menu.delete(client, menu)

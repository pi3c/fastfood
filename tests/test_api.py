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
    data = {"title": "Menu", "description": None}
    code, rspn = await Repo.Menu.write(client, data)
    assert code == 201
    assert rspn["title"] == "Menu"
    assert rspn["description"] is None
    await Repo.Menu.delete(client, rspn)


@pytest.mark.asyncio
async def test_menu_crud_get(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    data = {"title": "Menu", "description": None}
    code, rspn = await Repo.Menu.write(client, data)
    code, menu = await Repo.Menu.get(client, {"id": rspn.get("id")})
    assert code == 200
    assert menu["title"] == rspn["title"]
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_menu_crud_update(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    data = {"title": "Menu", "description": None}
    code, rspn = await Repo.Menu.write(client, data)

    upd_data = {
        "id": rspn.get("id"),
        "title": "upd Menu",
        "description": "",
    }
    code, upd_rspn = await Repo.Menu.update(client, upd_data)
    assert code == 200
    assert upd_rspn["title"] == "upd Menu"
    await Repo.Menu.delete(client, upd_rspn)


@pytest.mark.asyncio
async def test_menu_crud_delete(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    data = {"title": "Menu", "description": None}
    code, rspn = await Repo.Menu.write(client, data)

    code = await Repo.Menu.delete(client, rspn)
    assert code == 200

    code, rspn = await Repo.Menu.get(client, {"id": rspn.get("id")})
    assert code == 404


@pytest.mark.asyncio
async def test_menu_crud_get_all(client: AsyncClient) -> None:
    """Тестирование функций меню"""
    code, rspn = await Repo.Menu.read_all(client)
    assert code == 200
    assert rspn == []

    data = {"title": "Menu", "description": None}
    code, rspn = await Repo.Menu.write(client, data)

    code, upd_rspn = await Repo.Menu.read_all(client)
    assert code == 200
    assert upd_rspn == [rspn]
    await Repo.Menu.delete(client, rspn)


@pytest.mark.asyncio
async def test_submenus_get_all(client) -> None:
    # Создаем меню и проверяем ответ
    menu = {"title": "Menu", "description": "main menu"}
    code, rspn = await Repo.Menu.write(client, menu)
    assert code == 201
    menu.update(rspn)

    # Проверяем наличие подменю
    code, rspn = await Repo.Submenu.read_all(client, menu)
    assert code == 200
    assert rspn == []

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
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
    menu = {"title": "Menu", "description": "main menu"}
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
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
    menu = {"title": "Menu", "description": "main menu"}
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Обновляем подменю и проверяем
    submenu["title"] = "updated_submenu"
    code, rspn = await Repo.Submenu.update(client, menu, submenu)
    assert code == 200
    assert submenu["title"] == rspn["title"]
    submenu.update(rspn)

    # удаляем сопутствующее
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_submenus_delete(client) -> None:
    # Создаем меню и проверяем ответ
    menu = {"title": "Menu", "description": "main menu"}
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
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


@pytest.mark.asyncio
async def test_dishes_get_all(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        "title": "Menu",
        "description": "main menu",
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Проверяем все блюда в подменю
    code, rspn = await Repo.Dish.read_all(client, menu, submenu)
    assert code == 200
    assert rspn == []

    # Добавляем блюдо
    dish = {
        "title": "dish",
        "description": "some dish",
        "price": "12.5",
        "parent_submenu": submenu["id"],
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
        "title": "Menu",
        "description": "main menu",
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Добавляем блюдо
    dish = {
        "title": "dish",
        "description": "some dish",
        "price": "12.5",
        "parent_submenu": submenu["id"],
    }
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)
    assert code == 201
    dish.update(rspn)

    # Получаем блюдо
    code, rspn = await Repo.Dish.get(client, menu, submenu, dish)
    assert code == 200
    assert rspn["title"] == dish["title"]

    # удаляем сопутствующее
    await Repo.Dish.delete(client, menu, submenu, dish)
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_dishes_update(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        "title": "Menu",
        "description": "main menu",
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Добавляем блюдо
    dish = {
        "title": "dish",
        "description": "some dish",
        "price": "12.5",
        "parent_submenu": submenu["id"],
    }
    code, rspn = await Repo.Dish.write(client, menu, submenu, dish)
    dish.update(rspn)

    # Обновляем блюдо и проверяем
    dish["title"] = "updated_dish"
    code, rspn = await Repo.Dish.update(client, menu, submenu, dish)
    assert code == 200
    assert dish["title"] == rspn["title"]
    dish.update(rspn)

    # удаляем сопутствующее
    await Repo.Dish.delete(client, menu, submenu, dish)
    await Repo.Submenu.delete(client, menu, submenu)
    await Repo.Menu.delete(client, menu)


@pytest.mark.asyncio
async def test_dishes_delete(client: AsyncClient) -> None:
    # Создаем меню и проверяем ответ
    menu = {
        "title": "Menu",
        "description": "main menu",
    }
    code, rspn = await Repo.Menu.write(client, menu)
    menu.update(rspn)

    # Создаем и проверяем подменю
    submenu = {
        "title": "Submenu",
        "description": "submenu",
        "parent_menu": menu["id"],
    }
    code, rspn = await Repo.Submenu.write(client, menu, submenu)
    submenu.update(rspn)

    # Добавляем блюдо
    dish = {
        "title": "dish",
        "description": "some dish",
        "price": "12.5",
        "parent_submenu": submenu["id"],
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

from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood.cruds.menu import MenuCrud
from fastfood.cruds.submenu import SubMenuCrud
from fastfood.models import Dish, Menu, SubMenu
from fastfood.schemas import Menu as menuschema
from fastfood.schemas import MenuBase as menubaseschema


@pytest.mark.asyncio
async def test_menu(asession: AsyncSession) -> None:
    async with asession:
        menu: Menu = Menu(title="SomeMenu", description="SomeDescription")

        menu: Menu = await MenuCrud.create_menu_item(
            menubaseschema.model_validate(menu),
            asession,
        )

        menu_id: UUID = menu.id

        req_menu: Menu | None = await MenuCrud.get_menu_item(menu_id, asession)
        assert menu == req_menu

        req_menus = await MenuCrud.get_menus(asession)
        assert menu == req_menus.scalars().all()[0]

        menu.title = "updatedMenu"
        await MenuCrud.update_menu_item(
            menu.id, menuschema.model_validate(menu), asession
        )
        req_menu = await MenuCrud.get_menu_item(menu_id, asession)
        assert menu == req_menu

        await MenuCrud.delete_menu_item(menu_id, asession)
        req_menus = await MenuCrud.get_menus(asession)
        assert req_menus.all() == []


@pytest.mark.asyncio
async def test_submenu(asession: AsyncSession) -> None:
    async with asession:
        # Создаем меню напрямую
        menu: Menu = Menu(title="SomeMenu", description="SomeDescription")
        asession.add(menu)
        await asession.commit()
        await asession.refresh(menu)
        menu_id: UUID = menu.id

        # Создаем подменю через ручку
        submenu: SubMenu = SubMenu(
            title="submenu",
            description="",
            parent_menu=menu_id,
        )
        submenu = await SubMenuCrud.create_submenu_item(
            menu_id,
            menubaseschema.model_validate(submenu),
            asession,
        )


@pytest.mark.asyncio
async def test_dish(asession: AsyncSession):
    async with asession:
        pass

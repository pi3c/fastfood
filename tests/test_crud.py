from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastfood.cruds.submenu import SubMenuCrud
from fastfood.models import Menu, SubMenu, Dish
from fastfood.cruds.menu import MenuCrud
from fastfood.schemas import Menu as menuschema
from fastfood.schemas import SubMenuRead as submenuschema
from fastfood.schemas import MenuBase as menubaseschema
import pytest


@pytest.mark.asyncio
async def test_menu(asession: AsyncSession) -> None:
    async with asession:
        menu: Menu = Menu(title="SomeMenu", description="SomeDescription")
        asession.add(menu)

        await asession.commit()
        await asession.refresh(menu)
        menu_id: UUID = menu.id

        req_menu: Menu | None = await MenuCrud.get_menu_item(menu_id, asession)
        assert menu == req_menu

        req_menus = await MenuCrud.get_menus(asession)
        # assert menu == req_menus.first()

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
        menu: Menu = Menu(title="SomeMenu", description="SomeDescription")
        asession.add(menu)

        await asession.commit()
        await asession.refresh(menu)
        menu_id: UUID = menu.id
        submenu: SubMenu = SubMenu(
            title="submenu", description="", parent_menu=menu_id,
        )
        submenu = await SubMenuCrud.create_submenu_item(
            menu_id, menubaseschema.model_validate(submenu), asession,
        )

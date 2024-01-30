from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood.cruds.menu import MenuCrud
from fastfood.cruds.submenu import SubMenuCrud
from fastfood.models import Menu, SubMenu
from fastfood.schemas import Menu as menuschema
from fastfood.schemas import MenuBase as menubaseschema


@pytest.mark.asyncio
async def test_menu(asession: AsyncSession) -> None:
    async with asession:
        # Создаем меню
        menu: Menu = Menu(title="SomeMenu", description="SomeDescription")
        menu: Menu = await MenuCrud.create_menu_item(
            menubaseschema.model_validate(menu),
            asession,
        )
        menu_id: UUID = menu.id

        # Получаем его же
        req_menu: Menu | None = await MenuCrud.get_menu_item(menu_id, asession)
        assert menu == req_menu

        # Получаем все меню и проверяем
        req_menus = await MenuCrud.get_menus(asession)
        assert menu == req_menus.scalars().all()[0]

        # Обновляем
        menu.title = "updatedMenu"
        await MenuCrud.update_menu_item(
            menu.id, menuschema.model_validate(menu), asession
        )
        # И сверяем
        req_menu = await MenuCrud.get_menu_item(menu_id, asession)
        assert menu == req_menu

        # Удаляем и проверяем
        await MenuCrud.delete_menu_item(menu_id, asession)
        req_menus = await MenuCrud.get_menus(asession)
        assert req_menus.all() == []


@pytest.mark.asyncio
async def test_submenu(asession: AsyncSession) -> None:
    async with asession:
        # Создаем меню напрямую
        menu = Menu(title="SomeMenu", description="SomeDescription")
        asession.add(menu)
        await asession.commit()
        await asession.refresh(menu)
        menu_id: UUID = menu.id

        # Создаем подменю
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
        submenu_id = submenu.id

        # Проверяем подменю
        req_submenu = await SubMenuCrud.get_submenu_item(
            menu_id,
            submenu.id,
            asession,
        )
        assert submenu == req_submenu

        # Обновляем меню
        submenu.title = "UpdatedSubmenu"
        req_submenu = await SubMenuCrud.update_submenu_item(
            submenu_id,
            menubaseschema.model_validate(submenu),
            asession,
        )
        assert submenu == req_submenu.scalar_one_or_none()

        menu = await MenuCrud.get_menu_item(menu_id, asession)
        assert 1 == menu.submenus_count

        # Удаляем полменю
        await SubMenuCrud.delete_submenu_item(submenu_id, asession)

        menu = await MenuCrud.get_menu_item(menu_id, asession)
        assert 0 == menu.submenus_count

        await MenuCrud.delete_menu_item(menu_id, asession)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_dish(asession: AsyncSession):
    """Not Implemented yet"""
    async with asession:
        pass

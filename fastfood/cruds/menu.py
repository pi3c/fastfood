from uuid import UUID

from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from fastfood import models, schemas


class MenuCrud:
    @staticmethod
    async def get_menus(session: AsyncSession):
        async with session:
            query = select(models.Menu)
            menus = await session.execute(query)
            return menus

    @staticmethod
    async def create_menu_item(menu: schemas.MenuBase, session: AsyncSession):
        async with session:
            new_menu = models.Menu(**menu.model_dump())
            session.add(new_menu)
            await session.commit()
            await session.refresh(new_menu)
            return new_menu

    @staticmethod
    async def get_menu_item(menu_id: UUID, session: AsyncSession):
        async with session:
            m = aliased(models.Menu)
            s = aliased(models.SubMenu)
            d = aliased(models.Dish)

            query = (
                select(
                    m,
                    func.count(distinct(s.id)).label("submenus_count"),
                    func.count(distinct(d.id)).label("dishes_count")
                )
                .join(s, s.parent_menu == m.id, isouter=True)
                .join(d, d.parent_submenu == s.id, isouter=True)
                .group_by(m.id)
                .where(m.id == menu_id)
            )
            menu = await session.execute(query)
            menu = menu.scalars().one_or_none()
            if menu is None:
                return None
            return menu

    @staticmethod
    async def update_menu_item(
        menu_id: UUID,
        menu: schemas.MenuBase,
        session: AsyncSession,
    ):
        async with session:
            query = (
                update(models.Menu)
                .where(models.Menu.id == menu_id)
                .values(**menu.model_dump())
            )
            await session.execute(query)
            await session.commit()
            qr = select(models.Menu).where(models.Menu.id == menu_id)
            updated_menu = await session.execute(qr)
            return updated_menu

    @staticmethod
    async def delete_menu_item(menu_id: UUID, session: AsyncSession):
        async with session:
            query = delete(models.Menu).where(models.Menu.id == menu_id)
            await session.execute(query)
            await session.commit()

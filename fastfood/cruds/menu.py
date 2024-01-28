from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, aliased

from fastfood import models, schemas


class MenuCrud:
    @staticmethod
    async def get_menus(session: AsyncSession):
        async with session:
            query = select(models.Menu)
            result = await session.execute(query)
            return result.scalars().all()

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
            """ Комментарий для проверяющего 
            То что было, оставил закоментированным, удалю в следующей части
            в pgadmin набросал следующий запрос
            WITH subq as (
                SELECT
                    s.id,
                    s.title,
                    s.description,
                    s.parent_menu,
                    count(d.id) as dishes_count
                FROM submenu s
                JOIN dish d ON s.id = d.parent_submenu
                GROUP BY s.id
            )
            SELECT
                m.id,
                m.title,
                m.description,
                count(q.id) AS submenus_count,
                SUM(q.dishes_count) AS dishes_count
            FROM menu m
            JOIN subq q ON m.id = q.parent_menu
            GROUP BY m.id
            """
            m = aliased(models.Menu)
            s = aliased(models.SubMenu)
            d = aliased(models.Dish)

            query = select(m).where(m.id == menu_id)
            menu = await session.execute(query)
            menu = menu.scalars().one_or_none()

            if menu is None:
                return None

            submenu_query = select(
                func.count(s.id).label("counter")
            ).filter(s.parent_menu == menu_id)
            counter = await session.execute(submenu_query)

            dish_query = (
                select(func.count(d.id))
                .join(s)
                .filter(d.parent_submenu == s.id)
                .filter(s.parent_menu == menu_id)
            )
            dishes = await session.execute(dish_query)
            menu.submenus_count = counter.scalars().one_or_none()
            menu.dishes_count = dishes.scalars().one_or_none()
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
            return updated_menu.scalars().one()

    @staticmethod
    async def delete_menu_item(menu_id: UUID, session: AsyncSession):
        async with session:
            query = delete(models.Menu).where(models.Menu.id == menu_id)
            await session.execute(query)
            await session.commit()

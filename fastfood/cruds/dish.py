from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastfood import models, schemas


class DishCrud:
    @staticmethod
    async def get_dishes(submenu_id: UUID, session: AsyncSession):
        async with session:
            query = select(models.Dish).where(models.Dish.parent_submenu == submenu_id)
            dishes = await session.execute(query)
            return dishes.scalars().all()

    @staticmethod
    async def create_dish_item(
        submenu_id: UUID, dish: schemas.DishBase, session: AsyncSession,
    ):
        async with session:
            new_dish = models.Dish(**dish.model_dump())
            new_dish.parent_submenu = submenu_id
            session.add(new_dish)
            await session.flush()
            await session.commit()
            return new_dish

    @staticmethod
    async def get_dish_item(
        dish_id: UUID, session: AsyncSession,
    ):
        async with session:
            query = select(models.Dish).where(models.Dish.id == dish_id)
            submenu = await session.execute(query)
            return submenu.scalars().one_or_none()

    @staticmethod
    async def update_dish_item(
        dish_id: UUID,
        dish: schemas.DishBase,
        session: AsyncSession,
    ):
        async with session:
            query = update(models.Dish).where(models.Dish.id == dish_id).values(**dish.model_dump())
            await session.execute(query)
            await session.commit()
            qr = select(models.Dish).where(models.Dish.id == dish_id)
            updated_submenu = await session.execute(qr)
            return updated_submenu.scalars().one()

    @staticmethod
    async def delete_dish_item(dish_id: UUID, session: AsyncSession):
        async with session:
            query = delete(models.Dish).where(models.Dish.id == dish_id)
            await session.execute(query)
            await session.commit()



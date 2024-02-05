from uuid import UUID

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.dish import DishRepository
from fastfood.repository.redis import RedisRepository, get_key
from fastfood.schemas import Dish, Dish_db, DishBase


class DishService:
    def __init__(
        self,
        dish_repo: DishRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ) -> None:
        self.dish_repo = dish_repo
        self.cache = RedisRepository(redis_client)
        self.bg_tasks = background_tasks
        self.key = get_key

    async def read_dishes(self, menu_id: UUID, submenu_id: UUID) -> list[Dish]:
        cached_dishes = await self.cache.get(
            self.key('dishes', menu_id=str(menu_id), submenu_id=str(submenu_id))
        )
        if cached_dishes is not None:
            return cached_dishes

        data = await self.dish_repo.get_dishes(menu_id, submenu_id)
        response = []
        for row in data:
            dish = row.__dict__
            dish['price'] = str(dish['price'])
            response.append(Dish(**dish))
        await self.cache.set(
            self.key(
                'dishes',
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
            ),
            response,
            self.bg_tasks,
        )
        return response

    async def create_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_data: DishBase,
    ) -> Dish:
        dish_db = Dish_db(**dish_data.model_dump())
        data = await self.dish_repo.create_dish_item(
            menu_id,
            submenu_id,
            dish_db,
        )
        dish = data.__dict__
        dish['price'] = str(dish['price'])
        dish = Dish(**dish)
        await self.cache.set(
            self.key('dish', menu_id=str(menu_id), submenu_id=str(submenu_id)),
            dish,
            self.bg_tasks,
        )
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)

        return dish

    async def read_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish | None:
        cached_dish = await self.cache.get(
            self.key(
                'dish',
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
                dish_id=str(dish_id),
            )
        )
        if cached_dish is not None:
            return cached_dish

        data = await self.dish_repo.get_dish_item(menu_id, submenu_id, dish_id)
        if data is None:
            return None
        dish = data.__dict__
        dish['price'] = str(dish['price'])
        dish = Dish(**dish)
        await self.cache.set(
            self.key(
                'dish',
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
                dish_id=str(dish_id),
            ),
            dish,
            self.bg_tasks,
        )
        return dish

    async def update_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id, dish_data: DishBase
    ) -> Dish:
        dish_db = Dish_db(**dish_data.model_dump())
        data = await self.dish_repo.update_dish_item(
            menu_id, submenu_id, dish_id, dish_db
        )
        dish = data.__dict__
        dish['price'] = str(dish['price'])
        dish = Dish(**dish)
        await self.cache.set(
            self.key(
                'dish',
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
                dish_id=str(dish_id),
            ),
            dish,
            self.bg_tasks,
        )
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)

        return dish

    async def del_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> int:
        response = await self.dish_repo.delete_dish_item(
            menu_id,
            submenu_id,
            dish_id,
        )
        await self.cache.delete(key=str(menu_id), bg_task=self.bg_tasks)
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)

        return response

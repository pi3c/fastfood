import pickle
from uuid import UUID

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.cruds.menu import MenuCrud
from fastfood.cruds.redis_cache import AsyncRedisCache, get_async_redis_client
from fastfood.schemas import MenuRead


class MenuService:
    def __init__(
        self,
        menu_crud: MenuCrud = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ):
        self.menu_crud = menu_crud
        self.cache_client = AsyncRedisCache(redis_client)
        self.background_tasks = background_tasks

    async def read_menus(self):
        cached = await self.cache_client.get("all")

        if cached:
            return cached

        data = await self.menu_crud.get_menus()
        print("not cached", data)
        await self.cache_client.set("all", data, self.background_tasks)
        return data

    async def create_menu(self, menu_data):
        data = await self.menu_crud.create_menu_item(menu_data)
        await self.cache_client.set(str(data.id), data, self.background_tasks)
        await self.cache_client.clear_after_change(str(data.id), self.background_tasks)
        return data

    async def read_menu(self, menu_id: UUID):
        cached = await self.cache_client.get(str(menu_id))
        if cached is not None:
            return cached

        data = await self.menu_crud.get_menu_item(menu_id)
        await self.cache_client.set(str(menu_id), data, self.background_tasks)
        return data

    async def update_menu(self, menu_id: UUID, menu_data):
        data = await self.menu_crud.update_menu_item(menu_id, menu_data)
        await self.cache_client.set(str(menu_id), data, self.background_tasks)
        await self.cache_client.clear_after_change(str(menu_id), self.background_tasks)
        return data

    # async def del_menu(self, menu_id: int | str):
    #     data = await self.menu_crud.del_menu(menu_id)
    #     await self.cache_client.delete(f'{menu_id}', self.background_tasks)
    #     await self.cache_client.clear_after_change(menu_id, self.background_tasks)
    #     return data
    #
    # async def orm_read_menu(self, menu_id: int | str):
    #     return await self.menu_crud.orm_read_menu(menu_id)
    #
    # async def read_full_menus(self):
    #     menu_data = await self.menu_crud.get_full_menus()
    #     return FullMenuListResponse(menus=menu_data)

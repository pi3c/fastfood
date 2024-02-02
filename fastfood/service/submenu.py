from uuid import UUID

import redis.asyncio as redis
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.redis import RedisRepository
from fastfood.repository.submenu import SubMenuRepository
from fastfood.schemas import MenuBase


class SubmenuService:
    def __init__(
        self,
        submenu_repo: SubMenuRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ):
        self.submenu_repo = submenu_repo
        self.cache_client = RedisRepository(redis_client)
        self.background_tasks = background_tasks

    async def read_submenus(self, menu_id: UUID):
        data = await self.submenu_repo.get_submenus(menu_id=menu_id)
        return data

    async def create_submenu(self, menu_id: UUID, submenu_data: MenuBase):
        data = await self.submenu_repo.create_submenu_item(
            menu_id,
            submenu_data,
        )
        return data

    async def read_menu(self, menu_id: UUID, submenu_id: UUID):
        data = await self.submenu_repo.get_submenu_item(menu_id, submenu_id)
        return data

    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, submenu_data: MenuBase
    ):
        data = await self.submenu_repo.update_submenu_item(
            menu_id, submenu_id, submenu_data
        )
        return data

    async def del_menu(self, menu_id: UUID, submenu_id: UUID):
        data = await self.submenu_repo.delete_submenu_item(menu_id, submenu_id)
        return data

from uuid import UUID

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.redis import RedisRepository
from fastfood.repository.submenu import SubMenuRepository
from fastfood.schemas import MenuBase, SubMenuRead


class SubmenuService:
    def __init__(
        self,
        submenu_repo: SubMenuRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ) -> None:

        self.submenu_repo = submenu_repo
        self.cache_client = RedisRepository(redis_client)
        self.background_tasks = background_tasks

    async def read_submenus(self, menu_id: UUID) -> list[SubMenuRead]:
        data = await self.submenu_repo.get_submenus(menu_id=menu_id)
        submenus = []
        for r in data:
            submenu = r.__dict__
            subq = await self.submenu_repo.get_submenu_item(menu_id, r.id)
            if subq is not None:
                submenu['dishes_count'] = len(subq.dishes)
            submenu = SubMenuRead(**submenu)
            submenus.append(submenu)
        return submenus

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
        return await self.submenu_repo.delete_submenu_item(menu_id, submenu_id)

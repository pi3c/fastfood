from uuid import UUID

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.redis import RedisRepository, get_key
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
        self.cache = RedisRepository(redis_client)
        self.bg_tasks = background_tasks
        self.key = get_key

    async def read_submenus(self, menu_id: UUID) -> list[SubMenuRead]:
        cached_submenus = await self.cache.get(
            self.key('submenus', menu_id=str(menu_id))
        )
        if cached_submenus is not None:
            return cached_submenus

        data = await self.submenu_repo.get_submenus(menu_id=menu_id)
        submenus = []
        for r in data:
            submenu = r.__dict__
            subq = await self.submenu_repo.get_submenu_item(menu_id, r.id)
            if subq is not None:
                submenu['dishes_count'] = len(subq.dishes)
            submenu = SubMenuRead(**submenu)
            submenus.append(submenu)

        await self.cache.set(
            self.key('submenus', menu_id=str(menu_id)), submenus, self.bg_tasks
        )
        return submenus

    async def create_submenu(
        self, menu_id: UUID, submenu_data: MenuBase
    ) -> SubMenuRead:
        data = await self.submenu_repo.create_submenu_item(
            menu_id,
            submenu_data,
        )
        submenu = data.__dict__
        submenu = {k: v for k, v in submenu.items() if not k.startswith('_')}
        submenu['dishes_count'] = len(submenu.pop('dishes'))
        submenu = SubMenuRead(**submenu)
        await self.cache.set(
            self.key('submenu', menu_id=str(menu_id)), submenu, self.bg_tasks
        )
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)

        return submenu

    async def read_menu(self, menu_id: UUID, submenu_id: UUID) -> SubMenuRead | None:
        cached_submenu = await self.cache.get(
            self.key(
                'submenu',
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
            )
        )
        if cached_submenu is not None:
            return cached_submenu

        data = await self.submenu_repo.get_submenu_item(menu_id, submenu_id)
        if data is None:
            return None
        submenu = data.__dict__
        submenu = {k: v for k, v in submenu.items() if not k.startswith('_')}
        submenu['dishes_count'] = len(submenu.pop('dishes'))
        menu = SubMenuRead(**submenu)
        await self.cache.set(
            self.key('submenu', menu_id=str(menu_id), submenu_id=str(submenu_id)),
            submenu,
            self.bg_tasks,
        )
        return menu

    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, submenu_data: MenuBase
    ) -> SubMenuRead | None:
        data = await self.submenu_repo.update_submenu_item(
            menu_id, submenu_id, submenu_data
        )
        if data is None:
            return None

        submenu = data.__dict__
        submenu = {k: v for k, v in submenu.items() if not k.startswith('_')}
        submenu['dishes_count'] = len(submenu.pop('dishes'))
        submenu = SubMenuRead(**submenu)

        await self.cache.set(
            self.key('submenu', menu_id=str(menu_id), submenu_id=str(submenu_id)),
            submenu,
            self.bg_tasks,
        )
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)

        return submenu

    async def del_menu(self, menu_id: UUID, submenu_id: UUID) -> None:
        await self.submenu_repo.delete_submenu_item(menu_id, submenu_id)
        await self.cache.delete(
            key=self.key(
                'submenu',
                menu_id=str(menu_id),
                submenu_id=str(submenu_id),
            ),
            bg_task=self.bg_tasks,
        )
        await self.cache.invalidate(key=str(menu_id), bg_task=self.bg_tasks)

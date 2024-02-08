import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from fastfood.dbase import get_async_redis_client
from fastfood.repository.redis import RedisRepository, get_key
from fastfood.repository.summary import SummaryRepository
from fastfood.schemas import DishBase, MenuSummary, SubMenuSummary


class SummaryService:
    def __init__(
        self,
        sum_repo: SummaryRepository = Depends(),
        redis_client: redis.Redis = Depends(get_async_redis_client),
        background_tasks: BackgroundTasks = None,
    ) -> None:
        self.sum_repo = sum_repo
        self.cache = RedisRepository(redis_client)
        self.key = get_key
        self.bg_tasks = background_tasks

    async def read_data(self):
        def dump_to_schema(schema, obj):
            obj = obj.__dict__
            obj = {k: v for k, v in obj.items() if not k.startswith('_')}
            if 'price' in obj.keys():
                obj['price'] = str(obj['price'])
            return schema(**obj)

        cached_data = await self.cache.get(self.key('summary'))
        if cached_data is not None:
            return cached_data

        result = []
        data = await self.sum_repo.get_data()
        for menu in data:
            menus_res = dump_to_schema(MenuSummary, menu)
            menus_res.submenus = []

            for sub in menu.submenus:
                sub_res = dump_to_schema(SubMenuSummary, sub)
                sub_res.dishes = []

                for dish in sub.dishes:
                    dish_res = dump_to_schema(DishBase, dish)
                    sub_res.dishes.append(dish_res)

                menus_res.submenus.append(sub_res)

            result.append(menus_res)

        await self.cache.set(self.key('summary'), data, self.bg_tasks)

        return result

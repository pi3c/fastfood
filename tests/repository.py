from httpx import AsyncClient, Response

from .urls import reverse_url


class Repository:
    class Menu:
        @staticmethod
        async def read_all(ac: AsyncClient) -> tuple[int, dict]:
            """чтение всех меню"""

            response: Response = await ac.get(reverse_url('menus'))
            return response.status_code, response.json()

        @staticmethod
        async def get(ac: AsyncClient, data: dict) -> tuple[int, dict]:
            """Получение меню по id"""
            response: Response = await ac.get(
                reverse_url('menu', menu_id=data.get('id'))
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(ac: AsyncClient, data: dict) -> tuple[int, dict]:
            """создания меню"""
            response: Response = await ac.post(reverse_url('menus'), json=data)
            return response.status_code, response.json()

        @staticmethod
        async def update(ac: AsyncClient, data: dict) -> tuple[int, dict]:
            """Обновление меню по id"""
            response: Response = await ac.patch(
                reverse_url('menu', menu_id=data.get('id')),
                json=data,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac: AsyncClient, data: dict) -> int:
            """Удаление меню по id"""
            response: Response = await ac.delete(
                reverse_url('menu', menu_id=data.get('id')),
            )
            return response.status_code

    class Submenu:
        @staticmethod
        async def read_all(ac: AsyncClient, menu: dict) -> tuple[int, dict]:
            """чтение всех меню"""
            response: Response = await ac.get(
                reverse_url('submenus', menu_id=menu.get('id')),
            )
            return response.status_code, response.json()

        @staticmethod
        async def get(
            ac: AsyncClient,
            menu: dict,
            submenu: dict,
        ) -> tuple[int, dict]:
            """Получение меню по id"""
            response: Response = await ac.get(
                reverse_url(
                    'submenu',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                ),
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(
            ac: AsyncClient,
            menu: dict,
            submenu: dict,
        ) -> tuple[int, dict]:
            """создания меню"""
            response: Response = await ac.post(
                reverse_url('submenu', menu_id=menu.get('id')),
                json=submenu,
            )
            return response.status_code, response.json()

        @staticmethod
        async def update(
            ac: AsyncClient, menu: dict, submenu: dict
        ) -> tuple[int, dict]:
            """Обновление меню по id"""
            response: Response = await ac.patch(
                reverse_url(
                    'submenu',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                ),
                json=submenu,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac: AsyncClient, menu: dict, submenu: dict) -> int:
            """Удаление меню по id"""
            response: Response = await ac.delete(
                reverse_url(
                    'submenu',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                ),
            )
            return response.status_code

    class Dish:
        @staticmethod
        async def read_all(
            ac: AsyncClient, menu: dict, submenu: dict
        ) -> tuple[int, dict]:
            """чтение всех блюд"""
            response: Response = await ac.get(
                reverse_url(
                    'dishes',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                ),
            )
            return response.status_code, response.json()

        @staticmethod
        async def get(
            ac: AsyncClient, menu: dict, submenu: dict, dish: dict
        ) -> tuple[int, dict]:
            """Получение блюда по id"""
            response: Response = await ac.get(
                reverse_url(
                    'dish',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                    dish_id=dish.get('id'),
                ),
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(
            ac: AsyncClient, menu: dict, submenu: dict, dish: dict
        ) -> tuple[int, dict]:
            """создания блюда"""
            response: Response = await ac.post(
                reverse_url(
                    'dishes',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                ),
                json=dish,
            )
            return response.status_code, response.json()

        @staticmethod
        async def update(
            ac: AsyncClient, menu: dict, submenu: dict, dish: dict
        ) -> tuple[int, dict]:
            """Обновление блюда по id"""
            response: Response = await ac.patch(
                reverse_url(
                    'dish',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                    dish_id=dish.get('id'),
                ),
                json=dish,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(
            ac: AsyncClient,
            menu: dict,
            submenu: dict,
            dish: dict,
        ) -> int:
            """Удаление блюда по id"""
            response: Response = await ac.delete(
                reverse_url(
                    'dish',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                    dish_id=dish.get('id'),
                ),
            )
            return response.status_code

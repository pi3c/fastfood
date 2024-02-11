from httpx import AsyncClient, Response

from .urls import reverse


class Repository:
    class Menu:
        @staticmethod
        async def read_all(ac: AsyncClient) -> tuple[int, dict]:
            """чтение всех меню"""

            response: Response = await ac.get(reverse('get_menus'))
            return response.status_code, response.json()

        @staticmethod
        async def get(ac: AsyncClient, data: dict) -> tuple[int, dict]:
            """Получение меню по id"""
            response: Response = await ac.get(
                reverse('get_menu', menu_id=data.get('id'))
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(ac: AsyncClient, data: dict) -> tuple[int, dict]:
            """создания меню"""
            response: Response = await ac.post(reverse('add_menu'), json=data)
            return response.status_code, response.json()

        @staticmethod
        async def update(ac: AsyncClient, data: dict) -> tuple[int, dict]:
            """Обновление меню по id"""
            response: Response = await ac.patch(
                reverse('update_menu', menu_id=data.get('id')),
                json=data,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac: AsyncClient, data: dict) -> int:
            """Удаление меню по id"""
            response: Response = await ac.delete(
                reverse('delete_menu', menu_id=data.get('id')),
            )
            return response.status_code

    class Submenu:
        @staticmethod
        async def read_all(ac: AsyncClient, menu: dict) -> tuple[int, dict]:
            """чтение всех меню"""
            response: Response = await ac.get(
                reverse('get_submenus', menu_id=menu.get('id')),
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
                reverse(
                    'get_submenu',
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
                reverse('create_submenu_item', menu_id=menu.get('id')),
                json=submenu,
            )
            return response.status_code, response.json()

        @staticmethod
        async def update(
            ac: AsyncClient, menu: dict, submenu: dict
        ) -> tuple[int, dict]:
            """Обновление меню по id"""
            response: Response = await ac.patch(
                reverse(
                    'update_submenu',
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
                reverse(
                    'delete_submenu',
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
                reverse(
                    'get_dishes',
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
                reverse(
                    'get_dish',
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
                reverse(
                    'create_dish',
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
                reverse(
                    'update_dish',
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
                reverse(
                    'delete_dish',
                    menu_id=menu.get('id'),
                    submenu_id=submenu.get('id'),
                    dish_id=dish.get('id'),
                ),
            )
            return response.status_code

    class Summary:
        @staticmethod
        async def read_summary(ac: AsyncClient) -> tuple[int, dict]:
            """чтение summary"""

            response: Response = await ac.get(reverse('get_summary'))
            return response.status_code, response.json()

from typing import Tuple

from httpx import AsyncClient, Response


class Repository:
    class Menu:
        @staticmethod
        async def read_all(ac: AsyncClient) -> Tuple[int, dict]:
            """чтение всех меню"""

            response: Response = await ac.get("/")
            return response.status_code, response.json()

        @staticmethod
        async def get(ac: AsyncClient, data: dict) -> Tuple[int, dict]:
            """Получение меню по id"""
            response: Response = await ac.get(f"/{data.get('id')}")
            return response.status_code, response.json()

        @staticmethod
        async def write(ac: AsyncClient, data: dict) -> Tuple[int, dict]:
            """создания меню"""
            response: Response = await ac.post("/", json=data)
            return response.status_code, response.json()

        @staticmethod
        async def update(ac: AsyncClient, data: dict) -> Tuple[int, dict]:
            """Обновление меню по id"""
            response: Response = await ac.patch(
                f"/{data.get('id')}",
                json=data,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac: AsyncClient, data: dict) -> int:
            """Удаление меню по id"""
            response: Response = await ac.delete(f"/{data.get('id')}")
            return response.status_code

    class Submenu:
        @staticmethod
        async def read_all(ac: AsyncClient, menu: dict) -> Tuple[int, dict]:
            """чтение всех меню"""
            response: Response = await ac.get(f"/{menu.get('id')}/submenus/")
            return response.status_code, response.json()

        @staticmethod
        async def get(
            ac: AsyncClient,
            menu: dict,
            submenu: dict,
        ) -> Tuple[int, dict]:
            """Получение меню по id"""
            response: Response = await ac.get(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}",
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(
            ac: AsyncClient,
            menu: dict,
            submenu: dict,
        ) -> Tuple[int, dict]:
            """создания меню"""
            response: Response = await ac.post(
                f"/{menu.get('id')}/submenus/",
                json=submenu,
            )
            return response.status_code, response.json()

        @staticmethod
        async def update(
            ac: AsyncClient, menu: dict, submenu: dict
        ) -> Tuple[int, dict]:
            """Обновление меню по id"""
            response: Response = await ac.patch(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}",
                json=submenu,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac: AsyncClient, menu: dict, submenu: dict) -> int:
            """Удаление меню по id"""
            response: Response = await ac.delete(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}"
            )
            return response.status_code

    class Dish:
        @staticmethod
        async def read_all(
            ac: AsyncClient, menu: dict, submenu: dict
        ) -> Tuple[int, dict]:
            """чтение всех блюд"""
            response: Response = await ac.get(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}/dishes/",
            )
            return response.status_code, response.json()

        @staticmethod
        async def get(
            ac: AsyncClient, menu: dict, submenu: dict, dish: dict
        ) -> Tuple[int, dict]:
            """Получение блюда по id"""
            response: Response = await ac.get(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}"
                f"/dishes/{dish.get('id')}",
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(
            ac: AsyncClient, menu: dict, submenu: dict, dish: dict
        ) -> Tuple[int, dict]:
            """создания блюда"""
            response: Response = await ac.post(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}/dishes/",
                json=dish,
            )
            return response.status_code, response.json()

        @staticmethod
        async def update(
            ac: AsyncClient, menu: dict, submenu: dict, dish: dict
        ) -> Tuple[int, dict]:
            """Обновление блюда по id"""
            response: Response = await ac.patch(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}"
                f"/dishes/{dish.get('id')}",
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
                f"/{menu.get('id')}/submenus/{submenu.get('id')}"
                f"/dishes/{dish.get('id')}"
            )
            return response.status_code

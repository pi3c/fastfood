import pytest
from httpx import AsyncClient

url = "http://localhost:8000/api/v1/menus"


class TestCrud:
    class Menu:
        @staticmethod
        async def read_all(app):
            """чтение всех меню"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.get("/")
                return response.status_code, response.json()

        @staticmethod
        async def get(app, data):
            """Получение меню по id"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.get(f"/{data.get('id')}")
                return response.status_code, response.json()
                
        @staticmethod
        async def write(app, data):
            """создания меню"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.post("/", json=data)
                return response.status_code, response.json()
        
        @staticmethod
        async def update(app, data):
            """Обновление меню по id"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.patch(f"/{data.get('id')}", json=data)
                return response.status_code, response.json()

        @staticmethod
        async def delete(app, data):
            """Удаление меню по id"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.delete(f"/{data.get('id')}")

    class Submenu:
        @staticmethod
        async def read_all(app, menu):
            """чтение всех меню"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.get(f"/{menu.get('id')}/submenus/")
                print(response)
                return response.status_code, response.json()

        @staticmethod
        async def get(app, menu, submenu):
            """Получение меню по id"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.get(
                    f"/{menu.get('id')}/submenus/{submenu.get('id')}",
                )
                return response.status_code, response.json()

        @staticmethod
        async def write(app, menu, submenu):
            """создания меню"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.post(
                    f"/{menu.get('id')}/submenus/", json=submenu,
                )
                return response.status_code, response.json()

        @staticmethod
        async def update(app, menu, submenu):
            """Обновление меню по id"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.patch(
                    f"/{menu.get('id')}/submenus/{submenu.get('id')}",
                    json=submenu,
                )
                return response.status_code, response.json()

        @staticmethod
        async def delete(app, menu, submenu):
            """Удаление меню по id"""
            async with AsyncClient(app=app, base_url=url) as ac:
                response = await ac.delete(f"/{menu.get('id')}/submenus/{submenu.get('id')}")

    @pytest.mark.asyncio
    async def test_menu_crud(self, app):
        """Тестирование функций меню"""
        code, rspn = await self.Menu.read_all(app)
        assert code == 200

        data = {"title": "Menu", "description": None}
        code, rspn = await self.Menu.write(app, data)
        assert code == 201
        assert rspn["title"] == "Menu"
        assert rspn["description"] is None

        code, menu = await self.Menu.get(app, {"id": rspn.get("id")})
        assert code == 200
        assert menu["title"] == rspn["title"]

        upd_data = {
            "id": rspn.get("id"), "title": "upd Menu", "description": "",
        }
        code, upd_rspn = await self.Menu.update(app, upd_data)
        assert code == 200
        assert upd_rspn["title"] == "upd Menu"

        code = await self.Menu.delete(app, rspn)

        code, menu = await self.Menu.get(app, {"id": rspn.get("id")})
        assert code == 404

    @pytest.mark.asyncio
    async def test_submenu(self, app):
        menu = {"title": "Menu", "description": "main menu"}
        code, rspn = await self.Menu.write(app, menu)
        assert code == 201
        menu.update(rspn)
        print(menu)
        code, rspn = await self.Submenu.read_all(app, menu)
        assert code == 200
        assert rspn == []


class TestСontinuity:
    @pytest.mark.asyncio
    async def test_postman_continuity(self, app):
        async with AsyncClient(app=app, base_url=url) as ac:
            pass

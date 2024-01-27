import pytest


class TestCrud:
    class Menu:
        @staticmethod
        async def read_all(ac):
            """чтение всех меню"""
            response = await ac.get("/")
            return response.status_code, response.json()

        @staticmethod
        async def get(ac, data):
            """Получение меню по id"""
            response = await ac.get(f"/{data.get('id')}")
            return response.status_code, response.json()

        @staticmethod
        async def write(ac, data):
            """создания меню"""
            response = await ac.post("/", json=data)
            return response.status_code, response.json()

        @staticmethod
        async def update(ac, data):
            """Обновление меню по id"""
            response = await ac.patch(f"/{data.get('id')}", json=data)
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac, data):
            """Удаление меню по id"""
            response = await ac.delete(f"/{data.get('id')}")

    class Submenu:
        @staticmethod
        async def read_all(ac, menu):
            """чтение всех меню"""
            response = await ac.get(f"/{menu.get('id')}/submenus/")
            return response.status_code, response.json()

        @staticmethod
        async def get(ac, menu, submenu):
            """Получение меню по id"""
            response = await ac.get(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}",
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(ac, menu, submenu):
            """создания меню"""
            response = await ac.post(
                f"/{menu.get('id')}/submenus/",
                json=submenu,
            )
            return response.status_code, response.json()

        @staticmethod
        async def update(ac, menu, submenu):
            """Обновление меню по id"""
            response = await ac.patch(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}",
                json=submenu,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac, menu, submenu):
            """Удаление меню по id"""
            response = await ac.delete(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}"
            )

    @pytest.mark.asyncio
    async def test_menu_crud(self, client):
        """Тестирование функций меню"""
        code, rspn = await self.Menu.read_all(client)
        assert code == 200

        data = {"title": "Menu", "description": None}
        code, rspn = await self.Menu.write(client, data)
        assert code == 201
        assert rspn["title"] == "Menu"
        assert rspn["description"] is None

        code, menu = await self.Menu.get(client, {"id": rspn.get("id")})
        assert code == 200
        assert menu["title"] == rspn["title"]

        upd_data = {
            "id": rspn.get("id"),
            "title": "upd Menu",
            "description": "",
        }
        code, upd_rspn = await self.Menu.update(client, upd_data)
        assert code == 200
        assert upd_rspn["title"] == "upd Menu"

        code = await self.Menu.delete(client, rspn)

        code, menu = await self.Menu.get(client, {"id": rspn.get("id")})
        assert code == 404

    @pytest.mark.asyncio
    async def test_submenu(self, client):
        # Создаем меню и проверяем ответ
        menu = {"title": "Menu", "description": "main menu"}
        code, rspn = await self.Menu.write(client, menu)
        assert code == 201
        menu.update(rspn)

        # Проверяем наличие подменю
        code, rspn = await self.Submenu.read_all(client, menu)
        assert code == 200
        assert rspn == []

        # Создаем и проверяем подменю
        submenu = {
            "title": "Submenu",
            "description": "submenu",
            "parent_menu": menu["id"],
        }
        code, rspn = await self.Submenu.write(client, menu, submenu)
        assert code == 201
        submenu.update(rspn)

        # Проверяем меню на наличие подменю
        code, rspn = await self.Menu.get(client, menu)
        assert code == 200
        assert rspn["submenus_count"] == 1

        # Обновляем подменю и проверяем
        submenu["title"] = "updated_submenu"
        code, rspn = await self.Submenu.update(client, menu, submenu)
        assert code == 200
        assert submenu["title"] == rspn["title"]
        submenu.update(rspn)

        # Удаляем подменю
        await self.Submenu.delete(client, menu, submenu)

        # Проверяем меню
        code, rspn = await self.Menu.get(client, menu)
        assert code == 200
        assert rspn["submenus_count"] == 0

        # Проверяем удаленное подменю
        code, rspn = await self.Submenu.get(client, menu, submenu)
        assert code == 404

        # удаляем сопутствующее
        await self.Menu.delete(client, menu)


#
# class TestСontinuity:
#     @pytest.mark.asyncio
#     async def test_postman_continuity(self, app):
#         async with AsyncClient(app=app, base_url=url) as ac:
#             pass

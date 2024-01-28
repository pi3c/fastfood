import pytest


class TestBaseCrud:
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
            return response.status_code

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
            return response.status_code

    class Dish:
        @staticmethod
        async def read_all(ac, menu, submenu):
            """чтение всех блюд"""
            response = await ac.get(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}/dishes/",
            )
            return response.status_code, response.json()

        @staticmethod
        async def get(ac, menu, submenu, dish):
            """Получение блюда по id"""
            response = await ac.get(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}/dishes/{dish.get('id')}",
            )
            return response.status_code, response.json()

        @staticmethod
        async def write(ac, menu, submenu, dish):
            """создания блюда"""
            response = await ac.post(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}/dishes/",
                json=dish,
            )
            return response.status_code, response.json()

        @staticmethod
        async def update(ac, menu, submenu, dish):
            """Обновление блюда по id"""
            response = await ac.patch(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}/dishes/{dish.get('id')}",
                json=dish,
            )
            return response.status_code, response.json()

        @staticmethod
        async def delete(ac, menu, submenu, dish):
            """Удаление блюда по id"""
            response = await ac.delete(
                f"/{menu.get('id')}/submenus/{submenu.get('id')}/dishes/{dish.get('id')}"
            )
            return response.status_code

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
        assert code == 200

        code, menu = await self.Menu.get(client, {"id": rspn.get("id")})
        assert code == 404

    @pytest.mark.asyncio
    async def test_submenus(self, client):
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
        code = await self.Submenu.delete(client, menu, submenu)
        assert code == 200

        # Проверяем меню
        code, rspn = await self.Menu.get(client, menu)
        assert code == 200
        assert rspn["submenus_count"] == 0

        # Проверяем удаленное подменю
        code, rspn = await self.Submenu.get(client, menu, submenu)
        assert code == 404

        # удаляем сопутствующее
        await self.Menu.delete(client, menu)

    @pytest.mark.asyncio
    async def test_dishes(self, client):
        # Создаем меню и проверяем ответ
        menu = {
            "title": "Menu",
            "description": "main menu",
        }
        code, rspn = await self.Menu.write(client, menu)
        assert code == 201
        menu.update(rspn)

        # Создаем и проверяем подменю
        submenu = {
            "title": "Submenu",
            "description": "submenu",
            "parent_menu": menu["id"],
        }
        code, rspn = await self.Submenu.write(client, menu, submenu)
        assert code == 201
        submenu.update(rspn)

        # Проверяем все блюда в подменю
        code, rspn = await self.Dish.read_all(client, menu, submenu)
        assert code == 200
        assert rspn == []

        # Добавляем блюдо
        dish = {
            "title": "dish",
            "description": "some dish",
            "price": "12.5",
            "parent_submenu": submenu["id"],
        }
        code, rspn = await self.Dish.write(client, menu, submenu, dish)
        assert code == 201
        dish.update(rspn)

        # Получаем блюдо
        code, rspn = await self.Dish.get(client, menu, submenu, dish)
        assert code == 200
        assert rspn["title"] == dish["title"]

        # Проверяем меню на количество блюд
        code, rspn = await self.Menu.get(client, menu)
        assert code == 200
        assert rspn["dishes_count"] == 1

        # Проверяем подменю на наличие блюд
        code, rspn = await self.Submenu.get(client, menu, submenu)
        assert code == 200
        assert rspn["dishes_count"] == 1

        # Обновляем блюдо и проверяем
        dish["title"] = "updated_dish"
        code, rspn = await self.Dish.update(client, menu, submenu, dish)
        assert code == 200
        assert dish["title"] == rspn["title"]
        dish.update(rspn)

        # Удаляем подменю
        code = await self.Dish.delete(client, menu, submenu, dish)
        assert code == 200

        # Проверяем меню
        code, rspn = await self.Menu.get(client, menu)
        assert code == 200
        assert rspn["dishes_count"] == 0

        # Проверяем подменю на наличие блюд
        code, rspn = await self.Submenu.get(client, menu, submenu)
        assert code == 200
        assert rspn["dishes_count"] == 0

        # Проверяем удаленное блюдо
        code, rspn = await self.Dish.get(client, menu, submenu, dish)
        assert code == 404

        # удаляем сопутствующее
        await self.Submenu.delete(client, menu, submenu)
        await self.Menu.delete(client, menu)


class TestСontinuity:
    @pytest.mark.asyncio
    async def test_postman_continuity(self, client):
        # Создаем меню
        menu = {
            "title": "Menu",
            "description": "main menu",
        }
        code, rspn = await TestBaseCrud.Menu.write(client, menu)
        assert code == 201
        assert "id" in rspn.keys()
        menu.update(rspn)

        # Создаем подменю
        submenu = {
            "title": "Submenu",
            "description": "submenu",
            "parent_menu": menu["id"],
        }
        code, rspn = await TestBaseCrud.Submenu.write(client, menu, submenu)
        assert code == 201
        assert "id" in rspn.keys()
        submenu.update(rspn)

        # Добавляем блюдо1
        dish = {
            "title": "dish1",
            "description": "some dish1",
            "price": "13.50",
            "parent_submenu": submenu["id"],
        }
        code, rspn = await TestBaseCrud.Dish.write(client, menu, submenu, dish)
        assert code == 201
        assert "id" in rspn.keys()
        dish.update(rspn)

        # Добавляем блюдо2
        dish = {
            "title": "dish2",
            "description": "some dish2",
            "price": "12.50",
            "parent_submenu": submenu["id"],
        }
        code, rspn = await TestBaseCrud.Dish.write(client, menu, submenu, dish)
        assert code == 201
        assert "id" in rspn.keys()
        dish.update(rspn)

        # Просматриваем конкретное меню
        code, rspn = await TestBaseCrud.Menu.get(client, menu)
        assert code == 200
        assert "id" in rspn.keys()
        assert menu["id"] == rspn["id"]
        assert "submenus_count" in rspn.keys()
        assert rspn["submenus_count"] == 1
        assert "dishes_count" in rspn.keys()
        assert rspn["dishes_count"] == 2

        # Просматриваем конкретное подменю
        code, rspn = await TestBaseCrud.Submenu.get(client, menu, submenu)
        assert code == 200
        assert "id" in rspn.keys()
        assert "dishes_count" in rspn.keys()
        assert rspn["dishes_count"] == 2

        # Удаляем подменю
        code = await TestBaseCrud.Submenu.delete(client, menu, submenu)
        assert code == 200

        # Просматриваем список подменю
        code, rspn = await TestBaseCrud.Submenu.read_all(client, menu)
        assert code == 200
        assert rspn == []

        # Просматриваем список блюд
        code, rspn = await TestBaseCrud.Dish.read_all(client, menu, submenu)
        assert code == 200
        assert rspn == []

        # Просматриваем конкретное меню
        code, rspn = await TestBaseCrud.Menu.get(client, menu)
        assert code == 200
        assert "id" in rspn.keys()
        assert menu["id"] == rspn["id"]
        assert "submenus_count" in rspn.keys()
        assert rspn["submenus_count"] == 0
        assert "dishes_count" in rspn.keys()
        assert rspn["dishes_count"] == 0
        
        # Удаляем меню
        code = await TestBaseCrud.Menu.delete(client, menu)
        assert code == 200

        # Просматриваем все меню
        code, rspn = await TestBaseCrud.Menu.read_all(client)
        assert code == 200
        assert rspn == []

import pytest
from httpx import AsyncClient

url = "http://localhost:8000/api/v1/menus"


class TestCrud:
    @pytest.mark.asyncio
    async def test_read_menus(self, app):
        """тест пустой бд"""
        async with AsyncClient(app=app, base_url=url) as ac:
            response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_write_menu(self, app):
        """"""
        async with AsyncClient(app=app, base_url=url) as ac:
            response = await ac.post("/", json={"title": "menu 1", "description": None})
        assert response.status_code == 201
        assert response.json()["title"] == "menu 1"
        assert response.json()["description"] == None


class TestСontinuity:
    @pytest.mark.asyncio
    async def test_postman_continuity(self, app):
        async with AsyncClient(app=app, base_url=url) as ac:
            pass

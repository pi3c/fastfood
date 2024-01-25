import pytest
from httpx import AsyncClient


url = "http://localhost:8000/api/v1/menus"


@pytest.mark.asyncio
async def test_read_menus(app):
    async with AsyncClient(app=app, base_url=url) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_write_menu(app):
    async with AsyncClient(app=app, base_url=url) as ac:
        response = await ac.post("/", json={"title": "ddd", "description": "hh"})
    assert response.status_code == 201
    assert response.json()["title"] == "ddd"

import pytest
from httpx import AsyncClient
import pytest_asyncio


# записываем файл post_controller в переменную post_module
import controllers.post_controller as post_module
from app import app
from models.database import posts
from schemas.model import Post


# создаем фикстуру с копией бд, которая будет обнуляться перед каждым тестом
@pytest.fixture(autouse=True)
def post_controller() -> post_module.PostController:
    post_module.controller = post_module.PostController(posts.copy())
    yield post_module.controller


# кладем бд в фикстуру, сможем использовать ее в тестах
@pytest.fixture
def post_db(post_controller: post_module.PostController) -> dict[int: Post]:
    return post_controller.post_db


# создаем фикстуру с клиентом
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as client:
        yield client

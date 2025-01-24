import pytest
from httpx import AsyncClient
import pytest_asyncio

# записываем файл post_controller в переменную post_module
import controllers.post_controller as post_module
from app import app
from core.settings import Settings, get_settings
from db.connector import DatabaseConnector

pytest_plugins = [
    "fixtures.test_db",
    "fixtures.prepare_post",
    "fixtures.prepare_author",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


# создаем фикстуру с копией бд, которая будет обнуляться перед каждым тестом
@pytest.fixture(autouse=True)
def post_controller(post_db: DatabaseConnector) -> post_module.PostController:
    post_module.controller = post_module.PostController(post_db)
    yield post_module.controller


# создаем фикстуру с клиентом
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as client:
        yield client

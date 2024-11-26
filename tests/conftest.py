import pytest
# записываем файл post_controller в переменную post_module
import controllers.post_controller as post_module
from models.database import posts
from schemas.model import Post


# создаем фикстуру с копией бд, которая будет обнуляться перед каждым тестом
@pytest.fixture(autouse=True)
def post_controller() -> post_module.PostController:
    post_module.controller = post_module.PostController(posts.copy())
    yield post_module.controller


# кладем бд в фикстуру, сможем использовать ее в тестах
@pytest.fixture
def post_db(post_controller: post_module.PostController) -> list[Post]:
    return post_controller.post_db

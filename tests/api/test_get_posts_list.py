import pytest

from db.models import Post, Author
from schemas.enums import OrderBy


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_posts")
async def test_get_posts(async_client, posts: list[Post], author: Author):
    # Создаем объект фильтров
    filters = {
        "limit": 5,
        "offset": 3,
        "search": "test",
        "order_by": OrderBy.CREATED_AT.value,
        "descending": True
    }

    # Отправляем запрос с параметрами
    response = await async_client.get("/posts/", params=filters)

    assert response.status_code == 200, response.text

    # Эмулируем фильтрацию, сортировку и пагинацию API
    filtered_posts = [
        p for p in posts if not filters["search"] or filters["search"] in p.title
    ]
    sorted_posts = sorted(filtered_posts, key=lambda p: p.created_at, reverse=filters["descending"])

    expected_posts = sorted_posts[filters["offset"]: filters["offset"] + filters["limit"]]

    # Проверяем результат
    assert response.json() == [
        {
            "id": str(post.id),
            "title": post.title,
            "short_body": post.short_body,
            "author": {
                "id": str(author.id),
                "name": author.name,
                "age": author.age,
            }
        }
        for post in expected_posts
    ]

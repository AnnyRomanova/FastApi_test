from uuid import UUID, uuid4

import pytest

from db.connector import DatabaseConnector
from db.models import Author, Post


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_post")
async def test_update_post_202(async_client, post_db: DatabaseConnector, post_id: UUID, author: Author):
    response_body = {"title": "update_test_title",
                     "short_body": "update_test_short_body",
                     "body": "update_test_body"}

    response = await async_client.put(f"/posts/{post_id}", json=response_body)
    assert response.status_code == 202, response.text
    data = response.json()
    assert data == {
        "id": str(post_id),
        "title": "update_test_title",
        "short_body": "update_test_short_body",
        "author": {
            "id": str(author.id),
            "name": author.name,
            "age": author.age
        }
    }
    async with post_db.session_maker() as session:
        post_db = await session.get(Post, data["id"])
    assert post_db.title == data["title"]
    assert post_db.short_body == data["short_body"]


@pytest.mark.asyncio
async def test_update_post_404(async_client):
    response_body = {"title": "update_test_title",
                     "short_body": "update_test_short_body",
                     "body": "update_test_body"}

    response = await async_client.put(f"/posts/{uuid4()}", json=response_body)
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Пост не найден"}

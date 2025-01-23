from unittest.mock import ANY
from uuid import uuid4

import pytest

from db.connector import DatabaseConnector
from db.models import Author, Post


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_author")
async def test_create_post_201(async_client, post_db: DatabaseConnector, author: Author):
    new_post_data = {"title": "test_title",
                     "short_body": "test_short_body",
                     "body": "test_body",
                     "author_id": str(author.id)}
    response = await async_client.post("/posts/", json=new_post_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data == {
        "id": ANY,
        "title": "test_title",
        "body": "test_body",
        "author": {
            "id": str(author.id),
            "name": author.name,
            "age": author.age
        }
    }
    async with post_db.session_maker() as session:
        post_db = await session.get(Post, data["id"])
    assert post_db.title == data["title"]
    assert post_db.author_id == author.id


@pytest.mark.asyncio
async def test_create_post_400(async_client):
    response_body = {"title": "new_test_title",
                     "body": "new_test_body",
                     "short_body": "new_test_short_body",
                     "author_id": str(uuid4())}

    response = await async_client.post("/posts/", json=response_body)
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": f"Автор с id {response_body["author_id"]} не найден."}

from uuid import uuid4

import pytest

from db.models import Post, Author


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_post")
async def test_post_for_id_200(async_client, post: Post, author: Author):
    response = await async_client.get(f"/posts/{post.id}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(post.id),
        "title": post.title,
        "body": post.body,
        "author": {
            "id": str(author.id),
            "name": author.name,
            "age": author.age
        }
    }


@pytest.mark.asyncio
async def test_post_for_id_404(async_client):
    response = await async_client.get(f"/posts/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Пост не найден"}
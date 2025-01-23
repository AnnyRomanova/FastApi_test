from uuid import UUID, uuid4

import pytest

from db.connector import DatabaseConnector
from db.models import Post


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_post")
async def test_delete_post_204(async_client, post_db: DatabaseConnector, post_id: UUID):
    response = await async_client.delete(f"/posts/{post_id}")
    assert response.status_code == 204, response.text
    assert response.content == b""
    async with post_db.session_maker() as session:
        deleted_post = await session.get(Post, post_id)
    assert deleted_post is None


@pytest.mark.asyncio
async def test_delete_post_404(async_client):
    response = await async_client.delete(f"/posts/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Пост не найден"}

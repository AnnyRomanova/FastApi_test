import pytest


@pytest.mark.asyncio
async def test_get_posts(async_client):
    response = await async_client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == [
         {"id": 1, "title": "title_1", "body": "body_1", "author_id": 1},
         {"id": 2, "title": "title_2", "body": "body_2", "author_id": 2},
         {"id": 3, "title": "title_3", "body": "body_3", "author_id": 3}
    ]


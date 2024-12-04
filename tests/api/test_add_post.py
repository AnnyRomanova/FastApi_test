import pytest
from schemas.model import Post


@pytest.mark.asyncio
async def test_create_post_201(async_client, post_db: dict[int: Post]):
    new_post_id = len(post_db) + 1
    response_body = {"title": "new_test_title",
                     "body": "new_test_body",
                     "author_id": 1}
    response = await async_client.post("/posts/", json=response_body)

    assert response.status_code == 201
    assert response.json() == {"id": new_post_id,
                               "title": "new_test_title",
                               "body": "new_test_body",
                               "author_id": 1}


@pytest.mark.asyncio
async def test_create_post_404(async_client):
    response_body = {"title": "new_test_title",
                     "body": "new_test_body",
                     "author_id": 10000}

    response = await async_client.post("/posts/", json=response_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
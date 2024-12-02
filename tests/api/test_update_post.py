import pytest


@pytest.mark.asyncio
async def test_update_post_202(async_client):
    response_body = {"id": 1,
                     "title": "new_test_title",
                     "body": "new_test_body",
                     "author_id": 1}

    response = await async_client.put("/posts/1", json=response_body)
    assert response.status_code == 202
    assert response.json() == {"id": 1,
                               "title": "new_test_title",
                               "body": "new_test_body",
                               "author_id": 1}


@pytest.mark.asyncio
async def test_update_post_404(async_client):
    response_body = {"id": 1,
                     "title": "new_test_title",
                     "body": "new_test_body",
                     "author_id": 1}

    response = await async_client.put("/posts/10000", json=response_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
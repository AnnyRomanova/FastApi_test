import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
# декоратор позволяет подставлять в функцию различные входные и получаемые данные
@pytest.mark.parametrize("post_id, expected_result",
                         [(1, {"id": 1, "title": "title_1", "body": "body_1", "author_id": 1}),
                          (2, {"id": 2, "title": "title_2", "body": "body_2", "author_id": 2}),
                          (3, {"id": 3, "title": "title_3", "body": "body_3", "author_id": 3})])
async def test_post_for_id_200(async_client, post_id, expected_result):
    response = await async_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json() == expected_result


@pytest.mark.asyncio
async def test_post_for_id_404(async_client):
    response = await async_client.get("/posts/-1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
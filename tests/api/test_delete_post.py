import pytest


@pytest.mark.asyncio
async def test_delete_post_204(async_client):
    response = await async_client.delete("/posts/1")
    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.asyncio
async def test_delete_post_404(async_client):
    response = await async_client.delete("/posts/10000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

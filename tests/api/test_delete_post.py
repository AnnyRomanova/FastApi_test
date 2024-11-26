from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_delete_post_204():
    response = client.delete("/posts/1")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_post_404():
    response = client.delete("/posts/10000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

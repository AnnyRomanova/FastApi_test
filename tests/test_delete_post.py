from fastapi.testclient import TestClient
from src.app import app, posts

client = TestClient(app)


def test_delete_post_200():
    response = client.delete("/post/delete/1")
    assert response.status_code == 200
    assert response.json() == posts


def test_delete_post_404():
    response = client.delete("/post/delete/10000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

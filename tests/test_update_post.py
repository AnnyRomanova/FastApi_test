from fastapi.testclient import TestClient
from src.app import app, users

client = TestClient(app)


def test_update_post_200():
    response_body = {"title": "new_test_title",
                     "body": "new_test_body"}

    response = client.put("/post/update/1", json=response_body)
    assert response.status_code == 200
    assert response.json() == {"id": 1,
                               "title": "new_test_title",
                               "body": "new_test_body",
                               "author": users[1]}


def test_update_post_404():
    response_body = {"title": "new_test_title",
                     "body": "new_test_body"}

    response = client.put("/post/update/10000", json=response_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
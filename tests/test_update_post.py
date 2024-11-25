from fastapi.testclient import TestClient
from app import app
from models.database import users
import pytest


client = TestClient(app)


@pytest.mark.order(6)
def test_update_post_202():
    response_body = {"title": "new_test_title",
                     "body": "new_test_body"}

    response = client.put("/posts/1", json=response_body)
    assert response.status_code == 202
    assert response.json() == {"id": 1,
                               "title": "new_test_title",
                               "body": "new_test_body",
                               "author": users[1]}


@pytest.mark.order(7)
def test_update_post_404():
    response_body = {"title": "new_test_title",
                     "body": "new_test_body"}

    response = client.put("/posts/10000", json=response_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
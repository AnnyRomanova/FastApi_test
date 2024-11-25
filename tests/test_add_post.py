from fastapi.testclient import TestClient
from app import app
from models.database import posts, users
import pytest


client = TestClient(app)


@pytest.mark.order(4)
def test_create_post_201():
    new_post_id = len(posts) + 1
    response_body = {"title": "new_test_title",
                     "body": "new_test_body",
                     "author_id": 1}

    response = client.post("/posts", json=response_body)
    assert response.status_code == 201
    assert response.json() == {"id": new_post_id,
                               "title": "new_test_title",
                               "body": "new_test_body",
                               "author": users[0]}


@pytest.mark.order(5)
def test_create_post_404():
    response_body = {"title": "new_test_title",
                     "body": "new_test_body",
                     "author_id": 10000}

    response = client.post("/posts", json=response_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
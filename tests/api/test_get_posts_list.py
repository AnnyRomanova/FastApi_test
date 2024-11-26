from app import app
from models.database import users
from fastapi.testclient import TestClient


# эмулято http-запросов
# позволяет делать запросы к API напрямую
client = TestClient(app)


def test_get_posts():
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "title_1", "body": "body_1", "author": users[1]},
        {"id": 2, "title": "title_2", "body": "body_2", "author": users[0]},
        {"id": 3, "title": "title_3", "body": "body_3", "author": users[2]}]


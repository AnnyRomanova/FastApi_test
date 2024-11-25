import pytest
from fastapi.testclient import TestClient
from app import app
from models.database import users


client = TestClient(app)


@pytest.mark.order(2)
# декоратор позволяет подставлять в функцию различные входные и получаемые данные
@pytest.mark.parametrize("post_id, expected_result",
                         [(1, {"id": 1, "title": "title_1", "body": "body_1", "author": users[1]}),
                          (2, {"id": 2, "title": "title_2", "body": "body_2", "author": users[0]}),
                          (3, {"id": 3, "title": "title_3", "body": "body_3", "author": users[2]})])
def test_post_for_id_200(post_id, expected_result):
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json() == expected_result


@pytest.mark.order(3)
def test_post_for_id_404():
    response = client.get("/posts/-1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
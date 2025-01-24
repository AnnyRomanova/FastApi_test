import pytest

from db.models import Post, Author


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_post")
async def test_get_posts(async_client, post: Post, author: Author):
    response = await async_client.get("/posts/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": str(post.id),
            "title": post.title,
            "short_body": post.short_body,
            "author": {
                "id": str(author.id),
                "name": author.name,
                "age": author.age,
            }
        }
    ]

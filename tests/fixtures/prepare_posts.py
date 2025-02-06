from datetime import datetime
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Post


@pytest.fixture
def posts(post_id: UUID, author_id: UUID) -> list[Post]:
    return [
        Post(
            id=uuid4(),
            title=f"test_title_{i}",
            short_body=f"test_short_body_{i}",
            body=f"test_body_{i}",
            author_id=author_id,
            created_at=datetime.now()
        )
        for i in range(10)  # Создаём 10 постов
    ]

@pytest_asyncio.fixture
async def prepare_posts(post_db: DatabaseConnector, posts: list[Post], prepare_author: None) -> None:
    async with post_db.session_maker(expire_on_commit=False) as session:
        session.add_all(posts)  # Добавляем список постов
        await session.commit()
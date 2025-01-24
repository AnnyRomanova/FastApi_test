from uuid import uuid4, UUID

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Post


@pytest.fixture
def post_id() -> UUID:
    return uuid4()


@pytest.fixture
def post(post_id: UUID, author_id: UUID) -> Post:
    return Post(
        id=post_id,
        title="test_title",
        short_body="test_short_body",
        body="test_body",
        author_id=author_id,
    )


@pytest_asyncio.fixture
async def prepare_post(post_db: DatabaseConnector, post: Post, prepare_author: None) -> None:
    async with post_db.session_maker(expire_on_commit=False) as session:
        session.add(post)
        await session.commit()

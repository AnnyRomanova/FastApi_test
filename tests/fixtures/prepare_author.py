from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Author


@pytest.fixture
def author_id() -> UUID:
    return uuid4()


@pytest.fixture
def author(author_id: UUID) -> Author:
    return Author(
        id=author_id,
        name="test_author_name",
        age=18,
    )


@pytest_asyncio.fixture
async def prepare_author(post_db: DatabaseConnector, author: Author) -> None:
    async with post_db.session_maker(expire_on_commit=False) as session:
        session.add(author)
        await session.commit()

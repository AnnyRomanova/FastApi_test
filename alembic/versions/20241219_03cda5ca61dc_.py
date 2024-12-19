"""empty message

Revision ID: 03cda5ca61dc
Revises: d21a68c2385f
Create Date: 2024-12-19 21:29:32.954036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models import Post
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision: str = '03cda5ca61dc'
down_revision: Union[str, None] = 'd21a68c2385f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()  # Получаем объект соединения
    session = Session(bind=bind)  # Создаем сессию

    # Заполняю таблицу posts
    post1 = Post(title='title_1', body='body_1', author_id=1)
    post2 = Post(title='title_2', body='body_2', author_id=2)
    post3 = Post(title='title_3', body='body_3', author_id=1)
    post4 = Post(title='title_4', body='body_4', author_id=3)

    session.add_all([post1, post2, post3, post4])
    session.commit()


def downgrade() -> None:
    pass

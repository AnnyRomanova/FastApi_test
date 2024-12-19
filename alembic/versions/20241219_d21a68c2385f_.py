"""empty message

Revision ID: d21a68c2385f
Revises: 5bcfb89863cc
Create Date: 2024-12-19 21:13:16.038466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from src.models import Author


# revision identifiers, used by Alembic.
revision: str = 'd21a68c2385f'
down_revision: Union[str, None] = '5bcfb89863cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()  # Получаем объект соединения
    session = Session(bind=bind)  # Создаем сессию

    # Заполняю таблицу authors
    author1 = Author(author_name='Anna', age=29)
    author2 = Author(author_name='Pavel', age=33)
    author3 = Author(author_name='Inga', age=56)

    session.add_all([author1, author2, author3])
    session.commit()



def downgrade() -> None:
    pass

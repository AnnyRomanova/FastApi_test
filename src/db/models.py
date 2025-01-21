import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

# Базовый класс, от которого наследуются классы таблиц
Base = declarative_base()


# Создаем модели таблиц для бд


class Author(Base):
    __tablename__ = 'authors'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Прописываем связь таблиц
    posts = relationship('Post', order_by='Post.id', back_populates='author')


class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    short_body = Column(String, nullable=False)
    body = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Прописываем обратную связь
    author = relationship('Author', back_populates='posts')

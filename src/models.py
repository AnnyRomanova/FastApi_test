from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Базовый класс, от которого наследуются классы таблиц
Base = declarative_base()


# Создаем модели таблиц для бд


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    # Прописываем связь таблиц
    posts = relationship('Post', order_by='Post.id', back_populates='author')


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    # Прописываем обратную связь
    author = relationship('Author', back_populates='posts')

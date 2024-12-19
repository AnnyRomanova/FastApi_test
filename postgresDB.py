from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

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


# Создаем движок
engine = create_engine("postgresql+psycopg2://Anny:123456@localhost:5431/FAT_db4", echo=True) # будет выводить логи в терминал

# Создаем сами таблицы в бд
Base.metadata.create_all(engine) # metadata хранит информацию о всех таблицах, определенных через эти классы.

# Создаем сессию для работы с бд
Session = sessionmaker(bind=engine) # sessionmaker - фабрика, которая создает объекты сессий
session = Session() # Создает экземпляр сессии, который можно использовать для работы с бд


# Заполняю таблицу authors
author1 = Author(author_name='Anna', age=29)
author2 = Author(author_name='Pavel', age=33)
author3 = Author(author_name='Inga', age=56)

session.add_all([author1, author2, author3])
session.commit()


# Заполняю таблицу posts
post1 = Post(title='title_1', body='body_1', author_id=1)
post2 = Post(title='title_2', body='body_2', author_id=2)
post3 = Post(title='title_3', body='body_3', author_id=1)
post4 = Post(title='title_4', body='body_4', author_id=3)

session.add_all([post1, post2, post3, post4])
session.commit()

session.close()
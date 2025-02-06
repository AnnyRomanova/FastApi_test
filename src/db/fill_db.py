# Создаем движок
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from db.models import Author, Post

# Базовый класс, от которого наследуются классы таблиц
Base = declarative_base()

engine = create_engine("postgresql+psycopg2://Anny:123456@localhost:5431/FAT_db4",
                       echo=True)  # будет выводить логи в терминал

# Создаем сами таблицы в бд
Base.metadata.create_all(engine)  # metadata хранит информацию о всех таблицах, определенных через эти классы.

# Создаем сессию для работы с бд
Session = sessionmaker(bind=engine)  # sessionmaker - фабрика, которая создает объекты сессий
session = Session()  # Создает экземпляр сессии, который можно использовать для работы с бд

# Заполняю таблицу authors
author1 = Author(id=uuid4(), name='Anna', age=29)
author2 = Author(id=uuid4(), name='Pavel', age=33)
author3 = Author(id=uuid4(), name='Inga', age=56)

session.add_all([author1, author2, author3])
session.commit()

# Заполняю таблицу posts
post1 = Post(id=uuid4(), title='title_1', body='body_1', short_body='short_body_1', author_id=author1.id)
post2 = Post(id=uuid4(), title='title_2', body='body_2', short_body='short_body_2', author_id=author2.id)
post3 = Post(id=uuid4(), title='title_3', body='body_3', short_body='short_body_3', author_id=author3.id)
post4 = Post(id=uuid4(), title='title_4', body='body_4', short_body='short_body_4', author_id=author1.id)

session.add_all([post1, post2, post3, post4])
session.commit()

session.close()

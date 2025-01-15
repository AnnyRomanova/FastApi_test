import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID

from db.connector import DatabaseConnector
import schemas.model as post_pydentic
import db.models as post_DB

logger = logging.getLogger(__name__)


# todo переименовать файл на CRUD
class PostController:

    def __init__(self, post_db: DatabaseConnector) -> None:
        self.post_db = post_db

    async def get_posts_list(self) -> list[post_pydentic.PostOUT]:
        async with self.post_db.session_maker() as session:
            stmt = select(post_DB.Post).options(joinedload(post_DB.Post.author))  # Используем модель базы данных
            cursor = await session.execute(stmt)
            posts = cursor.scalars().all()
            # Конвертируем объекты базы данных в словари и создаём Pydantic модели
            posts_list = []
            for post in posts:
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "short_body": post.short_body,
                    "author": {
                        "id": post.author.id,
                        "name": post.author.name,
                        "age": post.author.age,
                    }
                }
                posts_list.append(post_pydentic.PostOUT(**post_data))

            return posts_list

    async def get_post(self, post_id: UUID) -> post_pydentic.PostDetail:
        logger.info("Post by id requested")
        async with self.post_db.session_maker() as session:
            stmt = select(post_DB.Post).where(post_DB.Post.id == post_id).options(
                joinedload(post_DB.Post.author))  # фильтр по id
            cursor = await session.execute(stmt)
            post = cursor.scalar_one_or_none()  # получаем один объект или None

            if not post:
                raise HTTPException(status_code=404, detail="Пост не найден")

            # Явное преобразование объекта ORM в словарь
            post_data = {
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "author": {
                    "id": post.author.id,
                    "name": post.author.name,
                    "age": post.author.age,
                }
            }
            # Передаём словарь в Pydantic модель
            return post_pydentic.PostDetail(**post_data)

    async def add_post(self, post_data: post_pydentic.PostCreate) -> None:
        logger.info("Request to add new post")
        async with self.post_db.session_maker() as session:
            # Проверяем существование автора
            stmt = select(post_DB.Author).where(post_DB.Author.id == post_data.author_id)
            result = await session.execute(stmt)
            author = result.scalar_one_or_none()

            if not author:
                logger.error(f"Author with id {post_data.author_id} does not exist.")
                raise HTTPException(status_code=500, detail=f"Автор с id {post_data.author_id} не найден.")

            # Создаем экземпляр модели базы данных
            new_post = post_DB.Post(**post_data.model_dump())
            session.add(new_post)

            await session.commit()
            await session.refresh(new_post)

    async def update_post(self, post: post_pydentic.PostUpdate, post_id: UUID) -> post_pydentic.PostOUT:
        logger.info("Request to update post")
        async with self.post_db.session_maker() as session:
            stmt = select(post_DB.Post).where(post_DB.Post.id == post_id)  # Ищем пост по ID
            cursor = await session.execute(stmt)
            existing_post = cursor.scalar_one_or_none()  # Получаем объект поста или None

            if not existing_post:
                raise HTTPException(status_code=404, detail="Пост не найден")

            # Обновляем поля поста
            for key, value in post.model_dump().items():
                setattr(existing_post, key, value)

            # Сохраняем изменения
            session.add(existing_post)
            await session.commit()
            await session.refresh(existing_post)  # Обновляем объект из базы данных

            # Загрузка автора
            author = await session.get(post_DB.Author, existing_post.author_id)
            if not author:
                raise HTTPException(status_code=404, detail="Автор не найден")

            # Преобразуем объект базы данных в словарь
            post_dict = existing_post.__dict__

            # Убираем ненужный атрибут
            post_dict.pop('_sa_instance_state', None)

            # Добавляем автора в данные поста
            post_dict['author'] = post_pydentic.Author.model_validate(author)  # Используем модель Pydantic для автора

            # Преобразуем в Pydantic модель и возвращаем
            return post_pydentic.PostOUT(**post_dict)

    async def delete_post(self, post_id: UUID) -> None:
        logger.info("Request to delete post")
        async with self.post_db.session_maker() as session:
            stmt = select(post_DB.Post).where(post_DB.Post.id == post_id)  # Ищем пост по ID
            cursor = await session.execute(stmt)
            existing_post = cursor.scalar_one_or_none()  # Получаем объект поста или None

            if not existing_post:
                raise HTTPException(status_code=404, detail="Пост не найден")

            # Удаляем пост
            await session.delete(existing_post)
            await session.commit()  # Фиксируем изменения
        logger.info("Post deleted")


controller: PostController | None = None


def get_post_controller() -> PostController:
    assert controller is not None, "Post controller not initialized"
    return controller

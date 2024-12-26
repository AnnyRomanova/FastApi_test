import logging

from fastapi import HTTPException
from sqlalchemy import select

from db.connector import DatabaseConnector
import schemas.model as post_pydentic
import db.models as post_DB


logger = logging.getLogger(__name__)


class PostController:

    def __init__(self, post_db: DatabaseConnector) -> None:
        self.post_db = post_db


    async def get_posts_list(self) -> list[post_pydentic.Post]:
        async with self.post_db.session_maker() as session:
            stmt = select(post_DB.Post)  # Используем модель базы данных
            cursor = await session.execute(stmt)
            posts = cursor.scalars().all()
            # Конвертируем объекты базы данных в Pydantic-модели
            return [post_pydentic.Post.model_validate(post) for post in posts]



    async def get_post(self, post_id: int) -> post_pydentic.Post:
        logger.info("Post by id requested")
        async with self.post_db.session_maker() as session:
            stmt = select(post_DB.Post).where(post_DB.Post.id == post_id)  # фильтр по id
            cursor = await session.execute(stmt)
            post = cursor.scalar_one_or_none()  # получаем один объект или None

            if not post:
                raise HTTPException(status_code=404, detail="Пост не найден")

            return post_pydentic.Post.model_validate(post)


    async def add_post(self, post_data: post_pydentic.PostCreate) -> post_pydentic.Post:
        logger.info("Request to add new post")
        async with self.post_db.session_maker() as session:
            new_post = post_DB.Post(**post_data.model_dump())  # Создаем экземпляр модели базы данных
            session.add(new_post)  # Добавляем объект в сессию

            await session.commit()  # Фиксируем изменения
            await session.refresh(new_post)  # Обновляем объект для получения автогенерированных данных (id)

            return post_pydentic.Post(**new_post.__dict__)  # Преобразуем в Pydantic-модель


    async def update_post(self, post: post_pydentic.Post, post_id: int) -> post_pydentic.Post:
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

            # Преобразуем объект базы данных обратно в Pydantic-модель
            return post_pydentic.Post(**existing_post.__dict__)


    async def delete_post(self, post_id: int) -> None:
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

import uvicorn
import logging.config

from fastapi import FastAPI, HTTPException
from typing import List

from schemas.database import posts, users
from schemas.model import Post, PostCreate, PostUpdate
from core.settings import settings

app = FastAPI(title=settings.app_name)
logger = logging.getLogger(__name__)


# выводит список постов
@app.get("/posts", response_model=List[Post])
async def get_posts() -> List[Post]:
    logger.info("Post`s list requested")
    post_objects = []
    for post in posts:
        # каждый элемент в списке точно соответствует структуре класса Post
        post_objects.append(Post(id=post["id"], title=post["title"], body=post["body"], author=post["author"]))
    logger.info("Post`s list responsed")
    return post_objects


# Поиск поста с заданным id
@app.get("/posts/{post_id}")
async def get_post(post_id: int) -> Post:
    logger.info("Post from post`s list requested")
    for post in posts:
        if post["id"] == post_id:
            # конвертируем пост в объект Post
            logger.info("Post from post`s list responsed")
            return Post(**post)
    logger.error("Post not found")
    raise HTTPException(status_code=404, detail="Post not found")


# добавление нового поста
@app.post("/posts", status_code=201)
async def add_post(post: PostCreate) -> Post:
    logger.info("Request to add new post")
    # поиск автора до первого совпадения id
    author = next((user for user in users if user["id"] == post.author_id), None)
    # если автор не найден, вызываем ошибку
    if not author:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    # если автор найден, создаем новый пост
    new_post_id = len(posts) + 1

    new_post = {"id": new_post_id, "title": post.title, "body": post.body, "author": author}
    posts.append(new_post)
    logger.info("New post added")
    return Post(**new_post)


# изменение поста по заданному id
@app.put("/posts/{post_id}", status_code=202)
async def update_post(post: PostUpdate, post_id: int) -> Post:
    logger.info("Request to update post")
    for el in posts:
        if el["id"] == post_id:
            # создаем новый пост и перезаписываем его в списке
            updated_post = {"id": post_id, "title": post.title, "body": post.body, "author": el["author"]}
            posts[posts.index(el)] = updated_post
            logger.info("Post updated")
            return Post(**updated_post)
    logger.error("Post not found")
    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}", status_code=204)
async def delete_post(post_id: int) -> None:
    logger.info("Request to delete post")
    post_not_found = True
    for post in posts:
        if post["id"] == post_id:
            del post
            post_not_found = False
            logger.info("Post deleted")
    if post_not_found:
        logger.error("Post not found")
        raise HTTPException(status_code=404, detail="Post not found")


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_config="core/logging.yaml")

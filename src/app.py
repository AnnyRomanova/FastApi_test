import uvicorn
import yaml
import logging.config


from fastapi import FastAPI, HTTPException
from typing import List

from schemas.database import posts, users
from schemas.model import Post, PostCreate, PostUpdate
from src.core.settings import settings

# импортируем из YAML-файла настройки для логирования
with open("src/core/logging.yaml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

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
@app.get("/posts/{id}")
async def get_post(id: int) -> Post:
    logger.info("Post from post`s list requested")
    for post in posts:
        if post["id"] == id:
            # конвертируем пост в объект Post
            logger.info("Post from post`s list responsed")
            return Post(**post)
    logger.error("Post not found")
    raise HTTPException(status_code=404, detail="Post not found")


# добавление нового поста
@app.post("/post/add", status_code=201)
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
@app.put("/post/update/{id}")
async def update_post(post: PostUpdate, id: int) -> Post:
    logger.info("Request to update post")
    for el in posts:
        if el["id"] == id:
            # создаем новый пост и перезаписываем его в списке
            updated_post = {"id": id, "title": post.title, "body": post.body, "author": el["author"]}
            posts[posts.index(el)] = updated_post
            logger.info("Post updated")
            return Post(**updated_post)
    logger.error("Post not found")
    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/post/delete/{id}")
async def delete_post(id: int) -> List:
    logger.info("Request to delete post")
    for el in posts:
        if el["id"] == id:
            del el
            logger.info("Post deleted")
            return posts
    logger.error("Post not found")
    raise HTTPException(status_code=404, detail="Post not found")


if __name__ == "__main__":
    uvicorn.run("app:app", port=8080)
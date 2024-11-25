import logging

from fastapi import HTTPException

from models.database import users
from schemas.model import Post, PostCreate, PostUpdate

logger = logging.getLogger(__name__)


class PostController:

    def __init__(self, post_db: list) -> None:
        self.post_db = post_db

    def get_posts_list(self) -> list[Post]:
        logger.info("Post`s list requested")
        post_objects = []
        for post in self.post_db:
            # каждый элемент в списке точно соответствует структуре класса Post
            post_objects.append(Post(id=post["id"], title=post["title"], body=post["body"], author=post["author"]))
        logger.info("Post`s list responsed")
        return post_objects

    def get_post(self, post_id: int) -> Post:
        logger.info("Post from post`s list requested")
        if post_id == 0:
            raise ValueError("Cannot get post with id 0")
        for post in self.post_db:
            if post["id"] == post_id:
                # конвертируем пост в объект Post
                logger.info("Post from post`s list responsed")
                return Post(**post)
        logger.error("Post not found")
        raise HTTPException(status_code=404, detail="Post not found")

    def add_post(self, new_post: PostCreate) -> Post:
        logger.info("Request to add new post")
        # поиск автора до первого совпадения id
        author = next((user for user in users if user["id"] == new_post.author_id), None)
        # если автор не найден, вызываем ошибку
        if not author:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        # если автор найден, создаем новый пост
        new_post_id = len(self.post_db) + 1

        new_post = {"id": new_post_id, "title": new_post.title, "body": new_post.body, "author": author}
        self.post_db.append(new_post)
        logger.info("New post added")
        return Post(**new_post)

    def update_post(self, post: PostUpdate, post_id: int) -> Post:
        logger.info("Request to update post")
        for el in self.post_db:
            if el["id"] == post_id:
                # создаем новый пост и перезаписываем его в списке
                updated_post = {"id": post_id, "title": post.title, "body": post.body, "author": el["author"]}
                self.post_db[self.post_db.index(el)] = updated_post
                logger.info("Post updated")
                return Post(**updated_post)
        logger.error("Post not found")
        raise HTTPException(status_code=404, detail="Post not found")

    def delete_post(self, post_id: int) -> None:
        logger.info("Request to delete post")
        post_not_found = True
        for post in self.post_db:
            if post["id"] == post_id:
                del post
                post_not_found = False
                logger.info("Post deleted")
        if post_not_found:
            logger.error("Post not found")
            raise HTTPException(status_code=404, detail="Post not found")


controller: PostController | None = None


def get_post_controller() -> PostController:
    assert controller is not None, "Post controller not initialized"
    return controller

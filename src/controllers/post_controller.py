import logging

from fastapi import HTTPException

from schemas.model import Post, PostCreate

logger = logging.getLogger(__name__)


class PostController:

    def __init__(self, post_db: dict) -> None:
        self.post_db = post_db

    def get_posts_list(self) -> list[Post]:
        logger.info("Post`s list requested")
        return list(self.post_db.values())

    def get_post(self, post_id: int) -> Post:
        logger.info("Post from post`s list requested")
        if post_id not in self.post_db:
            logger.error("Post not found")
            raise HTTPException(status_code=404, detail="Post not found")
        return self.post_db.get(post_id)

    def add_post(self, new_post: PostCreate) -> Post:
        logger.info("Request to add new post")
        user_not_found = True
        for post in self.post_db.values():
            if new_post.author_id == post.author_id:
                user_not_found = False
        if user_not_found:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            next_id = max(self.post_db.keys()) + 1
            post = Post(id=next_id, **new_post.model_dump())
            self.post_db[post.id] = post
            logger.info("New post added")
            return post

    def update_post(self, post: Post, post_id: int) -> Post:
        logger.info("Request to update post")
        post_not_found = True
        for el in self.post_db.values():
            if el.id == post_id:
                post_not_found = False
        if post_not_found:
            raise HTTPException(status_code=404, detail="Post not found")
        else:
            updated_post = Post(id=post_id, title=post.title, body=post.body, author_id=post.author_id)
            self.post_db[post_id] = updated_post
            logger.info("Post updated")
            return updated_post

    def delete_post(self, post_id: int) -> None:
        logger.info("Request to delete post")
        if post_id not in self.post_db:
            raise HTTPException(status_code=404, detail="Post not found")
        self.post_db.pop(post_id)
        logger.info("Post deleted")


controller: PostController | None = None


def get_post_controller() -> PostController:
    assert controller is not None, "Post controller not initialized"
    return controller

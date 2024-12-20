import logging

from fastapi import APIRouter, Depends

from controllers.post_controller import get_post_controller, PostController
from schemas.model import Post, PostCreate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[Post])
async def get_post_list(controller: PostController = Depends(get_post_controller)) -> list[Post]:
    return controller.get_posts_list()


@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int, controller: PostController = Depends(get_post_controller)) -> Post:
    return controller.get_post(post_id)


@router.post("/", response_model=Post, status_code=201)
async def create_post(new_post: PostCreate, controller: PostController = Depends(get_post_controller)) -> Post:
    return controller.add_post(new_post)


@router.put("/{post_id}", response_model=Post, status_code=202)
async def update_post(post: Post, post_id: int, controller: PostController = Depends(get_post_controller)) -> Post:
    return controller.update_post(post, post_id)


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, controller: PostController = Depends(get_post_controller)) -> None:
    controller.delete_post(post_id)

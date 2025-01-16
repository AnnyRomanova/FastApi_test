import logging
from uuid import UUID

from fastapi import APIRouter, Depends

from controllers.post_controller import get_post_controller, PostController
from schemas.model import PostOUT, PostDetail, PostCreate, PostUpdate

# todo переименовать файл на controller

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[PostOUT])
async def get_post_list(controller: PostController = Depends(get_post_controller)) -> list[PostOUT]:
    posts = await controller.get_posts_list()
    return posts


@router.get("/{post_id}", response_model=PostDetail)
async def get_post(post_id: UUID, controller: PostController = Depends(get_post_controller)) -> PostDetail:
    post = await controller.get_post(post_id)
    return post


@router.post("/", status_code=201, response_model=PostDetail)
async def create_post(new_post: PostCreate, controller: PostController = Depends(get_post_controller)) -> PostDetail:
    post = await controller.add_post(new_post)
    return post


@router.put("/{post_id}", response_model=PostOUT, status_code=202)
async def update_post(post: PostUpdate, post_id: UUID,
                      controller: PostController = Depends(get_post_controller)) -> PostOUT:
    post = await controller.update_post(post, post_id)
    return post


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: UUID, controller: PostController = Depends(get_post_controller)) -> None:
    await controller.delete_post(post_id)

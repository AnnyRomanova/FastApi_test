import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from controllers.post_controller import get_post_controller, PostController
from schemas.model import PostOUT, PostDetail, PostCreate, PostUpdate

# todo переименовать файл на controller

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[PostOUT])
async def get_post_list(
        limit: int = Query(20, ge=5, le=100), # limit: от 5 до 100, по умолчанию 20
        offset: int = Query(0, ge=0),  # offset: минимум 0, по умолчанию 0
        search: str | None = Query(None, min_length=1),  # По умолчанию None, минимальная длина строки — 1 символ
        controller: PostController = Depends(get_post_controller)) -> list[PostOUT]:
    posts = await controller.get_posts_list(limit=limit, offset=offset, search=search)
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

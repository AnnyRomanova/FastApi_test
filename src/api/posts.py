import logging
from enum import StrEnum
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from controllers.post_controller import get_post_controller, PostController
from schemas.model import PostOUT, PostDetail, PostCreate, PostUpdate

router = APIRouter()
logger = logging.getLogger(__name__)


# Определяем StrEnum для order_by
class OrderBy(StrEnum):
    CREATED_AT = "created_at"
    ID = "id"
    BODY = "body"


# Модель фильтров
class PostFilters(BaseModel):
    limit: int = Query(20, ge=5, le=100)
    offset: int = Query(0, ge=0)
    search: Optional[str] = Query(None, min_length=1)
    order_by: OrderBy = Query(OrderBy.CREATED_AT)
    descending: bool = Query(False)


@router.get("/", response_model=list[PostOUT])
async def get_post_list(
        filters: PostFilters = Depends(),  # Передаём фильтры через Depends
        controller: PostController = Depends(get_post_controller)
) -> list[PostOUT]:
    posts = await controller.get_posts_list(
        limit=filters.limit,
        offset=filters.offset,
        search=filters.search,
        order_by=filters.order_by.value,
        descending=filters.descending
    )

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

from typing import Optional

from fastapi import Query
from pydantic import BaseModel
from uuid import UUID

from schemas.enums import OrderBy


class Author(BaseModel):
    id: UUID
    name: str
    age: int

    model_config = {
        "from_attributes": True
    }


# проверяет входящий пост для создания нового
class PostCreate(BaseModel):
    title: str
    body: str
    short_body: str
    author_id: UUID

    model_config = {
        "from_attributes": True
    }


# проверяет каждый пост внутри исходящего списка
class PostOUT(BaseModel):
    id: UUID
    title: str
    short_body: str
    author: Author

    model_config = {
        "from_attributes": True
    }


# проверяет исходящий пост, полученный по id
class PostDetail(BaseModel):
    id: UUID
    title: str
    body: str
    author: Author

    model_config = {
        "from_attributes": True
    }


# проверяет входящий пост для обновления данных
class PostUpdate(BaseModel):
    title: str
    short_body: str
    body: str

    model_config = {
        "from_attributes": True
    }


# Модель фильтров
class PostFilters(BaseModel):
    limit: int = Query(20, ge=5, le=100)
    offset: int = Query(0, ge=0)
    search: Optional[str] = Query(None, min_length=1)
    order_by: OrderBy = Query(OrderBy.CREATED_AT)
    descending: bool = Query(False)

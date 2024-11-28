from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


class Post(PostCreate):
    id: int

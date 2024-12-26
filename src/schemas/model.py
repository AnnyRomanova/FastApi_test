from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int

    model_config = {
        "from_attributes": True
    }


class Post(PostCreate):
    id: int

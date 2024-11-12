import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


class PostUpdate(BaseModel):
    title: str
    body: str


users = [
    {"id": 1, "name": "Anna", "age": 28},
    {"id": 2, "name": "Pavel", "age": 63},
    {"id": 3, "name": "Ivan", "age": 44}
]


posts = [
    {"id": 1, "title": "title_1", "body": "body_1", "author": users[1]},
    {"id": 2, "title": "title_2", "body": "body_2", "author": users[0]},
    {"id": 3, "title": "title_3", "body": "body_3", "author": users[2]}
]


# выводит список постов
@app.get("/posts", response_model=List[Post])
def get_posts() -> List[Post]:
    post_objects = []
    for post in posts:
        # каждый элемент в списке точно соответствует структуре класса Post
        post_objects.append(Post(id=post["id"], title=post["title"], body=post["body"], author=post["author"]))
    return post_objects


# Поиск поста с заданным id
@app.get("/posts/{id}")
async def get_post(id: int) -> Post:
    for post in posts:
        if post["id"] == id:
            # конвертируем пост в объект Post
            return Post(**post)
    raise HTTPException(status_code=404, detail="Post not found")


# добавление нового поста
@app.post("/post/add", status_code=201)
async def add_post(post: PostCreate) -> Post:
    # поиск автора до первого совпадения id
    author = next((user for user in users if user["id"] == post.author_id), None)
    # если автор не найден, вызываем ошибку
    if not author:
        raise HTTPException(status_code=404, detail="User not found")
    # если автор найден, создаем новый пост
    new_post_id = len(posts) + 1

    new_post = {"id": new_post_id, "title": post.title, "body": post.body, "author": author}
    posts.append(new_post)

    return Post(**new_post)


# изменение поста по заданному id
@app.put("/post/update/{id}")
async def update_post(post: PostUpdate, id: int) -> Post:
    for el in posts:
        if el["id"] == id:
            # создаем новый пост и перезаписываем его в списке
            updated_post = {"id": id, "title": post.title, "body": post.body, "author": el["author"]}
            posts[posts.index(el)] = updated_post
            return Post(**updated_post)
    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/post/delete/{id}")
async def delete_post(id: int) -> List:
    for el in posts:
        if el["id"] == id:
            del el
            return posts
    raise HTTPException(status_code=404, detail="Post not found")


# if __name__ == "__main__":
#     uvicorn.run("main:app")
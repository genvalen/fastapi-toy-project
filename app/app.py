from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class updatedPost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool] = True
    rating: Optional[int] = None


my_posts = [{"title1": "content1", "id": 1}, {"title2": "content2", "id": 2}]

def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p
    return

def find_id(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return

@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    print(post)
    post = post.model_dump()
    post['id'] = randrange(0, 1000000)

    my_posts.append(post)

    # noramlly we would take the data and save in database
    return {"new post": f"title: {post['title']} content: {post['content']}"}

@app.get("/posts/latest")
async def get_latest_post():
    return my_posts[-1]


@app.get("/posts/{id}")
async def get_post(id: int, response: Response): #path parameters will automatically be returned as string unless otherwise indicated
    post = find_post(id)
    if not post:
        detail = f"post with id {id} not found."
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=detail)

    return (f"post {id}:", post)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_id(id)
    print(id, index)

    if not index:
        detail = f"message: post with id {id} not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def put_post(id: int, post: Post):
    index = find_id(id)
    print(index, id, type(id))

    if not index:
        detail = f"message: post with id {id} not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    new_post = post.model_dump()
    new_post["id"] = id
    my_posts[index] = new_post

    return {"updated post": f"title: {new_post['title']} content: {new_post['content']}"}







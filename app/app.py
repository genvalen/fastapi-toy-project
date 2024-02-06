from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

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

while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', \
            password="password", row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("the database connection failed.")
        print(f"The error was: {error}")
        time.sleep(2)

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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
async def get_post(id: int): #path parameters will automatically be returned as string unless otherwise indicated
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        detail = f"post with id {id} not found."
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=detail)

    return (f"post {id}:", post)

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) \
            VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    created_post = cursor.fetchone()
    conn.commit()
    return {"new post": created_post}

# @app.get("/posts/latest")
# async def get_latest_post():
#     return my_posts[-1]


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        detail = f"message: post with id {id} not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        detail = f"message: post with id {id} was not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    return ({"updated post": updated_post})

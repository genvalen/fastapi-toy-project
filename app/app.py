from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/sqlalchemy")
def test_sql(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', \
            password="password", cursor_factory=RealDictCursor)
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

@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id: int, db : Session = Depends(get_db)): #path parameters will automatically be returned as string unless otherwise indicated
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # if not post:
    #     detail = f"post with id {id} not found."
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=detail)

    # return (f"post {id}:", post)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        detail = f"Post with id {id} was not found.",
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    db.commit()
    db.refresh(post)

    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) \
    #         VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # created_post = cursor.fetchone()
    # conn.commit()
    created_post = models.Post(**post.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

# @app.get("/posts/latest")
# async def get_latest_post():
#     return my_posts[-1]

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db : Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if not deleted_post:
    #     detail = f"message: post with id {id} not found."
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        detail = f"Post with id {id} was not found.",
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.put("/posts/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if not updated_post:
    #     detail = f"message: post with id {id} was not found."
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    # return ({"updated post": updated_post})

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        detail = f"Post with id {id} was not found.",
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

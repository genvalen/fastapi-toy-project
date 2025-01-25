from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],  # related to organizing fastapi docs
)


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=schemas.Post)
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
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", response_model=schemas.Post)
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

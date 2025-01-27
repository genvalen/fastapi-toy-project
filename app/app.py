from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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

# add jwt token

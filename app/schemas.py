from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):  # model for responses.
    id: int
    created_at: datetime

    class config:  # This class enables pydantic to treat sqlalchemy models like dicts.
        orm_mode = True
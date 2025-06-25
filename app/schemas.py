from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserInfo(BaseModel):
    id: int
    email: EmailStr

class Post(PostBase):  # Model for responses.
    id: int
    created_at: datetime
    owner_id: int
    owner: UserInfo
    class config:  # This class enables pydantic to treat sqlalchemy models like dicts.
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserInfo):
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

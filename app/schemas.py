from pydantic import BaseModel
from typing import Optional, List


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        from_attributes = True

class ResponseBlog(BaseModel):
    id: int
    title: str
    body: str
    published: Optional[bool]

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
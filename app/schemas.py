from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True


class ResponseBlog(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True
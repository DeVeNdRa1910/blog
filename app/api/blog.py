from fastapi import APIRouter, Request
from ..schemas import Blog
router = APIRouter()

@router.post("/")
def create_blog(blog: Blog):
    print(blog)
    return {"data": f"Blos is created with title as {blog.title}"}
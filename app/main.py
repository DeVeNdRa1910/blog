from fastapi import FastAPI
from app.api import user, blog


app = FastAPI()


app.include_router(user.router, prefix="/user", tags=["tags"])
app.include_router(blog.router, prefix='/blog', tags=["blogs"])
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api import user, blog
from . import models
from .db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.router, prefix="/user", tags=["users"])
app.include_router(blog.router, prefix='/blog', tags=["blogs"])
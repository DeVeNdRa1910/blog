from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api import user, blog, auth
from . import models
from .db import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],          
)


app.include_router(auth.router, prefix='/auth', tags=["Authentication"])
app.include_router(user.router, prefix="/user", tags=["Users"])
app.include_router(blog.router, prefix='/blog', tags=["Blogs"])
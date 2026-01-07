from fastapi import FastAPI
from api import user, blog


app = FastAPI()


app.include_router(user.router, prefix="/user", tags=["tags"])
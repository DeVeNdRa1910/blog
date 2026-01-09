from fastapi import APIRouter, Depends
from ..schemas import Blog
from ..db import get_db
from sqlalchemy.orm import Session
from app import models

router = APIRouter()

@router.post("/")
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
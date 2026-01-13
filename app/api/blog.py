from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import Blog, ResponseBlog, UserResponse
from app.db import get_db
from sqlalchemy.orm import Session
from app import models
from typing import List
from ..utils.oauth2 import get_current_user

router = APIRouter()

# If need current user then we can call get_currrent_user in the function parameters, and if dont need the current user then we can pass get_current_user in the decorator

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    
    # Implement a check for user existance
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to fetch logged in user")
    new_blog = models.Blog(title=request.title, body=request.body, user_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ResponseBlog])
def get_all_the_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/me", status_code=status.HTTP_200_OK)
def get_blogs_of_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to fetch logged in user")
    blogs = db.query(models.Blog).filter(models.Blog.user_id == user.id).all()
    if len(blogs) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No blogs are created yet")
    return blogs

@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=ResponseBlog, dependencies=[Depends(get_current_user)])
def get_blog_by_id(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog details is not avaiolable for id: {blog_id}")
    return blog

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def delete_blog_by_id(blog_id, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    # or
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id={blog_id} doest not exist")
    db.delete(blog)
    db.commit()
    return {"detail": f"blog with id={blog_id} deleted successfully"}    

@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_current_user)])
def update_blog_by_id(blog_id, request: Blog, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id).update(request, synchronize_session=False)
    # or
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id={blog_id} doest not exist")
    blog.title = request.title
    blog.body = request.body
    blog.published=request.published
    db.commit()
    db.refresh(blog)
    return blog
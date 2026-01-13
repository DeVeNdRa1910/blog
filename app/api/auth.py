from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import Login, UserCreate, Token, UserResponse
from app import models
from app.db import get_db
from sqlalchemy.orm import Session
from app.utils.JWTtoken import create_access_token
from datetime import timedelta
from typing import Annotated
from app.utils.oauth2 import get_current_active_user
from app.utils.password import get_password_hash, verify_password

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 8*60

@router.post('/login')
def login(request: Login, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    is_password_matched = verify_password(request.password, user.password)
    
    if not user or not is_password_matched:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post('/signin', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    isUserExist = db.query(models.User).filter(models.User.email == request.email).first()
    hassed_password = get_password_hash(request.password)
        
    if isUserExist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email already exists")
        
    new_user = models.User(name=request.name, email=request.email, password=hassed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
        
    return new_user

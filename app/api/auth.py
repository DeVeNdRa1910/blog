from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import Login
from app import models
from app.db import get_db
from sqlalchemy.orm import Session
from .user import verify_password
from ..utils.JWTtoken import create_access_token
from datetime import timedelta
from ..schemas import Token, UserResponse
from typing import Annotated
from ..utils.oauth2 import get_current_active_user

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

@router.get('/user/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_loggedin_users_details(current_user: Annotated[UserResponse, Depends(get_current_active_user)]):
    print(current_user)
    return current_user

from fastapi import APIRouter, Depends, HTTPException, status
from app import models
from app.schemas import UserUpdate, UserResponse
from app.db import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from ..utils.oauth2 import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_loggedin_users_details(db:Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

@router.get('/', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).all()
        
        if not users:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Failed get users")
        
        return users
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Failed get users")
    
@router.get('/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def get_user_by_id(user_id, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        blogs = db.query(models.Blog).filter(models.Blog.user_id == user_id).all()
        return user
    except:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.delete('/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def delete_user_by_id(user_id, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db.delete(user)
        db.commit()
        db.refresh(user)
    except: 
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found")
    
@router.patch('/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def update_partial_user_data(user_id, request: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if request.name is not None:
            user.name = request.name
        
        if request.email is not None:
            user.email = request.email
        
        db.commit()
        db.refresh(user)
        
        return {
            "message": "User data updated successfully",
            "user": user
        }
    
    except:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.put("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def update_complete_user_data(user_id, request: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = request.name
    user.email = request.email

    db.commit()
    db.refresh(user)

    return user
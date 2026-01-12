from fastapi import APIRouter, Depends, HTTPException, status
from app import models
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.db import get_db
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
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

@router.get('/', status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).all()
        
        if not users:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Failed get users")
        
        return users
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Failed get users")
    
@router.get('/{user_id}', status_code=status.HTTP_200_OK)
def get_user_by_id(user_id, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
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
    
@router.patch('/{user_id}', status_code=status.HTTP_200_OK)
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
    
@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_complete_user_data(user_id, request: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = request.name
    user.email = request.email

    db.commit()
    db.refresh(user)

    return user
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .JWTtoken import verify_token
from typing import Annotated
from ..schemas import UserResponse

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if credentials is None:
        raise credentials_exception

    token = credentials.credentials

    return verify_token(token, credentials_exception)

def get_current_active_user(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    print(current_user)
    return current_user
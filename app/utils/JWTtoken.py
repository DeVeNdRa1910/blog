from fastapi import Depends
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from typing import Optional, Annotated
from ..schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
import os

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = 60):
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: Annotated[str, Depends(oauth2_scheme)], credentials_exception):
    credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception
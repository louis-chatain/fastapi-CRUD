from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import JWTError
from jose import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db import db_user
from db.database import get_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'b741de98ca5744033d5c521b744775195a5ba61fbd215bb2429718c772adfd76'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )
  credentials_exception2 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could not validate credentials 2",
    headers={"WWW-Authenticate": "Bearer"}
  )
  credentials_exception3 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could not validate credentials 3",
    headers={"WWW-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except JWTError as e:
        if str(e) == "Signature has expired.":
                raise credentials_exception2
        elif str(e) == "Not enough segments":
                raise HTTPException(
                    detail='Wrong Token or missing',
                    status_code=status.HTTP_400_BAD_REQUEST,
                    headers={"WWW-Authenticate": "Bearer"})
        else:
                raise HTTPException(detail='Not manager authenticated error', status_code=status.HTTP_400_BAD_REQUEST)
  
  user = db_user.read_user_by_username(username, db)

  if user is None:
    raise credentials_exception3
  
  return user
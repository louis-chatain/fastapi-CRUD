from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from auth import oauth2
from db.database import get_db
from db.hash import Hash
from db.models import DbUser

router = APIRouter(tags=["authentication"])
 
@router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.")
    if not Hash.verify_hashed_pwd(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password")
    
    acces_token = oauth2.create_access_token(data={"sub": user.username})

    return {
        "acces_token": acces_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }
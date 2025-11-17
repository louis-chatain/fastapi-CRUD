from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db import db_article
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay, UserBase
from auth.oauth2 import get_current_user


router = APIRouter(prefix="/article", tags=["article"])


@router.post("/new", response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db)):
    return db_article.create_article(request, db)


@router.get("/read_all", response_model=List[ArticleDisplay])
def read_all(db: Session = Depends(get_db)):
    return db_article.read_all(db)


@router.get("/{id}")#, response_model=ArticleDisplay)
def read_article(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        "data": db_article.read_article(id, db),
        "current_user_user_name": current_user.username,
        "current__user_email": current_user.email,
        "current_user_id": current_user.id
    }


@router.post("/{id}/update", response_model=ArticleDisplay)
def update_article(id: int, request: ArticleBase, db: Session = Depends(get_db)):
    return db_article.update_article(id, request, db)


@router.post("/{id}/delete")
def delete_article(id: int, db: Session = Depends(get_db)):
    return db_article.delete_article(id, db)

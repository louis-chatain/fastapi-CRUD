from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from db.models import DbArticle
from exceptions import StoryException
from schemas import ArticleBase

def create_article(request: ArticleBase, db: Session):
    if request.content.startswith("Il etait une fois, "):
        raise StoryException("No story here please.")
    new_article = DbArticle(
        title = request.title,
        content = request.content,
        published = request.published,
        user_id = request.creator_id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def read_all(db: Session):
    article = db.query(DbArticle).all()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No article found.")
    return article


def read_article(id: int, db: Session):
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article id {id} not found.")
    return article


def update_article(id: int, request: ArticleBase, db: Session):
    article = db.query(DbArticle).filter(DbArticle.id == id)
    if not article.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article id {id} not found.")
    article.update({
        DbArticle.title: request.title,
        DbArticle.content: request.content,
        DbArticle.published: request.published,
        DbArticle.user_id: request.creator_id
    })
    db.commit()
    updated_article = article.first()
    return updated_article


def delete_article(id: int, db: Session):
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article id {id} not found.")
    db.delete(article)
    db.commit()
    return {"data": article}
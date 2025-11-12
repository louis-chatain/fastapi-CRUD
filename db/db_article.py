from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from db.models import DbArticle
from schemas import ArticleBase

def create_article(request: ArticleBase, db: Session):
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
    return article

def read_article(id: int, db: Session):
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    return article


def update_article(id: int, request: ArticleBase, db: Session):
    article = db.query(DbArticle).filter(DbArticle.id == id)
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
    db.delete(article)
    db.commit()
    return {"data": article}
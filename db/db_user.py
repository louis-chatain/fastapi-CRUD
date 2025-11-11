from sqlalchemy.orm.session import Session
from db.models import DbUser
from schemas import UserBase
from db.hash import Hash

def create_user(request: UserBase, db: Session):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        hashed_password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def read_all(db: Session):
    return db.query(DbUser).all()


def read_user(id: int, db: Session):
    return db.query(DbUser).filter_by(id=id).first()


def update_user(id: int, request: UserBase, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.hashed_password: Hash.bcrypt(request.password)
    })
    db.commit()
    updated_user = user.first()
    return updated_user


def delete_user(id: int, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return user
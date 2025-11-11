from typing import List
from fastapi import APIRouter, Depends
from db.database import get_db
from db import db_user
from sqlalchemy.orm.session import Session
from schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/new", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(request, db)

@router.get("/read_all", response_model=List[UserDisplay])
def read_all(db: Session = Depends(get_db)):
    return db_user.read_all(db)


@router.get("/{id}", response_model=UserDisplay)
def read_user(id: int, db: Session = Depends(get_db)):
    return db_user.read_user(id, db)

@router.post("/{id}/update", response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return db_user.update_user(id, request, db)


@router.post("/{id}/delete", response_model=UserDisplay)
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(id, db)
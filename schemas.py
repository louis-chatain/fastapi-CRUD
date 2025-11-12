from typing import List
from pydantic import BaseModel


# Article inside UserDisplay
class Article(BaseModel):
    title: str
    content: str
    published: bool
    class Config():
        orm_mode = True


class UserBase(BaseModel):  # data that we will receive from the user
    username: str
    email: str
    password: str

class UserDisplay(BaseModel): # data that we will send back to the user
    username: str               # sends back only username and email in
    email: str                  # the response body in the docs
    id: int
    items: List[Article] = []
    class Config():
        orm_mode = True

# user inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str
    class Config():
        orm_mode = True

class ArticleBase(BaseModel):  # data that we will receive from the user
    title: str
    content: str
    published: bool
    creator_id: int = 2

class ArticleDisplay(BaseModel): # data that we will send back to the user
    id: int
    title: str                      # sends back only username and email in
    content: str                      # the response body in the docs
    published: bool
    user: User
    class Config():
        orm_mode = True
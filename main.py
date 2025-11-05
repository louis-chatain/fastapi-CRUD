from enum import Enum
from fastapi import FastAPI

app = FastAPI()

@app.get('/Hello')
def index():
    return {"message" : "Hello World!"}

# @app.get('/blog/all')
# def all_blog():
#     return {"message" : "you are seeing all blogs!"}

@app.get('/blog/all')
def all_blog(page: int, page_size: float):
    return {"message" : f"you are seeing all blogs on page {page} with the page size at {page_size} !"}

class Blogtype(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blog/type/{type}')
def get_blog_type(type: Blogtype):
    return {"message" : f"you are seeing blogs with the type: {type}"}

@app.get('/blog/{id}')
def get_blog(id: int):
    return {"message" : f"Hello user with id: {id}"}
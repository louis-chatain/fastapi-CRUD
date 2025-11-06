from enum import Enum
from typing import Optional
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get('/Hello', tags=['hello'])
def index():
    return {"message" : "Hello World!"}

# @app.get('/blog/all')
# def all_blog():
#     return {"message" : "you are seeing all blogs!"}

@app.get('/blog/all', tags=['blog'])
def all_blog(page: int = 1, page_size: Optional[float] = None):
    return {"message" : f"you are seeing all blogs on page {page} with the page size at {page_size} !"}

@app.get('/blog/{blog_id}/comments/{comment_id}', tags=['blog', 'comment'])
def get_comment(blog_id : int, comment_id : int, username : Optional[str] = None, valid : bool = True):
    return {"message" : f"Comment N°{comment_id} under the blog N°{blog_id} from {username}. {valid}"}

class Blogtype(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blog/type/{type}', tags=['blog', 'type'])
def get_blog_type(type: Blogtype):
    return {"message" : f"you are seeing blogs with the type: {type}"}

@app.get('/blog/{id}', tags=['blog'])
def get_blog(id: int, response: Response):
    if id == 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error" : f"blog {id} not found :("}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message" : f"Hello user with id: {id}"}
from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends ,Response, status

router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

def function_we_are_gonna_use_again_and_again():
    return {"req" : "Hello everynya!"}

# @app.get('/blog/all')
# def all_blog():
#     return {"message" : "you are seeing all blogs!"}


@router.get(
    "/all",
    summary="Retreive all blogs",
    description="This API call simulates fetching all blogs.",
    response_description="The list of available blogs.",
)
def all_blog(page: int = 1, page_size: Optional[float] = None):
    return {
        "message": f"you are seeing all blogs on page {page} with the page size at {page_size} !"
    }


@router.get("/{blog_id}/comments/{comment_id}", tags=["comment"])
def get_comment(
    blog_id: int, comment_id: int, username: Optional[str] = None, valid: bool = None
):
    """
    Simulates retreiving a comment of a blog

    - **blog_id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **username** optional query parameter
    - **valid** optional query parameter
    """
    return {
        "message": f"Comment N°{comment_id} under the blog N°{blog_id} from {username}. {valid}"
    }


class Blogtype(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"


@router.get("/type/{type}")
def get_blog_type(type: Blogtype, req_parameter: dict = Depends(function_we_are_gonna_use_again_and_again)):
    return {"message": f"you are seeing blogs with the type: {type}", "req_paramater" : req_parameter}


@router.get("/{id}")
def get_blog(id: int, response: Response):
    if id == 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"blog {id} not found :("}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Hello user with id: {id}"}
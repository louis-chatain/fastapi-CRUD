from typing import Dict, List, Optional
from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel

router = APIRouter(prefix="/blog", tags=["blog"])


class Image(BaseModel):
    url: str = "Desktop/dontlookintothisfolder/"
    alias: str = "freakyahhphoto.png"


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {
        "key of the DAMN value": " generic tones: 'Hello, i am the value.'"
    }
    image: Optional[Image]


@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {"id": id, "data": blog, "version": version}

# Query, Body and Path are dependency functions from FastAPI
# that tell the framework WHERE to look
# for the data in the HTTP request and HOW to validate it.
@router.post("/new/{id}/comment/{comment_id}")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: str = Query(
        None,
        title="title of the comment.",  # je sais pas a quoi sa sert.
        description="Some desc of the comment title.",
        alias="commentTitle",  # sa remplace ce qui a ecrit dans l'url
        deprecated=True,
    ),
    # content: str = Body("Hi, default value of this variable!") # provide a default value for this viariable, making it optional
    content: str = Body(
        Ellipsis,           # \
        min_length=10,      #  } Validators : each of those validators put a restrain on the value,
        max_length=50,      #  }              once all respected the value is valid.
        regex="^[a-z\s]*$", # /
    ),
    v: Optional[List[str]] = Query(
        ["1.0", "1.1", "1.2", "1.3"],
        alias="Version",
        description="list of str that represent different version with default value from 1.0 to 1.3",
    ),
    comment_id: int = Path(ge=1, le=999),
):
    return {
        "blog": blog,
        "id": id,
        "comment_title": comment_title,
        "content": content,
        "version": v,
        "comment_id": comment_id,
    }

from fastapi import APIRouter

router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

@router.post("/news")
def create_blog():
    pass
from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse
from db.models import Base
from db.database import engine
from exceptions import StoryException
from router import article, get_blog, post_blog, user, product


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})
app.include_router(get_blog.router)
app.include_router(post_blog.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)

favicon_path = "favicon.ico"


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"detail": exc.name}
    )


# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/", summary="Says 'Hello world!'", tags=["hello"])
def index():
    return {"message": "Hello World!"}


Base.metadata.create_all(engine)

from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from db.models import Base
from db.database import engine
from exceptions import StoryException
from router import article, file, get_blog, post_blog, user, product
from auth import authentication
from templates import templates


app = FastAPI(title="Learning FastApi", swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})
app.include_router(get_blog.router)
app.include_router(post_blog.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(templates.router)
favicon_path = "favicon.ico"


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"detail": exc.name}
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/", summary="Says 'Hello world!'", tags=["hello"])
def index():
    return {"message": "Hello World!"}


Base.metadata.create_all(engine)

app.mount("/files", StaticFiles(directory="files"), name="files") #makes files statically available
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")
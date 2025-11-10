from fastapi import FastAPI
from fastapi.responses import FileResponse
from db.models import Base
from db.database import engine
from router import get_blog, post_blog, user


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})
app.include_router(get_blog.router)
app.include_router(post_blog.router)
app.include_router(user.router)

favicon_path = "favicon.ico"


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/", summary="Says 'Hello world!'", tags=["hello"])
def index():
    return {"message": "Hello World!"}

Base.metadata.create_all(engine)

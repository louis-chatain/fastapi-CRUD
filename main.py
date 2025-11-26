import time
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response, WebSocket, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
from db.models import Base
from db.database import engine
from exceptions import StoryException
from router import article, dependencies, file, get_blog, ocr, post_blog, user, product
from auth import authentication
from templates import templates
from client import html


app = FastAPI(
    title="Learning FastApi",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)
app.include_router(get_blog.router)
app.include_router(post_blog.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(templates.router)
app.include_router(dependencies.router)
app.include_router(ocr.router)
favicon_path = "favicon.ico"


# --- Lifecycle Management (Initializes/Closes httpx.AsyncClient) ---

@app.on_event("startup")
async def startup_event():
    """Initializes the shared asynchronous HTTP client."""
    # Store the client instance on the app's state for routers to access
    app.state.http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully closes the client connection pool."""
    # Access the stored client and close it
    await app.state.http_client.aclose()


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT, content={"detail": exc.name}
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/hello", summary="Says 'Hello world!'", tags=["hello"])
def index():
    return {"message": "Hello World!"}


@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next: Callable[[Request],
    Awaitable[Response]]
) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["Process-Time"] = str(process_time)
    return response


Base.metadata.create_all(engine)

app.mount(
    "/files", StaticFiles(directory="files"), name="files"
)  # makes files statically available
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")

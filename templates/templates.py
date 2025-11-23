from log.custom_log import log
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas import ProductBase


router = APIRouter(prefix="/templates", tags=["templates"])

templates = Jinja2Templates(directory="templates")


@router.post("/products/{id}", response_class=HTMLResponse)
def get_product(id: int, product: ProductBase, request: Request, bt: BackgroundTasks):
    bt.add_task(log_template_call, f"template read for product with id {id}")
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "id": id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
        },
    )


def log_template_call(message: str):
    log("MyApi", message)

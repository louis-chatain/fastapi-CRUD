
from turtle import title
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas import ProductBase


router = APIRouter(prefix="/templates", tags=["templates"])

templates = Jinja2Templates(directory="templates")

@router.post("/poducts/{id}", response_class=HTMLResponse)
def get_product(id: int, product: ProductBase, request: Request):
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "id" : id,
            "title": product.title,
            "description": product.description,
            "price": product.price
        }
    )
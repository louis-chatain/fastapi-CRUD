from fastapi import APIRouter, Depends, Request
from log.custom_log import log


router = APIRouter(prefix="/dependencies", tags=["dependencies"], dependencies=[Depends(log)])


# Depends() does not seems to work very well with functions but pretty with variables in classes(i didn't do classes with function so dont know about that)


def convert_params(request: Request, separator: str = "|---|"):
    query = []
    for key, value in request.query_params.items():
        query.append(f"{key} {separator} {value}")
    return query


def convert_headers(request: Request, separator: str = "", query = Depends(convert_params)):
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f"{key} {separator} {value}")
    return {
        "headers": out_headers,
        "query": query
    }

@router.get("")
def get_items(separator: str = "newseparator", headers = Depends(convert_headers)):
    return{
        "items": ["a", "b", "c"],
        "headers": headers
    }

@router.post("new")
def create_item(headers = Depends(convert_headers)):
    return {
        "result": "a new item",
        "headers": headers
    }

class Account:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

@router.post("/user")
def create_user(name: str, email: str, account: Account = Depends(Account)):
    return {
        "name": name,
        "email": email,
        "account": account
    }
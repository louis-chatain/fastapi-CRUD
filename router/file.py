from fastapi import APIRouter, File

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.post("")
def get_file(file: bytes = File(Ellipsis)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines": lines}
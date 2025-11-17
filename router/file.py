import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

router = APIRouter(prefix="/file", tags=["file"])


@router.post("/uploadFile")
def upload_file(
    upload_file: UploadFile = File(Ellipsis),
):  # if a new uploaded file has the same name as a saved one, it will replaced it, not good.
    file_location = f"files/{upload_file.filename}"
    with open(file_location, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {
        "filename": upload_file.filename,
        "type": upload_file.content_type,
        "info": f"file '{upload_file.filename}' saved at '{file_location}'",
    }

@router.get("/download/{name}", response_class=FileResponse)
def get_file(name: str):
    path = f"files/{name}"
    return path
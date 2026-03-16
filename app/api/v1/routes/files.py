from fastapi import APIRouter, File, UploadFile
from typing import Annotated, List

router = APIRouter(
    prefix="/files",
    tags=["files"]
)


@router.post("/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

# upload file 
@router.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    return {"file_name": file.filename, "type": file.content_type, "file_size": (file.size)}

# save file
@router.post("/save")
async def save_file(file: UploadFile = File(...)):
    with open(f'uploads/{file.filename}', "wb") as f:
        f.write(file.file.read())
    return {"message": f"File {file.filename} saved successfully"}

# upload multiple files
@router.post("/upload-files")
async def save_file(files: List[UploadFile] = File(...)):
    for file in files:
        with open(f'uploads/{file.filename}', "wb") as f:
            f.write(file.file.read())
    return {"filenames": [f"File {file.filename} saved successfully" for file in files]}


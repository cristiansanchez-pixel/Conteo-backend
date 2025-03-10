from fastapi import APIRouter, File, UploadFile, Response
from ..models.file_model import FileModel
from ..controllers.file_controller import FileController
from pathlib import Path

router = APIRouter()


@router.post("/uploadfile", summary="Upload a file")
async def upload_file(
    response: Response,
    file: UploadFile = File(...)  # Asegurar que se define como UploadFile
):
    res = await FileController().upload_file(file)

    if res == "File too large":
        response.status_code = 413
        return {"error": "File too large"}

    if res == "File type not allowed":
        response.status_code = 415
        return {"error": "File type not allowed"}

    if res == "Data incorrecta o faltan columnas en el Excel.":
        response.status_code = 422
        return {"error": res}

    if isinstance(res, dict) and not res.get("success"):
        response.status_code = 500
        return res

    response.status_code = 200
    return {"message": "File uploaded successfully"}


# @router.post("/uploadfile", summary = "Upload a file")
# async def upload_file(
#     response: Response,
#     file: UploadFile = File(...),
# ):
    

#     res = await FileController().upload_file(file)
#     if res == "File too large":
#         response.status_code = 413
#         return {"error": "File too large"}

#     if res == "File type not allowed":
#         response.status_code = 415
#         return {"error": "File type not allowed"}

#     if res is None:
#         response.status_code = 500
#         return {"error": "Internal server error"}

#     response.status_code = 200
#     return {"message": "File uploaded successfully"}
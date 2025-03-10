from fastapi import APIRouter, File, UploadFile, Response
from ..models.file_model import FileModel
from ..controllers.file_controller import FileController
from pathlib import Path

router = APIRouter()



@router.post("/uploadfile/{id_inventario}", summary = "Upload a file")
async def upload_file(
    response: Response,
    id_inventario = "{id_inventario}",
    file: UploadFile = File(...),
):
    
    print(f"ID Inventario recibido: {id_inventario}")
    res = await FileController().upload_file(file, id_inventario)
    if res == "File too large":
        response.status_code = 413
        return {"error": "File too large"}

    if res == "File type not allowed":
        response.status_code = 415
        return {"error": "File type not allowed"}

    if res is None:
        response.status_code = 500
        return {"error": "Internal server error"}

    response.status_code = 200
    return {"message": "File uploaded successfully"}
from fastapi import APIRouter, Response, HTTPException
from ..models.perfil_model import CreatePerfil, UpdatePerfilModel, ConsultPerfilModel
from ..controllers.perfil_controller import PerfilController
# Importamos la clase correctamente

router = APIRouter()

@router.post("/crearperfiles", summary="Create a profile")
async def create_perfil(perfil: CreatePerfil, response: Response):
    """Crea un nuevo perfil con validación de nombre"""
    res = await PerfilController().create_perfil(perfil)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res

@router.get("/perfiles", summary="Listar todos los perfiles")
async def get_all_perfiles():
    return await PerfilController().get_all_perfiles()

@router.put("/perfiles/{id_perfil}")
async def actualizar_perfil(id_perfil: str, perfil: UpdatePerfilModel, response: Response):
    """Actualiza un perfil por su ID"""
    res = await PerfilController().update_perfil(id_perfil, perfil)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res

@router.get("/perfiles/{id_perfil}", response_model=ConsultPerfilModel)
async def obtener_perfil(id_perfil: str):
    """Obtiene un perfil por su ID"""
    perfil = await PerfilController().get_perfil_by_id(id_perfil)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

@router.delete("/perfil/{id_perfil}", summary="Eliminar un perfil")
async def delete_perfil(id_perfil: str, response: Response):
    res = await PerfilController().delete_perfil(id_perfil)
    if res:
        response.status_code = 200
        return {"message": "Perfil eliminado correctamente"}
    raise HTTPException(status_code=400, detail="Error al eliminar el perfil")

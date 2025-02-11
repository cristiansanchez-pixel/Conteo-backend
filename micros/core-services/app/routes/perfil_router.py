from fastapi import APIRouter, Response, HTTPException
from ..models.perfil_model import CreatePerfilModel, UpdatePerfilModel, ConsultPerfilModel
from ..controllers.perfil_controller import PerfilController
# Importamos la clase correctamente

router = APIRouter()

@router.post("/crearperfiles", summary="Create a profile")
async def create_perfil(perfil: CreatePerfilModel, response: Response):
    """Crea un nuevo perfil con validación de nombre"""
    res = await PerfilController().create_perfil(perfil)
    response.status_code = 200 if res else 404
    return res

@router.put("/perfiles/{id_perfil}")
async def actualizar_perfil(id_perfil: str, perfil: UpdatePerfilModel):
    """Actualiza un perfil por su ID"""
    res = await PerfilController().update_perfil(id_perfil, perfil)
    if not res:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"message": "Perfil actualizado correctamente"}

@router.get("/perfiles/{id_perfil}", response_model=ConsultPerfilModel)
async def obtener_perfil(id_perfil: str):
    """Obtiene un perfil por su ID"""
    perfil = await PerfilController().get_perfil_by_id(id_perfil)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

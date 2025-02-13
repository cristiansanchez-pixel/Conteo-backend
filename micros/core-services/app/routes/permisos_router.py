from fastapi import APIRouter, Response
from ..controllers.permisos_controller import PermisosController
from ..models.permisos_model import CreatePermisos, CreatePermisoPerfil

router = APIRouter()

@router.post("/Permiso", summary="Create a permisos")
async def create_permiso(permiso: CreatePermisos, response: Response):
    res = await PermisosController().create_permiso(permiso)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res

@router.get("/Permisos", summary="Get all permisos")
async def get_all_permisos(response: Response):
    res = await PermisosController().get_all_permisos()
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res

@router.post("/permissionAllData", summary="Create a new permission")
async def create_permiso_perfil(
    response: Response, ip: str, data: CreatePermisoPerfil
):
    res = await PermisosController().create_permiso_perfil(ip, data)
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res
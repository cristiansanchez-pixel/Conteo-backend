from fastapi import APIRouter, Response, Depends
from ..controllers.permisos_controller import PermisosController
from ..models.permisos_model import CreatePermisos
from ..utils.authJwt import get_current_user

router = APIRouter()

@router.post("/createPermiso", summary="Create a permisos", response_model=CreatePermisos)
async def create_permiso(permiso: CreatePermisos, response: Response, current_user: dict = Depends(get_current_user)):
    res = await PermisosController().create_permiso(permiso)
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res

@router.get("/Permisos", summary="Get all permisos", response_model=CreatePermisos)
async def get_all_permisos(response: Response, currect_user: dict = Depends(get_current_user)):
    res = await PermisosController().get_all_permisos()
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res

# @router.post("/permissionAllData", summary="Create a new permission")
# async def create_permiso_perfil(
#     response: Response, ip: str, data: CreatePermisoPerfil
# ):
#     res = await PermisosController().create_permiso_perfil(ip, data)
#     if res:
#         response.status_code = 200
#     else:
#         response.status_code = 400
#     return res
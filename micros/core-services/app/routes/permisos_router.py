from fastapi import APIRouter, Response
from ..controllers.permisos_controller import PermisosController
from ..models.permisos_model import CreatePermisosModel, CreateAllDataForPermission

router = APIRouter()

@router.post("/Permiso", summary="Create a permisos")
async def create_permiso(permiso: CreatePermisosModel, response: Response):
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

@router.post("/permissionAllData", summary="Create a new permission with all data")
async def create_permission_all_data(
    response: Response, ip: str, data: CreateAllDataForPermission
):
    res = await PermisosController().create_permission_all_data(ip, data)
    if res:
        response.status_code = 200
    else:
        response.status_code = 400
    return res
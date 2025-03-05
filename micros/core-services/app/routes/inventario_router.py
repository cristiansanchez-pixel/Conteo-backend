from fastapi import APIRouter, Response, Query, Path, HTTPException
from ..controllers.inventario_controller import InventarioController
from ..models.inventario_model import CreateInventarioModel, UpdateInventarioModel, ConsultInventarioModel
from ..models.paginator_model import PaginatorSearch


router = APIRouter()


@router.post("/createInventario", summary="Create an inventory")
async def create_inventario(inventario: CreateInventarioModel, response: Response):
    res = await InventarioController().create_inventario(inventario)
    if "error" not in res:  # Verifica si no hubo un error
        response.status_code = 200  # Código 201 para "Creado"
    else:
        response.status_code = 400  # Código 400 para "Solicitud Incorrecta"
    return res
  
@router.get("/inventarios", summary="Get inventory by id")
async def get_inventario_by_id(response: Response, id_inventario: str):
  res = await InventarioController().get_inventario_by_id(id_inventario)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res

@router.get("/getAllInventarios", summary="Get all inventories")
async def get_all_inventarios(
  response: Response, 
  filter: str = None, 
  order_by: str = Query(None, regex="^(nombre_inventario|cantidad_productos)$"), 
  order: str = Query(None, regex="^(ASC|DESC)$"),
  current_page: int = Query(1, ge=1),
  page_size: int = Query(20, ge=1) 
  ):
    
    res = await InventarioController().get_all_inventarios(filter, order_by, order, current_page, page_size)
    if "error" in res:
        response.status_code = 400
    else:
        response.status_code = 200
    return res


@router.put("/inventarios/{id_inventario}", summary="Update inventory")
async def update_inventario(
    id_inventario: int,
    request: UpdateInventarioModel
):
  
    id_usuario = request.id_usuario
    nombre_inventario = request.nombre_inventario
    res = await InventarioController().update_inventario(id_inventario, id_usuario, nombre_inventario)
    
    if not res:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el inventario")
    
    return {"message": "Inventario actualizado correctamente", "data": res}

@router.delete("/deleteInventario/{id_inventario}", summary="Delete inventory")
async def delete_inventario(id_inventario: str, response: Response):
  res = await InventarioController().delete_inventario(id_inventario)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res

@router.get("/dashboard/{id_inventario}", summary="Get inventory dashboard")
async def get_inventarios_dashboard(id_inventario: str, response: Response):
    res = await InventarioController().get_inventarios_dashboard(id_inventario)
    if "error" in res:
        response.status_code = 400
    else:
        response.status_code = 200
    return res
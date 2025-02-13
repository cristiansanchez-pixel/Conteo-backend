from fastapi import APIRouter, Response
from ..controllers.inventario_controller import InventarioController
from ..models.inventario_model import CreateInventarioModel, UpdateInventarioModel, ConsultInventarioModel

router = APIRouter()

@router.post("/createInventario", summary="Create an inventory")
async def create_inventario(inventario: CreateInventarioModel, response: Response):
    res = await InventarioController().create_inventario(inventario)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res
  
@router.get("/inventarios/{id_inventario}", summary="Get inventory by id")
async def get_inventario_by_id(response: Response, id_inventario: str):
  res = await InventarioController().get_inventario_by_id(id_inventario)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res

@router.put("/inventarios/{id_inventario}", summary="Update inventory")
async def update_inventario(id_inventario: str, inventario: UpdateInventarioModel, response: Response):
  res = await InventarioController().update_inventario(id_inventario, inventario)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res

@router.delete("/inventarios/{id_inventario}", summary="Delete inventory")
async def delete_inventario(id_inventario: str, response: Response):
  res = await InventarioController().delete_inventario(id_inventario)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res
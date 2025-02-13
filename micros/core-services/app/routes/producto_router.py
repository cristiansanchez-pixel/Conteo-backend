from fastapi import APIRouter, Response
from ..controllers.producto_controller import ProductController
from ..models.producto_model import CreateProductoModel, UpdateProductoModel, ConsultProductoModel

router = APIRouter()

@router.post("/createProducto", summary="Create a product")
async def create_producto(producto: CreateProductoModel, response: Response):
    res = await ProductController().create_producto(producto)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res
  
@router.get("/getProductsByid/{id_producto}", summary="Get product by id")
async def get_producto_by_id(response: Response, id_producto: str):
  res = await ProductController().get_producto_by_id(id_producto)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res

@router.put("/updateProducto/{id_producto}", summary="Update product")
async def update_producto(id_producto: str, producto: UpdateProductoModel, response: Response):
  res = await ProductController().update_producto(id_producto, producto)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res
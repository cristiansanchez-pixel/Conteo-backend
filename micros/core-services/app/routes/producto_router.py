from fastapi import APIRouter, Response, Request
from ..controllers.producto_controller import ProductController
from ..models.producto_model import CreateProductoModel, UpdateProductoModel, ConsultProductoModel, ConsultAllProductoModel

router = APIRouter()

@router.post("/createProducto", summary="Create a product")
async def create_producto(producto: CreateProductoModel, response: Response, request: Request):
    res = await ProductController().create_producto(producto)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res
  
@router.get("/getProductsByid", summary="Get product by id")
async def get_producto_by_id(response: Response, id_producto: str):
  res = await ProductController().get_producto_by_id(id_producto, producto=ConsultProductoModel)
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

@router.get("/getAllProductos", summary="Get user by id")
async def get_all_productos(response: Response):
    producto_controller = ProductController()  # Instancia correcta
    res = await producto_controller.get_all_productos()  # Llamada correcta

    response.status_code = 200 if res else 400
    return res
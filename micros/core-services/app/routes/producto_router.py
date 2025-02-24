from fastapi import APIRouter, Response, Request, Body
from ..controllers.producto_controller import ProductController
from ..models.producto_model import CreateProductoModel, UpdateProductoModel, ConsultProductoModel, DeleteProductoModel

router = APIRouter()

@router.post("/createProducto", summary="Create a product")
async def create_producto(producto: CreateProductoModel, response: Response, request: Request):
    res = await ProductController().create_producto(producto)
    if res:
        response.status_code = 200
    else:
        response.status_code = 404
    return res
  
@router.get("/getProductsByBarcode", summary="Get product by bar code")
async def get_producto_by_barcode(response: Response, codigo_barras: int):
  res = await ProductController().get_producto_by_barcode(codigo_barras, producto=ConsultProductoModel)
  if res:
    response.status_code = 200
  else:
    response.status_code = 400
  return res

@router.put("/updateProducto/{codigo_barras}", summary="Update product")
async def update_producto(codigo_barras: str, response: Response, producto: UpdateProductoModel = Body(...)):
  res = await ProductController().update_producto(codigo_barras, producto)
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
  
@router.delete("/deleteProducto/{id_producto}", summary="Delete Product")
async def delete_producto(id_producto: str):
  res = await ProductController().delete_producto(id_producto)
  if res:
    return {"message": "Producto eliminado con exito"}
  else:
    return {"message": "Producto no encontrado o fallo eliminación"}, 400
  
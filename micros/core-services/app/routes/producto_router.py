from fastapi import APIRouter, Response, Request, Body, File, UploadFile, FastAPI, Query
from ..controllers.producto_controller import ProductController
from ..models.producto_model import CreateProductoModel, UpdateProductoModel, ConsultProductoModel, DeleteProductoModel
# import openpyxl

router = APIRouter()
app = FastAPI()

@router.post("/createProducto", summary="Create a product")
async def create_producto(producto: CreateProductoModel, response: Response):
    res = await ProductController().create_producto(producto)
    print(producto)
    if "error" not in res:  # Verifica si no hubo un error
        response.status_code = 201  # Código 201 para "Creado"
    else:
        response.status_code = 400  # Código 400 para "Solicitud Incorrecta"
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

@router.get("/getAllProductos", summary="Get all products")
async def get_all_productos(
  response: Response,
    id_inventario: int = Query(..., description="ID of the inventory")  
):
    print(f"Recibido id_inventario: {id_inventario}")
    producto_controller = ProductController() 
    res = await producto_controller.get_all_productos(id_inventario)  

    response.status_code = 200 if res else 400
    return res
  
@router.delete("/deleteProducto/{id_producto}", summary="Delete Product")
async def delete_producto(id_producto: str):
  res = await ProductController().delete_producto(id_producto)
  if res:
    return {"message": "Producto eliminado con exito"}
  else:
    return {"message": "Producto no encontrado o fallo eliminación"}, 400
  
# @app.post("/api/upload")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         # Guardar el archivo temporalmente
#         with open("uploaded_file.xlsx", "wb") as f:
#             f.write(await file.read())  # Escribir el archivo en disco

#         # Abrir el archivo Excel
#         wb = openpyxl.load_workbook("uploaded_file.xlsx")
#         sheet = wb.active

#         # Leer las cabeceras de las columnas (primera fila)
#         headers = [cell.value for cell in sheet[1]]

#         # Leer los datos, usando las cabeceras dinámicas
#         productos = []
#         for row in sheet.iter_rows(min_row=2, values_only=True):  # Empezamos desde la segunda fila
#             producto = {}
#             for header, value in zip(headers, row):
#                 producto[header] = value  # Asignar cada columna a su correspondiente cabecera
#             productos.append(producto)

#         return {"productos": productos}
#     except Exception as e:
#         return {"error": str(e)}
  
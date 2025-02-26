from pydantic import BaseModel
from typing import Optional

class CreateProductoModel(BaseModel):
    id_usuario: int | None = None
    nombre_inventario: int | None = None
    nombre: str | None = None
    descripcion: str | None = None
    cantidad: int | None = None
    data: Optional[str]=None
    codigo_barras: str | None = None
    
    
class UpdateProductoModel(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    cantidad: Optional[int]
    conteo: Optional[int]
    data: Optional[str]=None
    
class ConsultProductoModel(BaseModel):
    codigo_barras: int | None = None
    nombre: str | None = None
    descripcion: str | None = None
    cantidad: int | None = None
    data: Optional[str]=None
    conteo: int | None = None
    
class ConsultAllProductoModel(BaseModel):
    id_producto: int | None = None
    nombre: str | None = None
    descripcion: str | None = None
    cantidad: int | None = None
    data: Optional[str]=None
    conteo: int | None = None
    
class DeleteProductoModel(BaseModel):
    id_producto: str
    
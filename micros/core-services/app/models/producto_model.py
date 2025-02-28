from pydantic import BaseModel
from typing import Optional

class CreateProductoModel(BaseModel):
    codigo_barras: str
    id_usuario: int
    id_perfil: int
    id_inventario: int
    nombre: str
    descripcion: Optional[str] = None
    cantidad: int
    
    
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
    
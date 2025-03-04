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
    id_producto: Optional[int] | None = None
    id_usuario: Optional[int] | None = None
    id_perfil: Optional[int] | None = None
    id_inventario: Optional[int] | None = None
    
class ConsultProductoModel(BaseModel):
    codigo_barras: int | None = None
    nombre: str | None = None
    descripcion: str | None = None
    cantidad: int | None = None
    data: Optional[str]=None
    conteo: Optional[int] | None = None
    id_producto: int | None = None
    id_usuario: int | None = None
    id_perfil: int | None = None
    id_inventario: int | None = None
    
    
class ConsultAllProductoModel(BaseModel):
    id_inventario: Optional[int] | None = None
    codigo_barras: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    cantidad: int | None = None
    data: Optional[str]=None
    conteo: Optional[int]| None = None
    id_producto: int | None = None
    id_usuario: int | None = None
    id_perfil: int | None = None
    id_inventario: int | None = None
    
class DeleteProductoModel(BaseModel):
    codigo_barras: int
    
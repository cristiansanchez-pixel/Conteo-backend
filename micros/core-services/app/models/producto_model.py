from pydantic import BaseModel
from typing import Optional

class CreateProductoModel(BaseModel):
    codigo_barras: str
    id_usuario: int
    id_perfil: int
    id_inventario: int
    nombre: str
    descripcion: Optional[str] = None
    stock: int
    precio_unidad: float
    
    
class UpdateProductoModel(BaseModel):
    codigo_barras: Optional[int]
    nombre: Optional[str]
    descripcion: Optional[str]
    stock: Optional[int]
    conteo: Optional[int]
    data: Optional[str]=None
    precio_unidad: Optional[float]
    id_producto: Optional[int] | None = None
    id_usuario: Optional[int] | None = None
    id_perfil: Optional[int] | None = None
    id_inventario: Optional[int] | None = None
    
class UpdateConteoModel(BaseModel):
    codigo_barras: Optional[int]
    conteo: Optional[int]
    id_producto: Optional[int] | None = None
    id_usuario: Optional[int] | None = None
    id_perfil: Optional[int] | None = None
    id_inventario: Optional[int] | None = None
    
class ConsultProductoModel(BaseModel):
    codigo_barras: int | None = None
    nombre: str | None = None
    descripcion: str | None = None
    stock: int | None = None
    data: Optional[str]=None
    conteo: Optional[int] | None = None
    precio_unidad: float | None = None
    id_producto: int | None = None
    id_usuario: int | None = None
    id_perfil: int | None = None
    id_inventario: int | None = None
    
    
class ConsultAllProductoModel(BaseModel):
    id_inventario: Optional[int] | None = None
    codigo_barras: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    stock: int | None = None
    data: Optional[str]=None
    conteo: Optional[int]| None = None
    precio_unidad: float | None = None
    id_producto: int | None = None
    id_usuario: int | None = None
    id_perfil: int | None = None
    id_inventario: int | None = None
    
class DeleteProductoModel(BaseModel):
    codigo_barras: int
    
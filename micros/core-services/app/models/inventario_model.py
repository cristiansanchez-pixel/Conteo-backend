from pydantic import BaseModel
from typing import Optional, List
from ..models.producto_model import CreateProductoModel

class CreateInventarioModel(BaseModel):
    id_inventario: int
    nombre_inventario: str
    id_usuario: int
    usuarios_id_perfil: str
    productos: Optional[List[CreateProductoModel]] = None
    
class UpdateInventarioModel(BaseModel):
    id_inventario: int
    nombre_inventario: str
    id_usuario: str
    usuarios_id_perfil: str
    productos: Optional[List[CreateProductoModel]] = None
    
class ConsultInventarioModel(BaseModel):
    id_inventario: int
    nombre_inventario: str
    id_usuario: int
    usuarios_id_perfil: str
    productos: Optional[List[CreateProductoModel]] = None
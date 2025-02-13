from pydantic import BaseModel
from typing import Optional, List
from ..models.producto_model import CreateProductoModel

class CreateInventarioModel(BaseModel):
    id_inventario: str
    nombre_inventario: str
    id_usuario: str
    usuarios_id_perfil: str
    
class UpdateInventarioModel(BaseModel):
    id_inventario: str
    nombre_inventario: str
    id_usuario: str
    usuarios_id_perfil: str
    productos: Optional[List[CreateProductoModel]] = []
    
class ConsultInventarioModel(BaseModel):
    id_inventario: str
    nombre_inventario: str
    id_usuario: str
    usuarios_id_perfil: str
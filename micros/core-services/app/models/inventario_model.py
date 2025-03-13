from pydantic import BaseModel
from typing import Optional, List
from ..models.producto_model import CreateProductoModel
from datetime import datetime 

class CreateInventarioModel(BaseModel):
    id_inventario: Optional[str]
    id_usuario:  Optional[str]
    nombre_inventario: str
    
    
class UpdateInventarioModel(BaseModel):
    nombre_inventario: str
    
class ConsultInventarioModel(BaseModel):
    id_inventario: int
    nombre_inventario: str
    id_usuario: int
    usuarios_id_perfil: str
    productos: Optional[List[CreateProductoModel]] = None
    
class ConsultAllInventarioModel(BaseModel):
    id_inventario: int
    nombre_inventario: str
    fecha_creacion: datetime
    
class ConsultInventariosDashboard(BaseModel):
    id_inventario: int
    nombre_inventario: str
    cantidad_productos: int
    cantidad_productos_con_conteo: int
    cantidad_productos_sin_conteo: int
    fecha_creacion: datetime
    
class ConsultNameInventory(BaseModel):
    
    nombre_inventario: str
    id_inventario: Optional[int]
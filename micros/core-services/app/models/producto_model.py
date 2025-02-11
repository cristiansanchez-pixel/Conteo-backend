from pydantic import BaseModel
from typing import Optional

class CreateProductoModel(BaseModel):
    id_producto: str
    descripcion: str
    cantidad: int
    data: Optional[str]=None
    conteo: int
    
class UpdateProductoModel(BaseModel):
    id_producto: str
    descripcion: str
    cantidad: int
    data: Optional[str]=None
    conteo: int
    
class ConsultProductoModel(BaseModel):
    id_producto: str
    descripcion: str
    cantidad: int
    data: Optional[str]=None
    conteo: int
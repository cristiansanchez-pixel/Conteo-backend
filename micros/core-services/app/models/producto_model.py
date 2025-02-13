from pydantic import BaseModel
from typing import Optional

class CreateProductoModel(BaseModel):
    id_producto: str
    descripcion: str
    cantidad: int
    data: Optional[str]=None
    conteo: int
    
class UpdateProductoModel(BaseModel):
    descripcion: str
    cantidad: int
    data: Optional[str]=None
    
class ConsultProductoModel(BaseModel):
    id_producto: str
    
class DeleteProductoModel(BaseModel):
    id_producto: str
    
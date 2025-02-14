from pydantic import BaseModel, Field
from typing import Optional 
from datetime import datetime

#Modelo de datos para manejar usuarios, en este caso se manejan los campos que se van a usar en la creación de usuarios

class UsuarioModel(BaseModel):
    id_usuario: int | None = None
    nombre: str | None = None
    email: str | None = None
    clave: str | None = None
    id_perfil: int | None = None
    fecha_creacion: int | None = None



class CreateUserModel(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    email: str
    clave: str
    id_perfil: Optional[int]


class UpdateUserModel(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del usuario")
    email: Optional[str] = Field(None, description="Correo del usuario")
    clave: Optional[str] = Field(None, description="Clave del usuario")
    id_perfil: Optional[str] = Field(None, description="Perfil del usuario")
    id_usuario: str



class ConsultUserModel(BaseModel):
    nombre: Optional[str]
    email: Optional[str]
    clave: Optional[str]
    id_perfil: str
    id_usuario: str
    nombre_perfil: str
    fecha_creacion: datetime
    
class DeleteUsuarioModel(BaseModel):
    id_usuario: int

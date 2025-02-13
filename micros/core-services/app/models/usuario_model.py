from pydantic import BaseModel
from typing import Optional 

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
    nombre: str
    email: str
    clave: str
    id_perfil: str



class ConsultUserModel(BaseModel):
    id_perfil: int
    nombre_perfil: str
    id_usuario: int
    fecha_creacion: int
    ip: str | None = None
    last_login: int | None = None
    
class DeleteUsuarioModel(BaseModel):
    id_usuario: int

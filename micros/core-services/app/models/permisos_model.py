from pydantic import BaseModel
from typing import List


class Permiso(BaseModel):
    id_permiso: int | None = None
    nombre_permiso: str
    descripcion_permiso: str


class Profile(BaseModel):
    id_perfil: int


class CreatePermisos(BaseModel):
    nombre_permiso: str
    descripcion_permiso: str



# class CreatePermisoPerfil(BaseModel):
#     nombre_permiso: str
#     descripcion_permiso: str | None = None
#     perfil: str
#     id_usuario: int

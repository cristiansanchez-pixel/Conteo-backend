from pydantic import BaseModel
from typing import List


class Permiso(BaseModel):
    id_permiso: str | None = None
    nombre_permiso: str
    descripcion_permiso: str


class Profile(BaseModel):
    id_perfil: str


class CreatePermisos(BaseModel):
    permiso: Permiso
    perfil: List[Profile]
    id_usuario: str


class CreatePermisoPerfil(BaseModel):
    nombre_permiso: str
    descripcion_permiso: str | None = None
    perfil: str
    id_usuario: str

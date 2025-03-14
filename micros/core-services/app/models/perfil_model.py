from pydantic import BaseModel
from typing import List


class Perfil(BaseModel):
    id_perfil: int | None = None
    nombre_perfil: str
    descripcion_perfil: str


class PermisosPerfiles(BaseModel):
    id_permiso: int
    id_perfil: int


class CreatePerfil(BaseModel):
    nombre_perfil: str
    descripcion_perfil: str

class UpdatePerfilModel(BaseModel):
    profile: Perfil
    permisos_perfiles: List[PermisosPerfiles]
    
class ConsultPerfilModel(BaseModel):
    profile: Perfil
    permisos_perfiles: List[PermisosPerfiles]
    id_usuario: int
    id_perfil: int
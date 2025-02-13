from pydantic import BaseModel
from typing import List


class Perfil(BaseModel):
    id_perfil: str | None = None
    nombre_perfil: str
    descripcion_perfil: str


class PermisosPerfiles(BaseModel):
    id_permiso: str
    nombre_permiso: str
    descripcion_perfil: str


class CreatePerfil(BaseModel):
    profile: Perfil
    permisos_perfiles: List[PermisosPerfiles]
    id_usuario: str

class UpdatePerfilModel(BaseModel):
    profile: Perfil
    permisos_perfiles: List[PermisosPerfiles]
    
class ConsultPerfilModel(BaseModel):
    profile: Perfil
    permisos_perfiles: List[PermisosPerfiles]
    id_usuario: str
    id_perfil: str
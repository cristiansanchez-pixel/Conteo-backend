from pydantic import BaseModel

#Modelo de datos para manejar usuarios, en este caso se manejan los campos que se van a usar en la creación de usuarios
class CreateUserModel(BaseModel):
    nombre: str
    email: str
    #user_document: str
    #user_cellphone: str
    id_perfil: str
    id_usuario: str
    # regi_id: int
    # city_id: int


class UpdateUserModel(BaseModel):
    nombre: str
    email: str
    #user_document: str
    #user_cellphone: str
    id_perfil: str
    id_usuario: str
    # regi_id: int
    # city_id: int


class ConsultUserModel(BaseModel):
    id_usuario: str
    nombre: str
    email: str
    #user_document: str
    #user_cellphone: str
    id_perfil: str
    nombre_perfil: str
    id_usuario: str
    # coun_id: int | None = None
    # regi_id: int | None = None
    # city_id: int | None = None
    fecha_creacion: int
    ip: str | None = None
    last_login: int | None = None

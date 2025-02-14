from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.usuario_model import CreateUserModel, UpdateUserModel, ConsultUserModel, DeleteUsuarioModel
from ..utils.usuario import hash_password, generar_valor_alfanumerico
from fastapi import HTTPException


class UserController:
    async def create_user(self, ip: str, usuarios: CreateUserModel):
        with Database() as db:
            try:
                clave = generar_valor_alfanumerico(10)
                hashed_clave = hash_password(clave)
                id_perfil = usuarios.id_perfil if usuarios.id_perfil is not None else 2
                query_user = """
                    INSERT INTO usuarios
                    ( nombre, email, clave, id_perfil)
                    VALUES( %s, %s, %s, %s);   
                """
                db.execute(
                    query_user,
                    (
                        usuarios.nombre,
                        usuarios.email,
                        hashed_clave,
                        id_perfil
                    ),
                )

                return {
                    "message": "Usuario creado exitosamente",
                    "email": usuarios.email,
                    "id_perfil": id_perfil
                }
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}


    async def get_user_by_id(self, id_usuario: str):
        with Database() as db:
            try:
                query = """
                    SELECT 
                        u.id_usuario, 
                        u.nombre, 
                        u.email, 
                        u.id_perfil,
                        p.nombre_perfil,
                        u.fecha_creacion
                    FROM usuarios AS u
                    INNER JOIN perfiles AS p ON u.id_perfil = p.id_perfil
                    WHERE u.id_usuario = %s
                """
                db.execute(query, (id_usuario,))
                usuario = db.fetchone()
                if not usuario:
                    return None
                return ConsultUserModel(
                    id_usuario=usuario[0],
                    nombre=usuario[1],
                    email=usuario[2],
                    id_perfil=usuario[3],
                    nombre_perfil=usuario[4],
                    fecha_creacion=usuario[5],
                )
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def delete_user(self, id_usuario: str):
        with Database() as db:
            try:
                 db.execute("DELETE FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
                 db.commit()
            
                 return {"message": f"Usuario con id {id_usuario} eliminado correctamente"}
        
            except Exception as e:
               db.rollback()
               return {"error": str(e)}

    async def update_user(self, id_usuario: str, usuarios: UpdateUserModel):
        with Database() as db:
            try:
                # Obtener los datos actuales del usuario
                old_user = await self.get_user_by_id(id_usuario)
                if not old_user:
                    raise HTTPException(status_code=404, detail="Usuario no encontrado")

                # Si `usuarios` es un dict en lugar de un objeto Pydantic, conviértelo
                if isinstance(usuarios, dict):
                    usuarios = UpdateUserModel(**usuarios)

                # Función para mantener los valores previos si son None o están vacíos
                def keep_old_value(new_value, old_value):
                    return old_value if new_value is None or new_value.strip() == "" else new_value

                # Aplicar la función a cada campo
                nombre = keep_old_value(usuarios.nombre, old_user.nombre)
                email = keep_old_value(usuarios.email, old_user.email)
                clave = keep_old_value(usuarios.clave, old_user.clave)
                id_perfil = keep_old_value(usuarios.id_perfil, old_user.id_perfil)

                query = """
                    UPDATE usuarios
                    SET nombre=%s, email=%s, clave=%s, id_perfil=%s
                    WHERE id_usuario=%s;
                """
                db.execute(query, (nombre, email, clave, id_perfil, id_usuario))

                db.commit()  # Guardar cambios en la base de datos

                return {
                    "message": "Usuario actualizado correctamente",
                    "data": {
                        "new_user": {
                            "nombre": nombre,
                            "email": email,
                            "clave": clave,
                            "id_perfil": id_perfil,
                        },
                    },
                }
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
            
    async def get_all_users(self):
        with Database() as db:
            try:
                query = """
                    SELECT 
                        u.id_usuario, 
                        u.nombre, 
                        u.email, 
                        u.id_perfil,
                        p.nombre_perfil,
                        u.fecha_creacion
                    FROM usuarios AS u
                    INNER JOIN perfiles AS p ON u.id_perfil = p.id_perfil
                """
                db.execute(query)
                usuarios = db.fetchall()

                return [
                    {
                        "id_usuario": user[0],
                        "nombre": user[1],
                        "email": user[2],
                        "id_perfil": user[3],
                        "nombre_perfil": user[4],
                        "fecha_creacion": user[5],
                    }
                    for user in usuarios
                ]
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.usuario_model import CreateUserModel, UpdateUserModel, ConsultUserModel
from ..utils.usuario import hash_password, generar_valor_alfanumerico


class UserController:
    async def create_user(self, ip: str, usuarios: CreateUserModel):
        with Database() as db:
            try:
                if usuarios.user_is_commercial is None:
                    usuarios.user_is_commercial = False
                clave = generar_valor_alfanumerico(10)
                hashed_clave = hash_password(clave)
                new_id_usuario = str(uuid())
                query_user = """
                    INSERT INTO usuarios
                    ( id_usuario, nombre, email, clave, id_perfil)
                    VALUES( %s, %s, %s, %s, %s);   
                """
                db.execute(
                    query_user,
                    (
                        new_id_usuario,
                        usuarios.nombre,
                        usuarios.email,
                        hashed_clave,
                        usuarios.id_perfil
                    ),
                )
                toSave = {
                    "id_usuario": new_id_usuario,
                    "nombre": usuarios.nombre,
                    "email": usuarios.email,
                    "id_perfil": usuarios.id_perfil
                }

                return True
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
                    FROM `usuarios` AS u
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
                query = """
                    UPDATE usuarios
                    SET nombre = CONCAT(nombre, '_deleted'), email = CONCAT(email, '_deleted')
                    WHERE id_usuario = %s;
                """
                db.execute(query, (id_usuario,))
                return {"message": "Usuario desactivado correctamente"}
            except Exception as e:
                await db.rollback()
                return {"error": str(e)}

    async def update_user(self, id_usuario: str, usuarios: UpdateUserModel):
        with Database() as db:
            try:
                old_user = await self.get_user_by_id(id_usuario)
                query = """
                    UPDATE `usuarios`
                    SET nombre=%s, id_perfil=%s
                    WHERE id_usuario=%s;
                """
                db.execute(
                    query,
                    (
                        usuarios.nombre,
                        usuarios.id_perfil,
                        usuarios.id_usuario,
                    ),
                )

                if old_user.email != usuarios.email:

                    query_email = """
                        UPDATE `usuarios`
                        SET email=%s
                        WHERE id_usuario=%s;
                    """
                    db.execute(query_email, (usuarios.email, usuarios.user_id))

                toSave = {
                    "old_user": {
                        "nombre": old_user.user_name,
                        "email": old_user.user_email,
                        "id_perfil": old_user.prof_id,
                    },
                    "new_user": {
                        "nombre": usuarios.nombre,
                        "email": usuarios.email,
                        "id_perfil": usuarios.id_perfil,
                        
                    },
                }

                return True
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

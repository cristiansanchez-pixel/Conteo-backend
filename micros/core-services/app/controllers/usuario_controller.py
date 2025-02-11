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
                    INSERT INTO `usuarios`
                    ( id_usuario, nombre, email, clave, id_perfil)
                    VALUES( %s, %s, %s, %s, %s, "active",  NULL, %s, %s, %s, %s);   
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

    async def get_all_users_by_enterprise(
        self, id_perfil: str, current_page, page_size, filter, order_by, order
    ):
        with Database() as db:
            total = 0
            list_users = []
            params_total = []
            params = []
            try:
                params_total.append(id_perfil)

                query_total = "SELECT COUNT(id_usuario) FROM `usuarios` WHERE (id_perfil = %s )"
                if filter != None and filter != "":
                    query_total += """ AND (nombre LIKE %s OR email LIKE %s) """
                    params_total.append(f"%{filter}%")
                    params_total.append(f"%{filter}%")
                db.execute(query_total, params_total)
                total = db.fetchone()[0]

                query = """
                    SELECT 
                        u.id_usuario, 
                        u.nombre, 
                        u.email, 
                        u.id_perfil, 
                        p.nombre_perfil,
                        u.fecha_creacion,
                        COALESCE(latest_login.auus_ip, 'N/A') AS last_login_ip,
                        COALESCE(latest_login.auus_date, 'N/A') AS last_login_date
                    FROM `usuarios` AS u
                    LEFT JOIN perfiles AS p ON u.id_perfil = p.id_perfil
                """

                params.append(id_perfil)
                if filter != None and filter != "":
                    query += """ AND (nombre LIKE %s OR email LIKE %s) """
                    params.append(f"%{filter}%")
                    params.append(f"%{filter}%")

                query += " ORDER BY u.id_usuario DESC"

                if order_by != None and order_by != "":
                    query += " , " + order_by
                    if order != None and order != "":
                        query += " " + order
                if current_page != None and page_size != None:
                    query += " LIMIT %s OFFSET %s"
                    params.append(page_size)
                    params.append((current_page - 1) * page_size)

                db.execute(query, params)
                usuarios = db.fetchall()

                for usuario in usuarios:
                    list_users.append(
                        ConsultUserModel(
                            id_usuario=usuario[0],
                            nombre=usuario[1],
                            email=usuario[2],
                            id_perfil=usuario[3],
                            nombre_perfil=usuario[4],
                            fecha_creacion=usuario[5]
                        )
                    )
                return {"total": total, "users": list_users}
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
                        u.fecha_creacion,
                    FROM `usuarios` AS u
                    INNER JOIN perfiles AS p ON u.id_perfil = p.id_perfil
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
                await db.execute(query, (id_usuario,))
                return {"message": "Usuario desactivado correctamente"}
            except Exception as e:
                await db.rollback()
                return {"error": str(e)}

    async def update_user(self, id_usuario: str, usuarios: UpdateUserModel):
        with Database() as db:
            try:
                old_user = await self.get_user_by_id(usuarios.id_usuario)
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

    # async def get_user_commercial(self, ente_id: str):
    #     with Database() as db:
    #         try:
    #             query = """
    #                 SELECT 
    #                     u.user_id, 
    #                     u.user_name, 
    #                     u.user_email, 
    #                     u.user_document, 
    #                     u.doty_id, 
    #                     u.user_is_commercial,
    #                     dt.doty_name
    #                 FROM `user` AS u
    #                 INNER JOIN document_type AS dt ON u.doty_id = dt.doty_id
    #                 WHERE (ente_id = %s AND user_is_commercial = 1 AND user_status = "active" AND u.deleted_at IS NULL)
    #             """
    #             db.execute(query, (ente_id,))
    #             users = db.fetchall()
    #             list_users = []
    #             for user in users:
    #                 list_users.append(
    #                     {
    #                         "user_id": user[0],
    #                         "user_name": user[1],
    #                         "user_email": user[2],
    #                         "user_document": user[3],
    #                         "doty_id": user[4],
    #                         "doty_name": user[6],
    #                         "user_is_commercial": user[5],
    #                     }
    #                 )
    #             return list_users
    #         except Exception as e:
    #             print(e)
    #             db.rollback()
    #             return {"error": str(e)}

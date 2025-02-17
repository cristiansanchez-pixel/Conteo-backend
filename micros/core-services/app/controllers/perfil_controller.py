from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.perfil_model import CreatePerfil, Perfil
from ..utils.perfil import ProfileUtils
from ..utils.audit import save_audit_user

class PerfilController:
    async def create_perfil(self, ip: str, perfil: CreatePerfil):
        with Database() as db:
            try:
                query_profile = """
                    INSERT INTO conteo.perfiles
                    (nombre_perfil, descripcion_perfil)
                    VALUES(%s, %s);
                """
                db.execute(
                    query_profile,
                    (
                        perfil.nombre_perfil,
                        perfil.descripcion_perfil,
                    ),
                )
                to_save = [
                    ("profile id", "id_perfil", False),
                    ("profile name", "nombre_perfil", True),
                ]
                save_audit_user(
                    db,
                    ip,
                    to_save,
                    perfil.id_user,
                    "CREATE PROFILE",
                )
                return True
            except Exception as e:
                print(e)
                db.rollback()
                return False
    
    async def get_all_perfiles(self):
        with Database() as db:
            try:
                query = "SELECT id_perfil, nombre_perfil, descripcion_perfil FROM perfiles"
                db.execute(query)
                perfiles = db.fetchall()
                
                return [
                    Perfil(id_perfil=perfil[0], nombre_perfil=perfil[1], descripcion_perfil=perfil[2])  # <- Se agregó `descripcion_perfil`
                    for perfil in perfiles
                ]
            except Exception as e:
                print(e)
                return False
            
    async def delete_perfil(self, ip: str, id_perfil: str, id_user: int):
        with Database() as db:
            try:
                query = "DELETE FROM perfiles WHERE id_perfil = %s"
                db.execute(query, (id_perfil,))
                to_save = [("profile id", "id_perfil", id_perfil, False)]
                save_audit_user(
                    db,
                    ip,
                    to_save,
                    id_user,
                    "DELETE PROFILE",
                )
                return True
            except Exception as e:
                print(e)
                db.rollback()
                return False

    # async def get_perfil_by_id(self, id_perfil: str):
    #     with Database() as db:
    #         try:
    #             query = "SELECT id_perfil, nombre_perfil, descripcion_perfil FROM `perfiles` WHERE id_perfil = %s"
    #             db.execute(query, (id_perfil,))
    #             perfil = db.fetchone()
    #             if not perfil:
    #                 return None
    #             return ConsultPerfilModel(id_perfil=perfil[0], nombre_perfil=perfil[1], descripcion_perfil=perfil[2])
    #         except Exception as e:
    #             print(e)
    #             db.rollback()
    #             return {"error": str(e)}

    # async def update_perfil(self, id_perfil: str, perfil: UpdatePerfilModel):
    #     with Database() as db:
    #         try:
    #             query = "UPDATE `perfiles` SET nombre_perfil=%s, descripcion_perfil=%s WHERE id_perfil=%s;"
    #             db.execute(
    #                 query,
    #                 (
    #                     ProfileUtils(perfil.nombre_perfil),
    #                     perfil.descripcion_perfil,
    #                     id_perfil,
    #                 ),
    #             )
    #             return {"message": "Perfil actualizado correctamente"}
    #         except Exception as e:
    #             print(e)
    #             db.rollback()
    #             return {"error": str(e)}

    # async def delete_perfil(self, id_perfil: str):
    #     with Database() as db:
    #         try:
    #             query = "DELETE FROM `perfiles` WHERE id_perfil = %s;"
    #             db.execute(query, (id_perfil,))
    #             return {"message": "Perfil eliminado correctamente"}
    #         except Exception as e:
    #             print(e)
    #             db.rollback()
    #             return {"error": str(e)}

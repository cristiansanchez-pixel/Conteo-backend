from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.perfil_model import CreateProfile, Perfil
from ..utils.perfil import format_profile_name

class PerfilController:
    async def create_perfil(self, perfil: CreateProfile):
        with Database() as db:
            try:
                id_perfil = str(uuid())
                nombre_formateado = format_profile_name(perfil.nombre_perfil)
                query_profile = """
                    INSERT INTO conteo.perfiles
                    (id_perfil, nombre_perfil, descripcion_perfil)
                    VALUES(%s, %s, %s);
                """
                db.execute(
                    query_profile,
                    (
                        id_perfil,
                        nombre_formateado,
                        perfil.descripcion_perfil,
                    ),
                )
                db.commit()
                return {"id_perfil": id_perfil, "nombre_perfil": nombre_formateado}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
    
    async def get_all_perfiles(self):
        with Database() as db:
            try:
                query = "SELECT id_perfil, nombre_perfil, descripcion_perfil FROM `perfiles`"
                db.execute(query)
                perfiles = db.fetchall()
                
                if not perfiles:
                    return []                
                
                return [
                    Perfil(
                        id_perfil=perfil[0], nombre_perfil=perfil[1], descripcion_perfil=perfil[2]
                    ) for perfil in perfiles
                ]
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

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

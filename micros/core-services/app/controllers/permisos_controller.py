from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.permisos_model import CreatePermisos, Permiso
import logging
# from ..utils.audit import save_audit_user
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
class PermisosController:
   async def create_permiso(self, ip: str, permiso: CreatePermisos):
    with Database() as db:
      try:
        query_permiso = """
          INSERT INTO permisos
          (nombre_permiso, descripcion_permiso)
          VALUES(%s, %s);
        """
        db.execute(
           query_permiso,
          (
            permiso.nombre_permiso,
            permiso.descripcion_permiso
          ),
        )
        db.commit()
        
        return {"message": "Permiso creado con éxito",
                "nombre_permiso": permiso.nombre_permiso,
                "descripcion_permiso": permiso.descripcion_permiso}
      except Exception as e:
        print(e)
        db.rollback()
        return {"error": str(e)}
      
   async def get_all_permisos(self):
    with Database() as db:
        try:
            query = "SELECT id_permiso, nombre_permiso, descripcion_permiso FROM `permisos`"
            db.execute(query)
            rows = db.fetchall()
            
            result = [
                Permiso(id_permiso=row[0], nombre_permiso=row[1], descripcion_permiso=row[2])
                for row in rows
            ]
            return result
        except Exception as e:
           print(e)
           return False
          
          
#    async def create_permiso_perfil(self, data: CreatePermisoPerfil):
#         with Database() as db:
#             try:
#                 # Buscar o crear permiso
#                 db.execute("SELECT id_permiso FROM permisos WHERE nombre_permiso = %s;", (data.permiso,))
#                 row = db.fetchone()
#                 permiso_id = row[0] if row else str(uuid())

#                 if not row:
#                     db.execute(
#                         "INSERT INTO permisos (id_permiso, nombre_permiso, descripcion_permiso) VALUES (%s, %s, %s);",
#                         (permiso_id, data.permiso, data.descripcion_permiso),
#                     )

#                 # Buscar o crear perfil
#                 db.execute("SELECT id_perfil FROM perfiles WHERE nombre_perfil = %s;", (data.perfil,))
#                 row = db.fetchone()
#                 perfil_id = row[0] if row else str(uuid())

#                 if not row:
#                     db.execute(
#                         "INSERT INTO perfiles (id_perfil, nombre_perfil, descripcion_perfil) VALUES (%s, %s, %s);",
#                         (perfil_id, data.perfil, data.descripcion_perfil),
#                     )

#                 # Verificar si la relación ya existe
#                 db.execute("SELECT id_permiso FROM permisos_perfiles WHERE id_permiso = %s AND id_perfil = %s;", 
#                            (permiso_id, perfil_id))
#                 if not db.fetchone():
#                     db.execute("INSERT INTO permisos_perfiles (id_permiso, id_perfil) VALUES (%s, %s);",
#                                (permiso_id, perfil_id))

#                 db.commit()
#                 return True
#             except Exception as e:
#                 print(e)
#                 db.rollback()
#                 return False
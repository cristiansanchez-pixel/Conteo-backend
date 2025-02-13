from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.permisos_model import CreatePermisos, Permiso, CreatePermisoPerfil
from ..utils.audit import save_audit_user

class PermisosController:
   async def create_permiso(self, ip: str, permiso: CreatePermisos):
    with Database() as db:
      try:
        id_permiso = str(uuid())
        query_permiso = """
          INSERT INTO `permisos`
          (id_permiso, nombre_permiso, descripcion_permiso)
          VALUES(%s, %s, %s);
        """
        db.execute(
           query_permiso,
          (
            id_permiso,
            permiso.permiso.nombre_permiso,
            permiso.permiso.descripcion_permiso,
          ),
        )
        
        to_save = [
            ("Permission", "nombre_permiso", permiso.permiso.nombre_permiso, True),
            (
                "Permission Description",
                "descripcion_permiso",
                permiso.permiso.descripcion_permiso,
                True,
                    ),
            ("Permission id", "id_permiso", id_permiso, False),
                ]
        save_audit_user(
            db,
            ip,
            to_save,
            permiso.id_usuario,
            "Create Permission",
            None,
                )
        return True
      except Exception as e:
        print(e)
        db.rollback()
        return {"error": str(e)}
      
   async def get_all_permisos(self):
    with Database() as db:
        query = "SELECT id_permiso, nombre_permiso, descripcion_permiso FROM `permisos`"
        db.execute(query)
        rows = db.fetchall()
        result = []
        for row in rows:
            result.append(
                  Permiso(
                    id_permiso=row[0],
                    nombre_permiso=row[1],
                    descripcion_permiso=row[2],
                    )
                )
            return result
          
          
   async def create_permiso_perfil(self, data):
    """
    Crea un permiso y un perfil si no existen y los relaciona en la tabla permisos_perfiles.
    """
    with Database() as db:
        try:
            # Buscar o crear permiso
            db.execute("SELECT id_permiso FROM permisos WHERE nombre_permiso = %s;", (data.permiso,))
            row = db.fetchone()
            if row:
                permiso_id = row[0]
            else:
                permiso_id = str(uuid.uuid4())
                db.execute(
                    """
                    INSERT INTO permisos (id_permiso, nombre_permiso, descripcion_permiso)
                    VALUES (%s, %s, %s);
                    """,
                    (permiso_id, data.permiso, data.descripcion_permiso),
                )

            # Buscar o crear perfil
            db.execute("SELECT id_perfil FROM perfiles WHERE nombre_perfil = %s;", (data.perfil,))
            row = db.fetchone()
            if row:
                perfil_id = row[0]
            else:
                perfil_id = str(uuid.uuid4())
                db.execute(
                    """
                    INSERT INTO perfiles (id_perfil, nombre_perfil, descripcion_perfil)
                    VALUES (%s, %s, %s);
                    """,
                    (perfil_id, data.perfil, data.descripcion_perfil),
                )

            # Verificar si la relación ya existe
            db.execute(
                "SELECT id_permiso FROM permisos_perfiles WHERE id_permiso = %s AND id_perfil = %s;", 
                (permiso_id, perfil_id)
            )
            if not db.fetchone():
                db.execute(
                    """
                    INSERT INTO permisos_perfiles (id_permiso, id_perfil)
                    VALUES (%s, %s);
                    """,
                    (permiso_id, perfil_id),
                )

            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
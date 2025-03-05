from typing import List
from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.inventario_model import CreateInventarioModel, ConsultInventariosDashboard


class InventarioController:
    
    async def create_inventario(self, inventario: CreateInventarioModel):
      with Database() as db:
        try:
            # Obtener id_perfil del usuario
            query_perfil = "SELECT id_perfil FROM usuarios WHERE id_usuario = %s"
            db.execute(query_perfil, (inventario.id_usuario,))
            perfil_result = db.fetchone()
            
            if not perfil_result:
                return {"error": "Usuario no encontrado"}

            id_perfil = perfil_result[0]  # Extraemos el id_perfil
            
            # Insertar en inventarios
            query_inventario = """
                INSERT INTO inventarios (nombre_inventario, id_usuario, usuarios_id_perfil)
                VALUES (%s, %s, %s);
            """
            db.execute(
                query_inventario,
                (inventario.nombre_inventario, inventario.id_usuario, id_perfil),
            )
            
            query_last_id = "SELECT LAST_INSERT_ID();"
            db.execute(query_last_id)
            id_inventario = db.fetchone()[0]
            
            db.commit()
            return {
                "id_inventario": id_inventario,
                "nombre_inventario": inventario.nombre_inventario,
                "id_usuario": inventario.id_usuario,
                "id_perfil": id_perfil
            }
            

        except Exception as e:
            print(e)
            db.rollback()
            return {"error": str(e)}
      
    async def get_all_inventarios(self, filter = None, order_by = None, order = None, current_page=None, page_size=None):
      with Database() as db:
          total = 0
          list_inventarios = []
          params_total = []
          params = []
          try:
          
          
          
              print("Ordenando por:", order_by, "en orden:", order)
              print("Filtro:", filter)
          

              query_total = "SELECT COUNT(id_inventario) FROM inventarios"
              if filter:
                  query_total += "WHERE nombre_inventario LIKE %s"
                  params_total.append(f"%{filter}%")
                
              db.execute(query_total, params_total)
              total = db.fetchone()[0]

              query = """  
                  SELECT 
                      i.id_inventario,
                      i.nombre_inventario,
                      COUNT(p.id_producto) AS cantidad_productos,
                      SUM(CASE WHEN p.conteo IS NOT NULL AND p.conteo > 0 THEN 1 ELSE 0 END) AS cantidad_productos_con_conteo,
                      i.fecha_creacion,
                      i.fecha_lectura,
                      i.id_usuario,
                      u.id_perfil
                  FROM inventarios AS i
                  LEFT JOIN productos AS p 
                    ON i.id_inventario = p.id_inventario
                  LEFT JOIN usuarios AS u
                    ON i.id_usuario = u.id_usuario
              """
              if filter:
                  query += """ WHERE i.nombre_inventario LIKE %s """
                  params.append(f"%{filter}%")

              query += " GROUP BY i.id_inventario"
            
              if order_by in ["nombre_inventario", "cantidad_productos", "cantidad_productos_con_conteo", "fecha_creacion", "fecha_lectura"] and order in ["ASC", "DESC"]:
                  query += f" ORDER BY {order_by} {order}"
              else:
                  query += " ORDER BY i.nombre_inventario ASC"
              if current_page != None and page_size != None:
                    query += " LIMIT %s OFFSET %s"
                    params.append(page_size)
                    params.append((current_page - 1) * page_size)


              db.execute(query, params)
              inventarios = db.fetchall()

              for inventario in inventarios:
                  list_inventarios.append(
                      {
                          "id_inventario": inventario[0],
                          "nombre_inventario": inventario[1],
                          "cantidad_productos": inventario[2],
                          "cantidad_productos_con_conteo": inventario[3],
                          "fecha_creacion": inventario[4],
                          "fecha_lectura": inventario[5],
                          "id_usuario": inventario[6],
                          "id_perfil": inventario[7]
                      }
                  )
              return {"total": total, "inventories": list_inventarios}
          except Exception as e:
              print(e)
              return {"error": str(e)}

      
  # async def get_all_inventarios(self, id_inventario: str, current_page, page_size, filter, order_by, order):
  #       with Database() as db:
  #           total = 0
  #           list_inventarios = []
  #           params_total = []
  #           params = []
  #           try:
  #               params_total.append(id_inventario)
  #               query_total = "SELECT COUNT(id_inventario) FROM `inventarios` WHERE (fecha_creacion = %s IS NULL)"
  #               if filter != None and filter != "":
  #                   query_total += """ AND (nombre_inventario LIKE %s) """
  #                   params_total.append(f"%{filter}%")
  #               db.execute(query_total, params_total)
  #               total = db.fetchone()[0]
            
  #               query = """
  #                   SELECT 
  #                       i.nombre_inventario, 
  #                       COALESCE(latest_login.auus_ip, 'N/A') AS last_login_ip,
  #                       COALESCE(latest_login.auus_date, 'N/A') AS last_login_date
  #                   FROM `inventarios` AS i
  #                   LEFT JOIN perfiles AS p ON u.id_perfil = p.id_perfil
  #                   LEFT JOIN (
  #                       SELECT 
  #                           auus_usuario,
  #                           auus_ip,
  #                           auus_date
  #                       FROM `audit_usuarios` AS au
  #                       WHERE au.auus_description = 'Login'
  #                       AND au.auus_date = (
  #                           SELECT MAX(au2.auus_date)
  #                       FROM `audit_usuarios` AS au2
  #                           WHERE au2.auus_usuario = au.auus_usuario
  #                           AND au2.auus_description = 'Login'
  #                       )
  #                   ) AS latest_login ON u.id_usuario = latest_login.auus_usuario
  #                   WHERE (i.id_inventario = %s)
  #                   """
  #               params.append(id_inventario)
  #               if filter != None and filter != "":
  #                   query += """ AND (nombre_inventario LIKE %s) """
  #                   params.append(f"%{filter}%")
        
  #               query += " ORDER BY u.id_usuario DESC"
                
  #               if order_by != None and order_by != "":
  #                   query += " , " + order_by
  #                   if order != None and order != "":
  #                       query += " " + order
  #               if current_page != None and page_size != None:
  #                   query += " LIMIT %s OFFSET %s"
  #                   params.append(page_size)
  #                   params.append((current_page - 1) * page_size)
                    
  #               db.execute(query, params)
  #               inventarios = db.fetchall()
                
  #               for inventario in inventarios:
  #                 list_inventarios.append(
  #                   ConsultInventarioModel(
  #                     nombre_inventario = inventario[0],
  #                     fehca_creacion = inventario[1],
  #                     id_producto = inventario[2]
  #                   )
  #                 ) 
  #               return {"total": total, "inventories": list_inventarios}
  #           except Exception as e:
  #               print(e)
  #               return {"error": str(e)}

      
    async def get_inventario_by_id(self, id_inventario: str):
      with Database() as db:
        try:
          query = "SELECT id_inventario, id_usuario, usuarios_id_perfil, nombre_inventario FROM `inventarios` WHERE id_inventario = %s"
          db.execute(query, (id_inventario,))
          inventario = db.fetchone()
          if not inventario:
            return None
          return CreateInventarioModel(
            id_inventario=inventario[0], id_usuario=inventario[1], usuarios_id_perfil=inventario[2], nombre_inventario=inventario[3]
          )
        except Exception as e:
          print(e)
          return {"error": str(e)}
      
    async def update_inventario(self, id_inventario: int, id_usuario: int, nombre_inventario: str):
      with Database() as db:
        try:
          query_inventario = """
            UPDATE inventarios
            SET id_usuario = %s, nombre_inventario = %s
            WHERE id_inventario = %s;
          """
          db.execute(
            query_inventario,
            (
                id_usuario,
                nombre_inventario,
                id_inventario
            ),
          )
        
          db.commit()
          return {"message": "Inventarioactualizado correctamente", "id_inventario": id_inventario}
        except Exception as e:
          print(e)
          db.rollback()
          return {"error": str(e)}
      
    async def delete_inventario(self, id_inventario: str):
      with Database() as db:
        try:
              db.execute("SELECT COUNT(*) FROM inventarios WHERE id_inventario = %s", (id_inventario,))
              if db.fetchone()[0] == 0:
                  return {"error": "Inventario no encontrado"}
            
              db.execute("DELETE FROM inventarios WHERE id_inventario = %s", (id_inventario,))
              db.commit()
              return {"message": "Inventario eliminado correctamente"}
        except Exception as e:
          print(e)
          db.rollback()
          return {"error": str(e)}
        
    
    async def get_inventarios_dashboard(self) -> List[ConsultInventariosDashboard]:
      with Database() as db:
        try:
            
            query = """
                SELECT
                    i.id_inventario,
                    i.nombre_inventario,
                    COUNT(p.id_producto) AS cantidad_productos,
                    SUM(CASE WHEN p.conteo IS NOT NULL AND p.conteo > 0 THEN 1 ELSE 0 END) AS cantidad_productos_con_conteo,
                    SUM(CASE WHEN p.conteo IS NULL OR p.conteo < 1 THEN 1 ELSE 0 END) AS cantidad_productos_sin_conteo,
                    i.fecha_creacion
                FROM inventarios i
                LEFT JOIN productos p ON i.id_inventario = p.id_inventario
                GROUP BY i.id_inventario
            """
            db.execute(query)
            inventarios = db.fetchall()
            print("imprimir", inventarios)
            respuesta = []
            
            for inventario in inventarios:
                inventario_temporal = ConsultInventariosDashboard(
                  id_inventario = inventario[0],
                  nombre_inventario = inventario[1],
                  cantidad_productos = inventario[2],
                  cantidad_productos_con_conteo = inventario[3],
                  cantidad_productos_sin_conteo = inventario[4],
                  fecha_creacion = inventario[5]
                  )
                respuesta.append(inventario_temporal)
            
            return respuesta

        except Exception as e:
            print(e)
            return {"error": str(e)}


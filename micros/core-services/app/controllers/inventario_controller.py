from typing import List
from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.inventario_model import CreateInventarioModel, ConsultInventariosDashboard, ConsultNameInventory


class InventarioController:
    
    async def create_inventario(self, inventario: CreateInventarioModel):
      with Database() as db:
        try:
          
            print(f"Datos recibidos para crear inventario: {inventario}")
          
            id_usuario = 5
            id_perfil = 2
            # Obtener id_perfil del usuario
            # query_perfil = "SELECT id_perfil FROM usuarios WHERE id_usuario = %s"
            # db.execute(query_perfil, (inventario.id_usuario,))
            # perfil_result = db.fetchone()
            
            # if not perfil_result:
            #     return {"error": "Usuario no encontrado"}

            # id_perfil = perfil_result[0]  # Extraemos el id_perfil
            
            # Insertar en inventarios
            query_inventario = """
                INSERT INTO inventarios (nombre_inventario, id_usuario, usuarios_id_perfil)
                VALUES (%s, %s, %s);
            """
            db.execute(
                query_inventario,
                (inventario.nombre_inventario, id_usuario, id_perfil),
            )
            
            query_last_id = "SELECT LAST_INSERT_ID();"
            db.execute(query_last_id)
            id_inventario = db.fetchone()[0]
            
            db.commit()
            return {
                "id_inventario": id_inventario,
                "nombre_inventario": inventario.nombre_inventario,
                "id_usuario": id_usuario,
                "id_perfil": id_perfil
            }
            

        except Exception as e:
            print(e)
            db.rollback()
            return {"error": str(e)}
          
          
          
    async def get_all_inventarios(self, filter=None, order_by=None, order=None, current_page=None, page_size=None):
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
                query_total += " WHERE nombre_inventario LIKE %s"
                params_total.append(f"%{filter}%")

            db.execute(query_total, params_total)
            total = db.fetchone()[0]

            query = """  
                SELECT 
                    i.id_inventario,
                    i.nombre_inventario,
                    COUNT(p.codigo_barras) AS cantidad_items,
                    SUM(CASE WHEN p.conteo IS NOT NULL AND p.conteo > 0 THEN 1 ELSE 0 END) AS cantidad_productos_con_conteo,
                    SUM(p.stock) AS total_stock,  -- Sumar el stock total
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
                query += """ WHERE i.id_inventario LIKE %s OR i.nombre_inventario LIKE %s """
                params.extend([f"%{filter}%", f"%{filter}%"])

            query += " GROUP BY i.id_inventario"

            if order_by in ["nombre_inventario", "cantidad_items", "cantidad_productos_con_conteo", "total_stock", "fecha_creacion", "fecha_lectura"] and order in ["ASC", "DESC"]:
                query += f" ORDER BY {order_by} {order}"
            else:
                query += " ORDER BY i.nombre_inventario ASC"

            if current_page is not None and page_size is not None:
                offset = (current_page - 1) * page_size
                query += f" LIMIT %s OFFSET %s"
                params.extend([page_size, offset])
                

            db.execute(query, params)
            inventarios = db.fetchall()

            for inventario in inventarios:
                cantidad_items = inventario[2]  # La cantidad de códigos de barras
                print(f"Inventario: {inventario[1]} - Códigos de barras: {cantidad_items}")  # Imprimir el nombre y la cantidad de códigos de barras
                list_inventarios.append(
                    {
                        "id_inventario": inventario[0],
                        "nombre_inventario": inventario[1],
                        "cantidad_items": inventario[2],
                        "cantidad_productos_con_conteo": inventario[3],
                        "total_stock": inventario[4],  # Nuevo campo total_stock
                        "fecha_creacion": inventario[5],
                        "fecha_lectura": inventario[6],
                        "id_usuario": inventario[7],
                        "id_perfil": inventario[8]
                    }
                )

            return {"total": total, "inventories": list_inventarios}
        except Exception as e:
            print(e)
            return {"error": str(e)}
      
          
          
          
          
          
          
          
      
    # async def get_all_inventarios(self, filter = None, order_by = None, order = None, current_page=None, page_size=None):
    #   with Database() as db:
    #       total = 0
    #       list_inventarios = []
    #       params_total = []
    #       params = []
    #       try:
          
          
          
    #           print("Ordenando por:", order_by, "en orden:", order)
    #           print("Filtro:", filter)
          

    #           query_total = "SELECT COUNT(id_inventario) FROM inventarios"
    #           if filter:
    #               query_total += " WHERE nombre_inventario LIKE %s"
    #               params_total.append(f"%{filter}%")
                
    #           db.execute(query_total, params_total)
    #           total = db.fetchone()[0]

    #           query = """  
    #               SELECT 
    #                   i.id_inventario,
    #                   i.nombre_inventario,
    #                   COUNT(p.id_producto) AS cantidad_items,
    #                   SUM(CASE WHEN p.conteo IS NOT NULL AND p.conteo > 0 THEN 1 ELSE 0 END) AS cantidad_productos_con_conteo,
    #                   i.fecha_creacion,
    #                   i.fecha_lectura,
    #                   i.id_usuario,
    #                   u.id_perfil
    #               FROM inventarios AS i
    #               LEFT JOIN productos AS p 
    #                 ON i.id_inventario = p.id_inventario
    #               LEFT JOIN usuarios AS u
    #                 ON i.id_usuario = u.id_usuario
    #           """
    #           if filter:
    #               query += """ WHERE i.nombre_inventario LIKE %s """
    #               params.append(f"%{filter}%")

    #           query += " GROUP BY i.id_inventario"
            
    #           if order_by in ["nombre_inventario", "cantidad_items", "cantidad_productos_con_conteo", "fecha_creacion", "fecha_lectura"] and order in ["ASC", "DESC"]:
    #               query += f" ORDER BY {order_by} {order}"
    #           else:
    #               query += " ORDER BY i.nombre_inventario ASC"
    #           if current_page != None and page_size != None:
    #                 query += " LIMIT %s OFFSET %s"
    #                 params.append(page_size)
    #                 params.append((current_page - 1) * page_size)


    #           db.execute(query, params)
    #           inventarios = db.fetchall()

    #           for inventario in inventarios:
    #               list_inventarios.append(
    #                   {
    #                       "id_inventario": inventario[0],
    #                       "nombre_inventario": inventario[1],
    #                       "cantidad_items": inventario[2],
    #                       "cantidad_productos_con_conteo": inventario[3],
    #                       "fecha_creacion": inventario[4],
    #                       "fecha_lectura": inventario[5],
    #                       "id_usuario": inventario[6],
    #                       "id_perfil": inventario[7]
    #                   }
    #               )
    #           return {"total": total, "inventories": list_inventarios}
    #       except Exception as e:
    #           print(e)
    #           return {"error": str(e)}

      
    async def get_inventario_by_id(self, id_inventario: int):
      with Database() as db:
        try:
          query = "SELECT nombre_inventario FROM inventarios WHERE id_inventario = %s"
          db.execute(query, (id_inventario,))
          inventario = db.fetchone()
          if not inventario:
            return None
          return ConsultNameInventory(
            nombre_inventario=inventario[0] 
          )
        except Exception as e:
          print(e)
          return {"error": str(e)}
      
    async def update_inventario(self, id_inventario: int, nombre_inventario: str):
      with Database() as db:
        try:
          query_inventario = """
            UPDATE inventarios
            SET nombre_inventario = %s
            WHERE id_inventario = %s;
          """
          db.execute(
            query_inventario,
            (
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
                
              db.execute("DELETE FROM productos WHERE id_inventario = %s", (id_inventario,))
            
              db.execute("DELETE FROM inventarios WHERE id_inventario = %s", (id_inventario,))
              db.commit()
              return {"message": "Inventario y productos asociados eliminados correctamente"}
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
                    COUNT(p.codigo_barras) AS cantidad_productos,
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
          
    


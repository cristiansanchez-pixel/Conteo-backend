from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.inventario_model import CreateInventarioModel


class InventarioController:
  async def create_inventario(self, inventario: CreateInventarioModel):
    with Database() as db:
      try:
        id_inventario = str(uuid())
        query_inventario = """
          INSERT INTO inventarios
          (id_inventario, id_usuario, usuarios_id_perfil, nombre_inventario)
          VALUES(%s, %s, %s, %s);
        """
        db.execute(
          query_inventario,
          (
              id_inventario,
              inventario.id_usuario,  
              inventario.usuarios_id_perfil,
              inventario.nombre_inventario
          ),
        )
        db.commit()
        return {"id_inventario": id_inventario, "nombre_inventario": inventario.nombre_inventario}
      except Exception as e:
        print(e)
        db.rollback()
        return {"error": str(e)}
      
  async def get_all_inventarios(self):
    with Database() as db:
      try:
        query = "SELECT id_inventario, id_usuario, usuarios_id_perfil, nombre_inventario FROM inventarios"
        db.execute(query)
        inventarios = db.fetchall()
        
        if not inventarios:
          return []                
        
        return [
          CreateInventarioModel(
            id_inventario=inventario[0], id_usuario=inventario[1], usuarios_id_perfil=inventario[2], nombre_inventario=inventario[3]
          ) for inventario in inventarios
        ]
      except Exception as e:
        print(e)
        return {"error": str(e)}
      
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
      
  async def update_inventario(self, id_inventario: int, inventario: CreateInventarioModel):
    with Database() as db:
      try:
        query_inventario = """
          UPDATE inventarios
          SET id_usuario = %s, usuarios_id_perfil = %s, nombre_inventario = %s
          WHERE id_inventario = %s;
        """
        db.execute(
          query_inventario,
          (
              inventario.id_usuario,  
              inventario.usuarios_id_perfil,
              inventario.nombre_inventario,
          ),
        )
        
        for producto in inventario.productos:  
          query_update_producto = """
          UPDATE productos
          SET descripcion = %s, cantidad = %s, data = %s, conteo = %s
          WHERE id_producto = %s AND id_inventario = %s;
          """
          db.execute(
          query_update_producto,
          (producto.descripcion, producto.cantidad, producto.data, producto.conteo, producto.id_producto, id_inventario),
            )
        db.commit()
        return {"message": "Inventario y productos actualizados correctamente", "id_inventario": id_inventario}
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
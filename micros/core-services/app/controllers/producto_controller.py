from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.producto_model import (CreateProductoModel, 
                                    UpdateProductoModel, 
                                    ConsultProductoModel,
                                    DeleteProductoModel,
                                    ConsultAllProductoModel)

class ProductController:
    async def create_producto(self, producto: CreateProductoModel):
        with Database() as db:
            try:
                #id_inventario = inventarios.id_inventario if inventarios.id_inventario is not None else 1
                query_product = """
                    INSERT INTO productos
                    (id_usuario, id_perfil,id_inventario, nombre, descripcion, cantidad, conteo)
                    VALUES(%s, %s, %s, %s, %s, %s, %s);
                """
                db.execute(
                    query_product,
                    (
                        producto.id_usuario,
                        producto.id_perfil,
                        producto.id_inventario,
                        producto.nombre,
                        producto.descripcion,
                        producto.cantidad,
                        producto.conteo
                    ),
                )               
                return {"id_usuario":producto.id_usuario,"id_perfil":producto.id_perfil ,"id_inventario":producto.id_inventario ,"nombre":producto.nombre, "descripcion": producto.descripcion, "cantidad": producto.cantidad, "conteo": producto.conteo}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
    
    async def get_all_productos(self):
        with Database() as db:
            try:
                query = "SELECT id_producto, nombre, descripcion, cantidad, data, conteo FROM `productos`"
                db.execute(query)
                productos = db.fetchall()
                
                if not productos:
                    return []                
                
                return [
                    ConsultAllProductoModel(
                        #   id_usuario=producto[0],
                        #   id_perfil=producto[1],
                        id_producto=producto[0],
                        nombre=producto[1],
                        descripcion=producto[2],
                        cantidad=producto[3],
                        data=producto[4],
                        conteo=producto[5]
                    ) for producto in productos
                ]
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def get_producto_by_barcode(self, codigo_barras: int, producto: ConsultProductoModel):
        with Database() as db:
            try:
                query = "SELECT codigo_barras, nombre, descripcion, cantidad, data, conteo FROM `productos` WHERE codigo_barras = %s"
                db.execute(query, (codigo_barras,))
                producto = db.fetchone()
                if not producto:
                    return None
                return ConsultProductoModel(
                    codigo_barras= producto[0],
                    nombre=producto[1],
                    descripcion=producto[2],
                    cantidad=producto[3],
                    data=producto[4],
                    conteo=producto[5]
                )
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def update_producto(self, codigo_barras: str, producto: UpdateProductoModel):
        with Database() as db:
            try:
                query = """
                    UPDATE productos
                    SET nombre=%s, descripcion = %s, cantidad = %s, data = %s, conteo = %s
                    WHERE codigo_barras = %s;
                """
                db.execute(
                    query,
                    (
                        producto.nombre,
                        producto.descripcion,
                        producto.cantidad,
                        producto.data,
                        producto.conteo,
                        codigo_barras,
                    ),
                )
                db.commit()
                return {"codigo_barras": codigo_barras, "nombre": producto.nombre, "descripcion": producto.descripcion, "cantidad": producto.cantidad, "conteo": producto.conteo}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
            
    async def delete_producto(self, id_producto: str):
        with Database() as db:
            try:
                check_query = "SELECT id_producto FROM productos WHERE id_producto = %s"
                db.execute(check_query, (id_producto,))
                if not db.fetchone():
                    return {"error": "Producto no encontrado"}
                
                query = "DELETE FROM productos WHERE id_producto = %s"
                db.execute(query, (id_producto,))
                db.commit()
                return {"id_producto": id_producto}
            
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
    



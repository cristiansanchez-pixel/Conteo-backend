from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.producto_model import CreateProductoModel, UpdateProductoModel, ConsultProductoModel

class ProductController:
    async def create_producto(self, producto: CreateProductoModel):
        with Database() as db:
            try:
                id_producto = str(uuid())
                query_product = """
                    INSERT INTO conteo.productos
                    (id_producto, descripcion, cantidad, data, conteo)
                    VALUES(%s, %s, %s, %s);
                """
                db.execute(
                    query_product,
                    (
                        id_producto,
                        producto.descripcion,
                        producto.cantidad,
                        producto.data,
                        producto.conteo
                    ),
                )
                db.commit()
                return {"id_producto": id_producto, "descripcion": producto.descripcion}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
    
    async def get_all_productos(self):
        with Database() as db:
            try:
                query = "SELECT id_producto, descripcion, cantidad, conteo data FROM `productos`"
                db.execute(query)
                productos = db.fetchall()
                
                if not productos:
                    return []                
                
                return [
                    ConsultProductoModel(
                        id_producto=producto[0], descripcion=producto[1], cantidad=producto[2], data=producto[3], conteo=producto[4]
                    ) for producto in productos
                ]
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def get_producto_by_id(self, id_producto: str):
        with Database() as db:
            try:
                query = "SELECT id_producto, descripcion, cantidad, data, conteo FROM `productos` WHERE id_producto = %s"
                db.execute(query, (id_producto,))
                producto = db.fetchone()
                if not producto:
                    return None
                return ConsultProductoModel(
                    id_producto=producto[0], descripcion=producto[1],
                    cantidad=producto[2], data=producto[3], conteo=producto[4]
                )
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def update_producto(self, id_producto: str, producto: UpdateProductoModel):
        with Database() as db:
            try:
                query = """
                    UPDATE productos
                    descripcion = %s, cantidad = %s, data = %s, conteo = %s
                    WHERE id_producto = %s;
                """
                db.execute(
                    query,
                    (
                        producto.descripcion,
                        producto.cantidad,
                        producto.data,
                        producto.conteo,
                        id_producto,
                    ),
                )
                db.commit()
                return {"id_producto": id_producto, "descripcion": producto.descripcion}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}


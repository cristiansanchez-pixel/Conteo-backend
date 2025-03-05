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
                    (codigo_barras, 
                    id_usuario,  
                    id_perfil,
                    id_inventario,
                    nombre, 
                    descripcion, 
                    cantidad,
                    precio_unidad)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
                """
                
                params = (
                    producto.codigo_barras,
                    producto.id_usuario,
                    producto.id_perfil,
                    producto.id_inventario,
                    producto.nombre,
                    producto.descripcion if producto.descripcion else None,
                    producto.cantidad,
                    producto.precio_unidad
            )
                # )  
                print("Parámetros a ejecutar:", params)  # Agrega esta línea para depuración

            # Ejecuta la consulta con los parámetros verificados
                db.execute(query_product, params)
                db.commit()        
                
                
                return {"codigo_barras": producto.codigo_barras,
                        "id_usuario":producto.id_usuario,
                        "id_inventario":producto.id_inventario,
                        "id_perfil":producto.id_perfil,
                        "nombre":producto.nombre,
                        "descripcion": producto.descripcion,
                        "cantidad": producto.cantidad,
                        "precio_unidad": producto.precio_unidad}
            except Exception as e:
                print("Error en la ejecución:", e)
                db.rollback()
                return {"error": str(e)}
    
    async def get_all_productos(self, id_inventario: int):
        with Database() as db:
            total = 0
            list_productos = []
            try:
                query = """
                    SELECT 
                        p.codigo_barras, 
                        p.nombre, 
                        p.descripcion,
                        p.cantidad, 
                        p.data, 
                        p.conteo,
                        p.precio_unidad,
                        p.id_producto, 
                        i.id_usuario,     
                        i.usuarios_id_perfil,
                        i.id_inventario
                    FROM productos p
                    JOIN inventarios i ON p.id_inventario = i.id_inventario
                    JOIN usuarios u ON i.id_usuario = u.id_usuario
                    WHERE i.id_inventario = %s
                """
                db.execute(query, (id_inventario,))
                productos = db.fetchall()
                
                print("Productos obtenidos:", productos)
                
                if not productos:
                    return {"total": total, "products": [] }             
                
                
                    
                for producto in productos:  
                    list_productos.append(
                        {
                        "codigo_barras": producto[0],
                        "nombre": producto[1],
                        "descripcion": producto[2],
                        "cantidad": producto[3],
                        "data": producto[4],
                        "conteo": producto[5],
                        "precio_unidad": producto[6],
                        "id_usuario": producto[7],
                        "usuario_id_perfil": producto[8],
                        "id_inventario": producto[9],
                        "id_producto": producto[10]
                    }
                        )
                    
                return {"total": total, "products": list_productos}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def get_producto_by_barcode(self, codigo_barras: int, producto: ConsultProductoModel):
        with Database() as db:
            try:
                query = """
                    SELECT 
                        p.codigo_barras, 
                        p.nombre, 
                        p.descripcion,
                        p.cantidad, 
                        p.data, 
                        p.conteo,
                        p.precio_unidad,
                        p.id_producto, 
                        i.id_usuario,     
                        i.usuarios_id_perfil,
                        i.id_inventario
                    FROM productos p
                    JOIN inventarios i ON p.id_inventario = i.id_inventario
                    JOIN usuarios u ON i.id_usuario = u.id_usuario
                    WHERE p.codigo_barras = %s
                """
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
                    conteo=producto[5],
                    precio_unidad=producto[6],
                    id_producto=producto[7],
                    id_usuario=producto[8],
                    id_perfil=producto[9],
                    id_inventario=producto[10]
                )
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def update_producto(self, codigo_barras: int, producto: UpdateProductoModel):
        with Database() as db:
            try:
                query = """
                    UPDATE productos
                    SET codigo_barras= %s, nombre=%s, descripcion = %s, cantidad = %s, data = %s, conteo = %s, precio_unidad = %s
                    WHERE codigo_barras = %s;
                """
                db.execute(
                    query,
                    (
                        producto.codigo_barras,
                        producto.nombre,
                        producto.descripcion,
                        producto.cantidad,
                        producto.data,
                        producto.conteo,
                        producto.precio_unidad,
                        codigo_barras,
                    ),
                )
                db.commit()
                return {"codigo_barras": codigo_barras, "nombre": producto.nombre, "descripcion": producto.descripcion, "cantidad": producto.cantidad, "conteo": producto.conteo, "precio_unidad": producto.precio_unidad}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
            
    async def delete_producto_by_barcode(self, codigo_barras: int):
        with Database() as db:
            try:
                check_query = "SELECT codigo_barras FROM productos WHERE codigo_barras = %s"
                db.execute(check_query, (codigo_barras,))
                if not db.fetchone():
                    return {"error": "Producto no encontrado"}
                
                query = "DELETE FROM productos WHERE codigo_barras = %s"
                db.execute(query, (codigo_barras,))
                db.commit()
                return {"codigo_barras": codigo_barras}
            
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
    



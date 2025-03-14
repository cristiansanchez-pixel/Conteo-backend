from uuid import uuid4 as uuid
from ..mysql import Database
from ..models.producto_model import (CreateProductoModel,
                                    UpdateConteoModel, 
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
                    descripcion, 
                    stock)
                    VALUES(%s, %s, %s, %s, %s, %s);
                """
                
                params = (
                    producto.codigo_barras,
                    producto.id_usuario,
                    producto.id_perfil,
                    producto.id_inventario,
                    producto.descripcion if producto.descripcion else None,
                    producto.stock
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
                        "descripcion": producto.descripcion,
                        "stock": producto.stock}
            except Exception as e:
                print("Error en la ejecución:", e)
                db.rollback()
                return {"error": str(e)}
            
    async def get_all_productos(self, id_inventario: int, filter=None, order_by=None, order=None, current_page=None, page_size=None):
      with Database() as db:
        total = 0
        list_productos = []
        try:
            query = """
                SELECT 
                    p.codigo_barras, 
                    p.descripcion,
                    p.stock, 
                    p.data, 
                    p.conteo,
                    p.id_producto, 
                    i.id_usuario,     
                    i.usuarios_id_perfil,
                    i.id_inventario,
                    i.nombre_inventario
                FROM productos p
                JOIN inventarios i ON p.id_inventario = i.id_inventario
                JOIN usuarios u ON i.id_usuario = u.id_usuario
                WHERE i.id_inventario = %s
            """

      
            params = [id_inventario]

            if filter:
                query += """
                    AND (JSON_UNQUOTE(JSON_EXTRACT(p.data, '$.DESCRIPCION')) LIKE %s 
                    OR p.codigo_barras LIKE %s)
                """
                params.extend([f"%{filter}%", f"%{filter}%"])



            if current_page is not None and page_size is not None:
                offset = (current_page - 1) * page_size
                query += f" LIMIT %s OFFSET %s"
                params.extend([page_size, offset])

            count_query = """
                SELECT COUNT(*) 
                FROM productos p
                JOIN inventarios i ON p.id_inventario = i.id_inventario
                WHERE i.id_inventario = %s
            """
            db.execute(count_query, (id_inventario,))
            total = db.fetchone()[0]

            db.execute(query, tuple(params))
            productos = db.fetchall()

            print("Productos obtenidos:", productos)

            if not productos:
                return {"total": total, "products": []}
            
            # Formatear los resultados
            for producto in productos:
                list_productos.append(
                    {
                        "codigo_barras": producto[0],
                        "descripcion": producto[1],
                        "stock": producto[2],
                        "data": producto[3],
                        "conteo": producto[4],
                        "id_producto": producto[5],
                        "id_usuario": producto[6],
                        "usuario_id_perfil": producto[7],
                        "id_inventario": producto[8],
                        "nombre_inventario": producto[9]
                    }
                )

            return {"total": total, "products": list_productos}

        except Exception as e:
            print(e)
            db.rollback()
            return {"error": str(e)}

    
    # async def get_all_productos(self, id_inventario: int, filter=None, order_by=None, order=None, current_page=None, page_size=None):
    #     with Database() as db:
    #         total = 0
    #         list_productos = []
    #         try:
                
    #             query = """
    #                 SELECT 
    #                     p.codigo_barras, 
    #                     p.descripcion,
    #                     p.stock, 
    #                     p.data, 
    #                     p.conteo,
    #                     p.id_producto, 
    #                     i.id_usuario,     
    #                     i.usuarios_id_perfil,
    #                     i.id_inventario,
    #                     i.nombre_inventario
    #                 FROM productos p
    #                 JOIN inventarios i ON p.id_inventario = i.id_inventario
    #                 JOIN usuarios u ON i.id_usuario = u.id_usuario
    #                 WHERE i.id_inventario = %s
    #             """
    #             db.execute(query, (id_inventario,))
    #             productos = db.fetchall()
                
    #             print("Productos obtenidos:", productos)
                
    #             if not productos:
    #                 return {"total": total, "products": [] }             
                
                
                    
    #             for producto in productos:  
    #                 list_productos.append(
    #                     {
    #                     "codigo_barras": producto[0],
    #                     "descripcion": producto[1],
    #                     "stock": producto[2],
    #                     "data": producto[3],
    #                     "conteo": producto[4],
    #                     "id_producto": producto[5],
    #                     "id_usuario": producto[6],
    #                     "usuario_id_perfil": producto[7],
    #                     "id_inventario": producto[8],
    #                     "nombre_inventario": producto[9]
    #                 }
    #                     )
                    
    #             return {"total": total, "products": list_productos}
    #         except Exception as e:
    #             print(e)
    #             db.rollback()
    #             return {"error": str(e)}
            
    async def get_all_products(self):
        with Database() as db:
            
            list_productos = []
            try:
                query = """
                    SELECT 
                        p.codigo_barras, 
                        p.stock, 
                        p.data, 
                        p.conteo
                    FROM productos p
                """
                db.execute(query, ())
                productos = db.fetchall()
                
                print("Productos obtenidos:", productos)
                
                if not productos:
                    return { "products": [] }             
                
                
                    
                for producto in productos:  
                    list_productos.append(
                        {
                        "codigo_barras": producto[0],
                        "stock": producto[1],
                        "data": producto[2],
                        "conteo": producto[3]
                    }
                        )
                    
                return { "products": list_productos}
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
                        p.descripcion,
                        p.stock, 
                        p.data, 
                        p.conteo,
                        p.id_producto, 
                        i.id_usuario,     
                        i.usuarios_id_perfil,
                        i.id_inventario
                    FROM productos p
                    JOIN inventarios i ON p.id_inventario = i.id_inventario
                    JOIN usuarios u ON i.id_usuario = u.id_usuario
                    WHERE p.codigo_barras LIKE %s
                """
                db.execute(query, (f"%{codigo_barras}%",))
                producto = db.fetchone()
                if not producto:
                    return None
                return ConsultProductoModel(
                    codigo_barras= producto[0],
                    descripcion=producto[1],
                    stock=producto[2],
                    data=producto[3],
                    conteo=producto[4],
                    id_producto=producto[5],
                    id_usuario=producto[6],
                    id_perfil=producto[7],
                    id_inventario=producto[8]
                )
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}

    async def update_conteo(self, codigo_barras: int, producto: UpdateConteoModel):
        with Database() as db:
            try:
                query = """
                    UPDATE productos
                    SET codigo_barras= %s, conteo = %s
                    WHERE codigo_barras = %s;
                """
                db.execute(
                    query,
                    (
                        producto.codigo_barras,
                        producto.conteo,
                        codigo_barras,
                    ),
                )
                db.commit()
                return {"codigo_barras": codigo_barras, "conteo": producto.conteo}
            except Exception as e:
                print(e)
                db.rollback()
                return {"error": str(e)}
            
    async def update_producto(self, codigo_barras: int, producto: UpdateProductoModel):
        with Database() as db:
            try:
                query = """
                    UPDATE productos
                    SET codigo_barras= %s, stock = %s, data = %s
                    WHERE codigo_barras = %s;
                """
                db.execute(
                    query,
                    (
                        producto.codigo_barras,
                        producto.stock,
                        producto.data,
                        codigo_barras,
                    ),
                )
                db.commit()
                return {"codigo_barras": codigo_barras,
                        "stock": producto.stock,
                        "data": producto.data
                        }
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
    



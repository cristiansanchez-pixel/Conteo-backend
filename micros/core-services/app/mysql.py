import MySQLdb
from app.config import get_env

settings = get_env()



db_config = {
    "host": settings.DB_HOST,
    "user":  settings.DB_USER,
    "passwd":  settings.DB_PASS,
    "db":  settings.DB_NAME,
}

class Database:
    def __init__(self):
        self._conn = None #Para almacenar la conexión a la base de datos. Se inicia en None, porque aún no se ha establecido una conexión
        self._cursor = None #Se us para ejecutar consulta SQL. Se inicia en None, porque aún no se ha establecido una conexión

        try: #Intenta conectar a la base de datos
            print("Inicializando DB connection")
            self._conn = MySQLdb.connect(**db_config)#Establece la conexión con MySQL, usando los datos de configuración
            self._cursor = self._conn.cursor()
        except MySQLdb.Error as e: #Si hay un error, imprime el error
            print(f"Error connecting to MySQL Database: {e}")
            self.close(commit=False)
            
    def __enter__(self):
        print("Enter DB connection")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exit DB connection")
        self.close()
        
    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor
      
    def commit(self): #Guarda o confirma los cambios en la base de datos, permitiendo que los cambios sean permanentes
        self.connection.commit()
        print("Commit DB connection")
        
    def rollback(self):#Deshace los cambios en la base de datos, permitiendo que los cambios no sean permanentes
        self.connection.rollback()
        print("Rollback DB connection")
        
    def close(self, commit=True): #Cierra la conexión a la base de datos de manera segura, se usa cuando ya no necesitas realizar mas consultas
        if commit and self.connection:
            self.commit()
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self._cursor = None
        self._conn = None
        print("Cerrando DB connection")
        
    def execute(self, sql, params=None): #Ejecuta una consulta SQL en la base de datos
        return self.cursor.execute(sql, params or ())
      
    def lastrowid(self):#Devuelve el ID del último registro insertado en la base de datos
        return self.cursor.lastrowid
      
    def fetchall(self):#Devuelve todos los registros de la consulta SQL
        return self.cursor.fetchall()
      
    def fetchone(self): #
        return self.cursor.fetchone()
      
    def query(self, sql, params=None): #Ejecuta una consulta SQL en la base de datos y devuelve los registros
        self.cursor.execute(sql, params or ())
        return self.fetchall()
      

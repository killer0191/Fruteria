import pyodbc

class Conexion:
    def __init__(self):
        self.server = "localhost"
        self.database = "Fruteria"
        self.username = "sa"
        self.password = ""
        self.connection = None

    def conectar(self):
        try:
            # Cadena de conexión
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};"
            
            # Conectar a la base de datos
            self.connection = pyodbc.connect(connection_string)
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cerrar_conexion(self):
        try:
            if self.connection:
                self.connection.close()
                print("Conexión cerrada.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

    def execute_query(self, query, parameters):
      try:
        if self.connection:
            cursor = self.connection.cursor()
            if parameters:
                result = cursor.execute(query, parameters).fetchall()
            else:
                result = cursor.execute(query).fetchall()
            return result
        else:
            print("Error: No hay conexión a la base de datos.")
            return None
      except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

    def insert(self, table, data):
      try:
        if self.connection:
            columns = ", ".join(data.keys())
            values = ", ".join(["?" for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            parameters = list(data.values())
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
            self.connection.commit()
            print("Inserción exitosa.")
        else:
            print("Error: No hay conexión a la base de datos.")
      except Exception as e:
        print(f"Error al insertar: {e}")
    
    def execute_update(self, query, parameters):
      try:
        if not self.connection:
            print("Error: No hay conexión a la base de datos.")
            return False

        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        self.connection.commit()
        if cursor.rowcount > 0:
            print("Actualización exitosa.")
            return True
        else:
            print("Advertencia: No se realizaron cambios. Puede ser que no exista el registro.")
            return False
      except Exception as e:
        print(f"Error al ejecutar la actualización: {e}")
        return False
    
    def update(self, table, data, where):
        try:
            if self.connection:
                set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
                where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])
                query = f"UPDATE {table} SET {set_clause} WHERE {where_clause};"
                parameters = list(data.values()) + list(where.values())
                self.connection.execute(query, parameters)
                self.connection.commit()  # Asegúrate de que esta línea esté presente
                print("Actualización exitosa.")
            else:
                print("Error: No hay conexión a la base de datos.")
        except Exception as e:
            print(f"Error al actualizar: {e}")
    
    def delete(self, table, where):
        try:
            if self.connection:
                where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])
                query = f"DELETE FROM {table} WHERE {where_clause};"
                parameters = list(where.values())
                self.connection.execute(query, parameters)
                self.connection.commit()
                print("Borrado exitoso.")
            else:
                print("Error: No hay conexión a la base de datos.")
        except Exception as e:
            print(f"Error al borrar: {e}")
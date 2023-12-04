from Backend.Interfaces.IProductos import IProducto
from Backend.conexion import Conexion
from typing import List
from typing import Union

class ProductoRepository(IProducto):
    def __init__(self, conexion: Conexion):
        self.conexion = conexion

    def insertar(self, nombre: str, cantidad: int, precio: float, idProveedor: int) -> bool:
        try:
            data_insert = {"Nombre": nombre, "Cantidad": cantidad, "Precio": precio, "IdProveedor": idProveedor}
            self.conexion.insert("Productos", data_insert)
            print("Inserción exitosa en Productos.")
            return True
        except Exception as e:
            print(f"Error al insertar en Productos: {e}")
            return False

    def obtener_todo(self) -> List[dict]:
        try:
            self.conexion.conectar()
            query = "SELECT * FROM Productos;"
            parameters = ""
            result = self.conexion.execute_query(query, parameters)
            return result
        except Exception as e:
            print(f"Error al obtener datos de Productos: {e}")
            return []

    def obtener(self, id: int) -> List[dict]:
        try:
            self.conexion.conectar()
            query = "SELECT * FROM Productos WHERE IdProducto = ?;"
            parameters = (id,)
            result = self.conexion.execute_query(query, parameters)
            return result
        except Exception as e:
            print(f"Error al obtener datos de Productos: {e}")
            return []

    def editar_datos(self, idProducto: int, nombre: str, cantidad: int, precio: float, idProveedor: int) -> bool:
      try:
        data_update = {"Nombre": nombre, "Cantidad": cantidad, "Precio": precio, "IdProveedor": idProveedor}
        where_clause = {"IdProducto": idProducto}
        self.conexion.update("Productos", data_update, where_clause)
        print("Actualización exitosa en Productos.")
        return True
      except Exception as e:
        print(f"Error al actualizar en Productos: {e}")
        return False

    def borrar(self, id: int) -> bool:
        try:
            where_clause = {"IdProducto": id}
            self.conexion.delete("Productos", where_clause)
            print("Borrado exitoso en Productos.")
            return True
        except Exception as e:
            print(f"Error al borrar en Productos: {e}")
            return False
    
    def existe_producto(self, codigo_producto):
      try:
        self.conexion.conectar()
        query = f"SELECT IdProducto FROM Productos WHERE IdProducto = {codigo_producto};"
        parameters=""
        result = self.conexion.execute_query(query,parameters)
        print("resultado2: ", result)
        return result[0][0] > 0 if result else False
      except Exception as e:
        print(f"Error al verificar existencia del producto: {e}")
        return False
      finally:
        self.conexion.cerrar_conexion()
    
    def obtener_precio_producto(self, codigo_producto) -> Union[float, None]:
        try:
            self.conexion.conectar()
            query = f"SELECT Precio FROM Productos WHERE IdProducto = {codigo_producto};"
            parameters=""
            result = self.conexion.execute_query(query,parameters)
            
            print("Precio: ", result)
            # Verifica si se obtuvo algún resultado
            if result:
                return result[0][0]
            else:
                print(f"No se encontró el precio para el producto con código {codigo_producto}")
                return None
        except Exception as e:
            print(f"Error al obtener el precio del producto: {e}")
            return None
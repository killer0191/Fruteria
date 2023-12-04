from Backend.conexion import Conexion
from typing import List

class ProveedorRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_proveedores(self):
      try:
        self.conexion.conectar()
        query = "SELECT Proveedores.IdProveedor, Persona.Nombre FROM Proveedores INNER JOIN Persona ON Proveedores.IdPersona = Persona.IdPersona;"
        result = self.conexion.execute_query(query, None)
        return result
      except Exception as e:
        print(f"Error al obtener proveedores: {e}")
        return None

    def ingresar_proveedor(self, nombre, direccion, telefono):
        try:
            self.conexion.conectar()
            proveedor_data = {
                "Nombre": nombre,
                "Direccion": direccion,
                "Telefono": telefono
            }
            self.conexion.insert("Proveedores", proveedor_data)
            return True
        except Exception as e:
            print(f"Error al ingresar proveedor: {e}")
            return False
        finally:
            self.conexion.cerrar_conexion()

    def actualizar_proveedor(self, id_proveedor, nombre, direccion, telefono):
        try:
            self.conexion.conectar()
            proveedor_data = {
                "Nombre": nombre,
                "Direccion": direccion,
                "Telefono": telefono
            }
            where_clause = {"IdProveedor": id_proveedor}
            self.conexion.update("Proveedores", proveedor_data, where_clause)
            return True
        except Exception as e:
            print(f"Error al actualizar proveedor: {e}")
            return False
        finally:
            self.conexion.cerrar_conexion()

    def eliminar_proveedor(self, id_proveedor):
        try:
            self.conexion.conectar()
            where_clause = {"IdProveedor": id_proveedor}
            self.conexion.delete("Proveedores", where_clause)
            return True
        except Exception as e:
            print(f"Error al eliminar proveedor: {e}")
            return False
        finally:
            self.conexion.cerrar_conexion()

    def obtener_empresas(self) -> List[dict]:
        try:
            self.conexion.conectar()
            query = "SELECT IdEmpresa, Nombre FROM Empresas;"
            parameters = ""

            result = self.conexion.execute_query(query, parameters)

            return result
        except Exception as e:
            print(f"Error al obtener datos de Empresas: {e}")
            return []
        finally:
            self.conexion.cerrar_conexion()
    
    def insertar(self, nombre: str, apellidos: str, rfc: str, id_empresa: int) -> bool:
        try:
            self.conexion.conectar()

            # Insertar en la tabla Persona
            if not self.insertar_persona(nombre, apellidos, rfc):
                print("Error al insertar en Persona.")
                return False

            id_persona = self.obtener_id_persona(nombre, apellidos, rfc)

            if id_persona == -1:
                print("Error al obtener IdPersona.")
                return False

            if not self.insertar_proveedor(id_persona, id_empresa):
                print("Error al insertar en Proveedores.")
                return False

            print("Registro exitoso en Persona y Proveedores.")
            return True
        except Exception as e:
            print(f"Error al registrar: {e}")
            return False
        finally:
            self.conexion.cerrar_conexion()

    def insertar_persona(self, nombre: str, apellidos: str, rfc: str) -> bool:
        try:
            data_insert = {"Nombre": nombre, "Apellidos": apellidos, "RFC": rfc}
            self.conexion.insert("Persona", data_insert)

            print("Inserción exitosa en Persona.")
            return True
        except Exception as e:
            print(f"Error al insertar en Persona: {e}")
            return False

    def insertar_proveedor(self, id_persona: int, id_empresa: int) -> bool:
        try:
            data_insert = {"IdPersona": id_persona, "IdEmpresa": id_empresa}
            self.conexion.insert("Proveedores", data_insert)

            print("Inserción exitosa en Proveedores.")
            return True
        except Exception as e:
            print(f"Error al insertar en Proveedores: {e}")
            return False
    
    def obtener_id_persona(self, nombre: str, apellidos: str, rfc: str) -> int:
        query = "SELECT IdPersona FROM Persona WHERE Nombre = ? and Apellidos=? and RFC=?;"
        parameters = (nombre, apellidos, rfc)
        result = self.conexion.execute_query(query, parameters)
        if result is not None and len(result) > 0:
          return result[0][0] 
        else:
          return -1
    
    def obtener(self, id: int) -> List[dict]:
        try:
            self.conexion.conectar()
            query = "SELECT * FROM Proveedores, Persona, Empresas WHERE Proveedores.IdPersona = Persona.IdPersona AND Proveedores.IdEmpresa = Empresas.IdEmpresa AND Proveedores.IdProveedor = ?;"
            parameters = (id,)
            result = self.conexion.execute_query(query, parameters)
            return result
        except Exception as e:
            print(f"Error al obtener datos de Productos: {e}")
            return []

    def editar_datos(self, idProveedor: int, nombre: str, apellidos: str, rfc: str, idEmpresa: int, idPerson: int) -> bool:
      try:
        self.conexion.conectar()

        # Actualizar en la tabla Persona
        data_persona = {"Nombre": nombre, "Apellidos": apellidos, "RFC": rfc}
        where_persona = {"IdPersona": idPerson}
        query_persona = f"UPDATE Persona SET {', '.join([f'{key}=?' for key in data_persona.keys()])} WHERE {', '.join([f'{key}=?' for key in where_persona.keys()])};"
        parameters_persona = list(data_persona.values()) + list(where_persona.values())
        print("Query Persona:", query_persona)
        print("Parametros Persona: ", parameters_persona)
        self.conexion.execute_update(query_persona, parameters_persona)

        # Actualizar en la tabla Proveedores (asegúrate de tener la columna correcta para IdPersona en Proveedores)
        data_proveedores = {"IdEmpresa": idEmpresa}  # Agrega IdPersona aquí si es necesario
        where_proveedores = {"IdProveedor": idProveedor}
        query_proveedores = f"UPDATE Proveedores SET {', '.join([f'{key}=?' for key in data_proveedores.keys()])} WHERE {', '.join([f'{key}=?' for key in where_proveedores.keys()])};"
        parameters_proveedores = list(data_proveedores.values()) + list(where_proveedores.values())
        print("Query Proveedores:", query_proveedores)
        print("Parametros Proveedores: ", parameters_proveedores)
        self.conexion.execute_update(query_proveedores, parameters_proveedores)

        print("Actualización exitosa en Persona y Proveedores.")
        return True
      except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
      finally:
        self.conexion.cerrar_conexion()

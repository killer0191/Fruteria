from Backend.conexion import Conexion
from typing import List

class ClienteRepository:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion

    def obtener_todo(self) -> List[dict]:
        try:
            self.conexion.conectar()
            query = "SELECT Clientes.IdCliente, Persona.Nombre FROM Clientes INNER JOIN Persona ON Clientes.IdPersona = Persona.IdPersona;"
            parameters = ""

            result = self.conexion.execute_query(query, parameters)

            return result
        except Exception as e:
            print(f"Error al obtener datos de Clientes: {e}")
            return []
        finally:
            self.conexion.cerrar_conexion()
    
    def obtener_clientes(self) -> List[dict]:
          try:
            self.conexion.conectar()
            query = "SELECT * FROM Clientes, Persona, Empresas WHERE Clientes.IdPersona = Persona.IdPersona AND Clientes.IdEmpresa = Empresas.IdEmpresa;"
            parameters = ""
            result = self.conexion.execute_query(query, parameters)
            return result
          except Exception as e:
            print(f"Error al obtener datos de Productos: {e}")
            return []

    def obtener(self, id: int) -> List[dict]:
        try:
            self.conexion.conectar()
            query = "SELECT * FROM Clientes, Persona, Empresas WHERE Clientes.IdPersona = Persona.IdPersona AND Clientes.IdEmpresa = Empresas.IdEmpresa AND Clientes.IdCliente=?;"
            parameters = (id,)
            result = self.conexion.execute_query(query, parameters)
            return result
        except Exception as e:
            print(f"Error al obtener datos de Productos: {e}")
            return []

    def existe_cliente(self, codigo_cliente):
      try:
        self.conexion.conectar()
        query = f"SELECT IdCliente FROM Clientes WHERE IdCliente = {codigo_cliente};"
        parameters=""
        result = self.conexion.execute_query(query,parameters)
        print("resultado1: ", result)
        return result[0][0] > 0 if result else False
      except Exception as e:
        print(f"Error al verificar existencia del cliente: {e}")
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

            # Insertar en la tabla Clientes
            if not self.insertar_cliente(id_persona, id_empresa):
                print("Error al insertar en Clientes.")
                return False

            print("Registro exitoso en Persona y Clientes.")
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

    def insertar_cliente(self, id_persona: int, id_empresa: int) -> bool:
        try:
            data_insert = {"IdPersona": id_persona, "IdEmpresa": id_empresa}
            self.conexion.insert("Clientes", data_insert)

            print("Inserción exitosa en Clientes.")
            return True
        except Exception as e:
            print(f"Error al insertar en Clientes: {e}")
            return False
    
    def obtener_id_persona(self, nombre: str, apellidos: str, rfc: str) -> int:
        query = "SELECT IdPersona FROM Persona WHERE Nombre = ? and Apellidos=? and RFC=?;"
        parameters = (nombre, apellidos, rfc)
        result = self.conexion.execute_query(query, parameters)
        if result is not None and len(result) > 0:
          return result[0][0] 
        else:
          return -1
    
    def editar_datos(self, idCliente: int, nombre: str, apellidos: str, rfc: str, idEmpresa: int, idPerson: int) -> bool:
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

        # Actualizar en la tabla Clientes
        data_clientes = {"IdEmpresa": idEmpresa}
        where_clientes = {"IdCliente": idCliente}
        query_clientes = f"UPDATE Clientes SET {', '.join([f'{key}=?' for key in data_clientes.keys()])} WHERE {', '.join([f'{key}=?' for key in where_clientes.keys()])};"
        parameters_clientes = list(data_clientes.values()) + list(where_clientes.values())
        print("Query Clientes:", query_clientes)
        print("Parametros Clientes: ", parameters_clientes)
        self.conexion.execute_update(query_clientes, parameters_clientes)

        print("Actualización exitosa en Persona y Clientes.")
        return True
      except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
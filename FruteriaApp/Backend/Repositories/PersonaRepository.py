from Backend.conexion import Conexion
from Backend.Interfaces.IPersona import IPersona

class PersonaRepository(IPersona):
    def __init__(self, conexion: Conexion):
        self.conexion = conexion

    def insertar(self, nombre: str, apellidos: str, rfc: str) -> bool:
        try:
            data_insert = {"Nombre": nombre, "Apellidos": apellidos, "RFC": rfc}
            self.conexion.insert("Persona", data_insert)

            print("Inserción exitosa en Persona.")
            return True
        except Exception as e:
            print(f"Error al insertar en Persona: {e}")
            return False

    def obtener_todo(self):
        try:
            self.conexion.conectar()

            query = "SELECT * FROM Persona;"
            result = self.conexion.execute_query(query)

            return result
        except Exception as e:
            print(f"Error al obtener datos de Persona: {e}")
            return []
        finally:
            self.conexion.cerrar_conexion()

    def obtener(self, id: int):
        try:
            self.conexion.conectar()

            query = "SELECT * FROM Persona WHERE IdPersona = ?;"
            parameters = (id,)
            result = self.conexion.execute_query(query, parameters)

            return result
        except Exception as e:
            print(f"Error al obtener datos de Persona: {e}")
            return []
        finally:
            self.conexion.cerrar_conexion()

    def obtener_id_persona(self, nombre: str, apellidos: str, rfc: str):
        try:
            query = "SELECT * FROM Persona WHERE Nombre = ? AND Apellidos = ? AND RFC = ?;"
            parameters = (nombre, apellidos, rfc)
            result = self.conexion.execute_query(query, parameters)

            return result
        except Exception as e:
            print(f"Error al obtener datos de Persona: {e}")
            return []

    def editar_datos(self, id: int, nombre: str, apellidos: str, rfc: str) -> bool:
        try:
            self.conexion.conectar()

            query = "UPDATE Persona SET Nombre=?, Apellidos=?, RFC=? WHERE IdPersona=?;"
            parameters = (nombre, apellidos, rfc, id)
            self.conexion.execute_query(query, parameters)

            print("Edición exitosa en Persona.")
            return True
        except Exception as e:
            print(f"Error al editar en Persona: {e}")
            return False
        finally:
            self.conexion.cerrar_conexion()

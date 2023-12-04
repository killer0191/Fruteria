from Backend.conexion import Conexion
from Backend.Interfaces.IUsuario import IUsuario
from Backend.Repositories.PersonaRepository import PersonaRepository

class UsuarioRepository(IUsuario):
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.persona_repo = PersonaRepository(conexion)

    def registrar(self, nombre: str, apellidos: str, rfc: str, email: str, password: str) -> bool:
      try:
        self.conexion.conectar()
        
        varx=self.obtener_id_por_email(email)
        print(varx)
        if self.obtener_id_por_email(email)>-1:
          print("Email ya registrado")
          return False

        if not self.persona_repo.insertar(nombre, apellidos, rfc):
            print("Error al insertar en Persona.")
            return False

        id_persona = self.persona_repo.obtener_id_persona(nombre, apellidos, rfc)

        if id_persona == -1:
            print("Error al obtener IdPersona.")
            return False
        print(id_persona)

        if not self.insertar(email, password, id_persona[0][0]):
            print("Error al insertar en Usuario.")
            return False
        
        print("Registro exitoso en Persona y Usuario.")
        return True
      except Exception as e:
        print(f"Error al registrar: {e}")
        return False
      finally:
        self.conexion.cerrar_conexion()
    
    def insertar(self, email: str, password: str, idPersona: str) -> bool:
        try:
            data_insert = {"Email": email, "Password": password, "IdPersona": idPersona}
            self.conexion.insert("Usuarios", data_insert)

            print("Inserción exitosa en Usuario.")
            return True
        except Exception as e:
            print(f"Error al insertar en Usuario: {e}")
            return False

    def obtener_todo(self):
        # Implementa la lógica para obtener todos los usuarios de la base de datos
        pass

    def iniciar_sesion(self, email, password):
        user_id = self.obtener_id_por_email(email)
        if user_id is not None:
            return self.validar_contraseña(email, password)
        else:
            return False

    def obtener_id_por_email(self, email: str) -> int:
        query = "SELECT IdUsuario FROM Usuarios WHERE Email = ?;"
        parameters = (email,)
        result = self.conexion.execute_query(query, parameters)
        if result is not None and len(result) > 0:
          return result[0][0] 
        else:
          return -1

    def obtener_id_persona(self, nombre: str, apellidos: str, rfc: str) -> int:
        query = "SELECT IdPersona FROM Persona WHERE Nombre = ? and Apellidos=? and RFC=?;"
        parameters = (nombre, apellidos, rfc)
        result = self.conexion.execute_query(query, parameters)
        if result is not None and len(result) > 0:
          return result[0][0] 
        else:
          return -1
        
    def validar_contraseña(self, email: str, password: str) -> bool:
        query = "SELECT IdUsuario FROM Usuarios WHERE Email = ? AND Password = ?;"
        parameters = (email, password)
        result = self.conexion.execute_query(query, parameters)
        return len(result) > 0 

    def editar_datos(self, user_id: int, new_email: str, new_password: str) -> bool:
        # Implementa la lógica para editar los datos de un usuario
        # Retorna True si la edición es exitosa, False en caso contrario
        pass

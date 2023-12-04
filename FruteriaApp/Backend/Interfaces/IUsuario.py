from abc import ABC, abstractmethod
from typing import List

class IUsuario(ABC):
    @abstractmethod
    def registrar(self, email: str, password: str) -> bool:
        pass

    @abstractmethod
    def obtener_todo(self) -> List[dict]:
        pass

    @abstractmethod
    def iniciar_sesion(self, email: str, password: str) -> bool:
        pass

    @abstractmethod
    def obtener_id_por_email(self, email: str) -> int:
        pass

    @abstractmethod
    def validar_contraseña(self, email: str, password: str) -> bool:
        pass

    @abstractmethod
    def editar_datos(self, user_id: int, new_email: str, new_password: str) -> bool:
        pass

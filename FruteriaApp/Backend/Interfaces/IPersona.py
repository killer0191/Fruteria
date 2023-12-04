from abc import ABC, abstractmethod
from typing import List

class IPersona(ABC):
    @abstractmethod
    def insertar(self, nombre: str, apellidos: str, rfc: str) -> bool:
        pass

    @abstractmethod
    def obtener_todo(self) -> List[dict]:
        pass

    @abstractmethod
    def obtener(self, id: int) -> List[dict]:
        pass


    @abstractmethod
    def editar_datos(self, nombre: str, apellidos: str, rfc: str) -> bool:
        pass

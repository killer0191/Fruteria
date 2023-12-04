from abc import ABC, abstractmethod
from typing import List

class IProducto(ABC):
    @abstractmethod
    def insertar(self, nombre: str, cantidad: int, precio: float, idProveedor: int) -> bool:
        pass

    @abstractmethod
    def obtener_todo(self) -> List[dict]:
        pass

    @abstractmethod
    def obtener(self, id: int) -> List[dict]:
        pass

    @abstractmethod
    def editar_datos(self, nombre: str, cantidad: int, precio: float, idProveedor: int) -> bool:
        pass
    
    @abstractmethod
    def borrar(self, id: int) -> bool:
        pass

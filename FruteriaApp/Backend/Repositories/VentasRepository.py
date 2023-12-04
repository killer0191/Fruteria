from Backend.Repositories.ClienteRepository import ClienteRepository
from Backend.Repositories.ProductoRepository import ProductoRepository
from Backend.conexion import Conexion

class VentasRepository:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cliente_repository = ClienteRepository(conexion)
        self.producto_repository = ProductoRepository(conexion)

    def obtener_clientes(self):
        return self.cliente_repository.obtener_todo()

    def obtener_productos(self):
        return self.producto_repository.obtener_todo()

    def ingresar_venta(self, codigo_cliente:int, codigo_producto:int, cantidad: int, fecha)-> bool:
        cliente_existe = self.cliente_repository.existe_cliente(codigo_cliente)
        print("el id cliente: ",codigo_cliente, "resultado", cliente_existe)
        producto_existe = self.producto_repository.existe_producto(codigo_producto)
        print("el id producto: ",codigo_producto, "resultado",producto_existe)

        if cliente_existe and producto_existe:
            precio_producto = self.producto_repository.obtener_precio_producto(codigo_producto)

            # Calcular el total
            total = precio_producto * int(cantidad)

            venta_data = {
                "IdCliente": codigo_cliente,
                "IdProducto": codigo_producto,
                "Cantidad": cantidad,
                "Fecha": fecha,
                "Total": total
            }

            self.conexion.insert("Ventas", venta_data)
            print("Venta ingresada exitosamente.")
            return True
        else:
            print("Error: Cliente o producto no existe.")
            return False

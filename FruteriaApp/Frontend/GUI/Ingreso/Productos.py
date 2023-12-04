import tkinter as tk
from tkinter import ttk, messagebox
from Backend.Repositories.ProductoRepository import ProductoRepository
from Backend.Repositories.ProveedorRepository import ProveedorRepository
from Backend.conexion import Conexion
from Frontend.GUI.inventario import Inventario

class Productos:
    def __init__(self, root):
        self.root = root
        self.root.title("Productos")
        self.root.resizable(False, False)  # No permitir redimensionar

        # Aplicar paleta de colores
        self.root.tk_setPalette(background="#f1f6f8")

        # Centrar la ventana
        self.center_window(500, 300)

        conexion = Conexion()

        # Crea una instancia de ProductoRepository y ProveedorRepository
        self.producto_repository = ProductoRepository(conexion)
        self.proveedor_repository = ProveedorRepository(conexion)

        # Barra de menú
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Menú de Proveedor
        self.menu_proveedor = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Inventario", menu=self.menu_proveedor)
        self.menu_proveedor.add_command(label="Ir a inventario", command=self.ir_a_inventario)

        # Menú de Ingresar
        self.menu_ingresar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ingresar", menu=self.menu_ingresar)
        self.menu_ingresar.add_command(label="Ingresar Venta", command=self.ingresar_venta)
        self.menu_ingresar.add_command(label="Ingresar Cliente", command=self.ingresar_cliente)
        self.menu_ingresar.add_command(label="Ingresar Proveedor", command=self.ingresar_proveedor)

        # Menú de Edición
        self.menu_edicion = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.menu_edicion)
        self.menu_edicion.add_command(label="Editar Producto", command=self.editar)

        # Menú de Sesión
        self.menu_sesion = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Sesión", menu=self.menu_sesion)
        self.menu_sesion.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)

        # Campos de formulario para productos
        self.label_nombre = tk.Label(root, text="Nombre:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_nombre.grid(row=1, column=0, padx=50, pady=15, sticky="w")

        self.entry_nombre = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=15, sticky="w")

        self.label_cantidad = tk.Label(root, text="Cantidad:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_cantidad.grid(row=2, column=0, padx=50, pady=15, sticky="w")

        self.entry_cantidad = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=15, sticky="w")

        # Obtener la lista de proveedores desde la base de datos
        proveedores = self.proveedor_repository.obtener_proveedores()

        self.label_proveedor = tk.Label(root, text="Proveedor:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_proveedor.grid(row=3, column=0, padx=50, pady=15, sticky="w")

        self.combo_proveedor = ttk.Combobox(root, values=[f"{proveedor[0]} - {proveedor[1]}" for proveedor in proveedores], font=("Helvetica", 12))
        self.combo_proveedor.grid(row=3, column=1, padx=10, pady=15, sticky="w")

        self.label_precio = tk.Label(root, text="Precio:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_precio.grid(row=4, column=0, padx=50, pady=15, sticky="w")

        self.entry_precio = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_precio.grid(row=4, column=1, padx=10, pady=15, sticky="w")

        # Botón para ingresar el producto
        btn_ingresar_producto = tk.Button(root, text="Ingresar producto", command=self.ingresar_producto, bg="#ff7c00", fg="white", font=("Helvetica", 12, "bold"))
        btn_ingresar_producto.grid(row=5, column=0, columnspan=2, pady=20, sticky="s", padx=130, ipadx=50, ipady=7)

        # Agregar espacio para centrar el formulario
        self.root.grid_rowconfigure(6, weight=1)
        
    def ir_a_inventario(self):
        self.root.withdraw()
        inventario_root = tk.Tk()
        inventario_app = Inventario(inventario_root)
        inventario_root.mainloop()

    def cerrar_sesion(self):
        # Ocultar la ventana actual
        self.root.withdraw()
        
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def ingresar_producto(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()
        codigo_proveedor = self.combo_proveedor.get().split(" - ")[0]
        precio = self.entry_precio.get()

        # Verificar que todos los campos estén completos
        if not nombre or not cantidad or not codigo_proveedor or not precio:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Advertencia", "Cantidad y Precio deben ser valores numéricos.")
            return

        # Verificar que la cantidad y el precio sean valores positivos
        if cantidad <= 0 or precio <= 0:
            messagebox.showwarning("Advertencia", "Cantidad y Precio deben ser valores positivos.")
            return

        if self.producto_repository.insertar(nombre, cantidad, precio, codigo_proveedor):
            messagebox.showinfo("Éxito", "El producto se ha ingresado correctamente.")
            self.entry_nombre.delete(0, 'end')
            self.entry_cantidad.delete(0, 'end')
            self.combo_proveedor.set('')
            self.entry_precio.delete(0, 'end')
        else:
            messagebox.showinfo("Error", "El producto no se ha ingresado.")

    def ingresar_venta(self):
          from Frontend.GUI.Ingreso.Ventas import Ventas
          self.root.withdraw()
          ventas_root = tk.Tk()
          ventas_app = Ventas(ventas_root)
          ventas_root.mainloop()

    def ingresar_cliente(self):
          # Redirigir a la ventana de clientes
          from Frontend.GUI.Ingreso.Clientes import Clientes
          self.root.withdraw()
          clientes_root = tk.Tk()
          clientes_app = Clientes(clientes_root)
          clientes_root.mainloop()

    def ingresar_proveedor(self):
          from Frontend.GUI.Ingreso.Proveedor import Proveedores
          self.root.withdraw()
          proveedores_root = tk.Tk()
          proveedores_app = Proveedores(proveedores_root)
          proveedores_root.mainloop()
    
    def editar(self):
          from Frontend.GUI.Edicion.EProducto import EProductos
          self.root.withdraw()
          editar = tk.Tk()
          editar_app = EProductos(editar)
          editar.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    conexion = Conexion()
    productos_app = Productos(root)
    root.mainloop()

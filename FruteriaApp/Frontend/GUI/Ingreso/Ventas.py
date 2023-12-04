import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Backend.Repositories.VentasRepository import VentasRepository
from Frontend.GUI.inventario import Inventario
from Backend.conexion import Conexion

class Ventas:
    def __init__(self, root):
      self.root = root
      self.root.title("Ventas")
      self.root.resizable(False, False)  # No permitir redimensionar

      # Aplicar paleta de colores
      self.root.tk_setPalette(background="#f1f6f8")

      # Centrar la ventana
      self.center_window(500, 300)

      # Crea una instancia de Conexion
      conexion = Conexion()

      # Crea una instancia de VentasRepository pasando la instancia de Conexion
      self.ventas_repository = VentasRepository(conexion)

      # Barra de menú
      self.menu_bar = tk.Menu(root, bg="#29323c", fg="white", activebackground="#29323c")
      root.config(menu=self.menu_bar)

      # Menú de Inventario
      self.menu_inventario = tk.Menu(self.menu_bar, tearoff=0, bg="#29323c", fg="white", activebackground="#29323c")
      self.menu_bar.add_cascade(label="Inventario", menu=self.menu_inventario)
      self.menu_inventario.add_command(label="Ir a Inventario", command=self.ir_a_inventario)

      # Menú de Ingresar
      self.menu_ingresar = tk.Menu(self.menu_bar, tearoff=0, bg="#29323c", fg="white", activebackground="#29323c")
      self.menu_bar.add_cascade(label="Ingresar", menu=self.menu_ingresar)
      self.menu_ingresar.add_command(label="Ingresar Producto", command=self.ingresar_producto)
      self.menu_ingresar.add_command(label="Ingresar Cliente", command=self.ingresar_cliente)
      self.menu_ingresar.add_command(label="Ingresar Proveedor", command=self.ingresar_proveedor)

      # Menú de Sesión
      self.menu_sesion = tk.Menu(self.menu_bar, tearoff=0, bg="#29323c", fg="white", activebackground="#29323c")
      self.menu_bar.add_cascade(label="Sesión", menu=self.menu_sesion)
      self.menu_sesion.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)

      # Campos de formulario para ventas
      self.label_fecha = tk.Label(root, text="Fecha:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
      self.label_fecha.grid(row=1, column=0, padx=50, pady=15, sticky="w")

      # Obtener la fecha actual en horario de la Ciudad de México
      self.fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      self.label_fecha_valor = tk.Label(root, text=self.fecha_actual, bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12, "italic"))
      self.label_fecha_valor.grid(row=1, column=1, padx=10, pady=15, sticky="w")

      self.label_cliente = tk.Label(root, text="Código del Cliente:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
      self.label_cliente.grid(row=2, column=0, padx=50, pady=15, sticky="w")

      # Obtener la lista de clientes desde la base de datos
      clientes = self.ventas_repository.obtener_clientes()

      # Usar índices enteros en lugar de claves de cadena
      self.combo_cliente = ttk.Combobox(
          root, values=[f"{cliente[0]} - {cliente[1]}" for cliente in clientes], background="#ffffff", foreground="#29323c", font=("Helvetica", 12)
      )

      self.combo_cliente.grid(row=2, column=1, padx=10, pady=15, sticky="w")

      self.label_producto = tk.Label(root, text="Producto:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
      self.label_producto.grid(row=3, column=0, padx=50, pady=15, sticky="w")

      # Obtener la lista de productos desde la base de datos
      productos = self.ventas_repository.obtener_productos()

      self.combo_producto = ttk.Combobox(
          root, values=[f"{producto[0]} - {producto[1]}" for producto in productos], background="#ffffff", foreground="#29323c", font=("Helvetica", 12)
      )
      self.combo_producto.grid(row=3, column=1, padx=10, pady=15, sticky="w")

      self.label_cantidad = tk.Label(root, text="Cantidad:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
      self.label_cantidad.grid(row=4, column=0, padx=50, pady=15, sticky="w")

      self.entry_cantidad = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
      self.entry_cantidad.grid(row=4, column=1, padx=10, pady=15, sticky="w")

      # Botón para ingresar la venta
      btn_ingresar_venta = tk.Button(root, text="Ingresar Venta", command=self.ingresar_venta, bg="#ff7c00", fg="white", font=("Helvetica", 12, "bold"))
      btn_ingresar_venta.grid(row=5, column=0, columnspan=2, pady=20, sticky="s", padx=130, ipadx=50, ipady=7)

      # Agregar espacio para centrar el formulario
      self.root.grid_rowconfigure(6, weight=1)

    def ir_a_inventario(self):
        # Redirigir a la ventana de inventario
        self.root.withdraw()
        inventario_root = tk.Tk()
        inventario_app = Inventario(inventario_root)
        inventario_root.mainloop()

    def ingresar_producto(self):
        from Frontend.GUI.Ingreso.Productos import Productos
        self.root.withdraw()
        productos_root = tk.Tk()
        productos_app = Productos(productos_root)
        productos_root.mainloop()

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

    def cerrar_sesion(self):
        # Ocultar la ventana actual
        self.root.withdraw()
        
    def ingresar_venta(self):
      fecha = self.fecha_actual
      codigo_cliente = self.combo_cliente.get().split(" - ")[0]
      codigo_producto = self.combo_producto.get().split(" - ")[0]
      cantidad = self.entry_cantidad.get()

      # Verificar que todos los campos estén llenos
      if not codigo_cliente or not codigo_producto or not cantidad:
          messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
          return

      # Intentar ingresar la venta
      if self.ventas_repository.ingresar_venta(codigo_cliente, codigo_producto, cantidad, fecha):
          messagebox.showinfo("Éxito", "La venta se ha ingresado correctamente.")
          self.combo_cliente.set('')
          self.combo_producto.set('')
          self.entry_cantidad.delete(0, 'end')
      else:
          messagebox.showinfo("Error", "La venta no ha sido ingresada.")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    conexion = Conexion()
    ventas_repository = VentasRepository(conexion)
    app = Ventas(root)
    root.mainloop()

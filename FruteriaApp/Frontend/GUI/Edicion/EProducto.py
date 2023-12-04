import tkinter as tk
from tkinter import ttk, messagebox
from Backend.Repositories.ProductoRepository import ProductoRepository
from Backend.Repositories.ProveedorRepository import ProveedorRepository
from Backend.conexion import Conexion
from Frontend.GUI.inventario import Inventario

class EProductos:
    def __init__(self, root):
        self.root = root
        self.root.title("Editar Producto")
        self.center_window(500, 350)
        conexion = Conexion()

        # Crea una instancia de ProductoRepository y ProveedorRepository
        self.producto_repository = ProductoRepository(conexion)
        self.proveedor_repository = ProveedorRepository(conexion)

        # Barra de menú
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Menú de Ingresar
        self.menu_ingresar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ingresar", menu=self.menu_ingresar)
        self.menu_ingresar.add_command(label="Ingresar Producto", command=self.ingresar_producto)

        # Combo box para seleccionar el producto
        self.label_seleccionar_producto = tk.Label(root, text="Seleccionar Producto:", fg="#29323c", font=("Helvetica", 12))
        self.label_seleccionar_producto.grid(row=0, column=0, padx=50, pady=15, sticky="w")

        # Obtener la lista de productos desde la base de datos
        productos = self.producto_repository.obtener_todo()
        print(productos)

        self.combo_productos = ttk.Combobox(root, values=[f"{producto[0]} - {producto[1]}" for producto in productos], font=("Helvetica", 12))
        self.combo_productos.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        self.combo_productos.bind("<<ComboboxSelected>>", self.cargar_datos_producto)

        # Campos de formulario para productos
        self.label_nombre = tk.Label(root, text="Nombre:", fg="#29323c", font=("Helvetica", 12))
        self.label_nombre.grid(row=1, column=0, padx=50, pady=15, sticky="w")

        self.entry_nombre = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=15, sticky="w")

        self.label_cantidad = tk.Label(root, text="Cantidad:", fg="#29323c", font=("Helvetica", 12))
        self.label_cantidad.grid(row=2, column=0, padx=50, pady=15, sticky="w")

        self.entry_cantidad = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=15, sticky="w")

        # Obtener la lista de proveedores desde la base de datos
        proveedores = self.proveedor_repository.obtener_proveedores()

        self.label_proveedor = tk.Label(root, text="Proveedor:", fg="#29323c", font=("Helvetica", 12))
        self.label_proveedor.grid(row=3, column=0, padx=50, pady=15, sticky="w")

        self.combo_proveedor = ttk.Combobox(root, values=[f"{proveedor[0]} - {proveedor[1]}" for proveedor in proveedores], font=("Helvetica", 12))
        self.combo_proveedor.grid(row=3, column=1, padx=10, pady=15, sticky="w")

        self.label_precio = tk.Label(root, text="Precio:", fg="#29323c", font=("Helvetica", 12))
        self.label_precio.grid(row=4, column=0, padx=50, pady=15, sticky="w")

        self.entry_precio = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_precio.grid(row=4, column=1, padx=10, pady=15, sticky="w")

        # Botón para editar el producto
        btn_editar_producto = tk.Button(root, text="Editar producto", command=self.editar_producto, bg="#ff7c00", fg="white", font=("Helvetica", 12, "bold"))
        btn_editar_producto.grid(row=5, column=0, columnspan=2, pady=20, sticky="s", padx=130, ipadx=50, ipady=7)
        
        # Agregar espacio para centrar el formulario
        self.root.grid_rowconfigure(6, weight=1)

    def cargar_datos_producto(self, event):
        # Obtener el ID del producto seleccionado
        selected_producto = self.combo_productos.get().split(" - ")[0]

        # Obtener los datos del producto seleccionado
        producto_datos = self.producto_repository.obtener(int(selected_producto))

        # Rellenar los campos con los datos del producto
        self.entry_nombre.delete(0, 'end')
        self.entry_nombre.insert(0, producto_datos[0][1])

        self.entry_cantidad.delete(0, 'end')
        self.entry_cantidad.insert(0, producto_datos[0][2])

        self.combo_proveedor.set(producto_datos[0][4])

        self.entry_precio.delete(0, 'end')
        self.entry_precio.insert(0, producto_datos[0][3])

    def ingresar_producto(self):
        from Frontend.GUI.Ingreso.Productos import Productos
        self.root.withdraw()
        productos_root = tk.Tk()
        productos_app = Productos(productos_root)
        productos_root.mainloop()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def editar_producto(self):
      # Obtener la selección actual del combo de productos
      seleccion_producto = self.combo_productos.get()

      # Verificar que se ha seleccionado un producto
      if not seleccion_producto:
          messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para editar.")
          return

      # Extraer el ID del producto de la selección
      idProducto = seleccion_producto.split(" - ")[0]
      
      nombre = self.entry_nombre.get()
      cantidad = self.entry_cantidad.get()
      precio = self.entry_precio.get()
      idProveedor = self.combo_proveedor.get().split(" - ")[0]

      # Verificar que todos los campos estén completos
      if not nombre or not cantidad or not idProveedor or not precio:
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

      if self.producto_repository.editar_datos(idProducto, nombre, cantidad, precio, idProveedor):
          messagebox.showinfo("Éxito", "El producto se ha editado correctamente.")
          # Limpiar campos después de la edición
          self.entry_nombre.delete(0, 'end')
          self.entry_cantidad.delete(0, 'end')
          self.combo_proveedor.set('')
          self.entry_precio.delete(0, 'end')
      else:
          messagebox.showinfo("Error", "El producto no ha sido editado.")

if __name__ == "__main__":
    root = tk.Tk()
    conexion = Conexion()
    eproductos_app = EProductos(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
from Backend.Repositories.ClienteRepository import ClienteRepository
from Frontend.GUI.inventario import Inventario
from Backend.conexion import Conexion

class Clientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Clientes")
        self.root.resizable(False, False)  # No permitir redimensionar

        # Aplicar paleta de colores
        self.root.tk_setPalette(background="#f1f6f8")
        self.center_window(500, 300)

        # Crea una instancia de Conexion
        conexion = Conexion()

        # Crea una instancia de ClienteRepository pasando la instancia de Conexion
        self.cliente_repository = ClienteRepository(conexion)

        # Barra de menú
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Menú de Inventario
        self.menu_inventario = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Inventario", menu=self.menu_inventario)
        self.menu_inventario.add_command(label="Ir a Inventario", command=self.ir_a_inventario)

        # Menú de Ingresar
        self.menu_ingresar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ingresar", menu=self.menu_ingresar)
        self.menu_ingresar.add_command(label="Ingresar Venta", command=self.ingresar_venta)
        self.menu_ingresar.add_command(label="Ingresar Producto", command=self.ingresar_producto)
        self.menu_ingresar.add_command(label="Ingresar Proveedor", command=self.ingresar_proveedor)
        
        # Menú de Edición
        self.menu_edicion = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.menu_edicion)
        self.menu_edicion.add_command(label="Editar Cliente", command=self.editar)

        # Menú de Sesión
        self.menu_sesion = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Sesión", menu=self.menu_sesion)
        self.menu_sesion.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)

        # Campos de formulario para clientes
        self.label_nombre = tk.Label(root, text="Nombre:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_nombre.grid(row=1, column=0, padx=50, pady=15, sticky="w")

        self.entry_nombre = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=15, sticky="w")

        self.label_apellidos = tk.Label(root, text="Apellidos:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_apellidos.grid(row=2, column=0, padx=50, pady=15, sticky="w")

        self.entry_apellidos = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_apellidos.grid(row=2, column=1, padx=10, pady=15, sticky="w")

        # Obtener la lista de empresas desde la base de datos
        empresas = self.cliente_repository.obtener_empresas()
        print("Las empresas son: ", empresas)

        self.label_empresa = tk.Label(root, text="Empresa:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_empresa.grid(row=3, column=0, padx=50, pady=15, sticky="w")

        self.combo_empresa = ttk.Combobox(
            root, values=[f"{empresa[0]} - {empresa[1]}" for empresa in empresas],
            background="#ffffff", foreground="#29323c", font=("Helvetica", 12)
        )
        self.combo_empresa.grid(row=3, column=1, padx=10, pady=15, sticky="w")

        self.label_rfc = tk.Label(root, text="RFC:", bg="#f1f6f8", fg="#29323c", font=("Helvetica", 12))
        self.label_rfc.grid(row=4, column=0, padx=50, pady=15, sticky="w")

        self.entry_rfc = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_rfc.grid(row=4, column=1, padx=10, pady=15, sticky="w")

        # Botón para ingresar el cliente
        btn_ingresar_cliente = tk.Button(
            root, text="Ingresar Cliente", command=self.ingresar_cliente,
            bg="#ff7c00", fg="white", font=("Helvetica", 12, "bold")
        )
        btn_ingresar_cliente.grid(row=5, column=0, columnspan=2, pady=20, sticky="s", padx=130, ipadx=50, ipady=7)
        
        self.root.grid_rowconfigure(6, weight=1)

    def ir_a_inventario(self):
        # Redirigir a la ventana de inventario
        self.root.withdraw()
        inventario_root = tk.Tk()
        inventario_app = Inventario(inventario_root)
        inventario_root.mainloop()

    def ingresar_venta(self):
          from Frontend.GUI.Ingreso.Ventas import Ventas
          self.root.withdraw()
          ventas_root = tk.Tk()
          ventas_app = Ventas(ventas_root)
          ventas_root.mainloop()

    def ingresar_producto(self):
          from Frontend.GUI.Ingreso.Productos import Productos
          self.root.withdraw()
          productos_root = tk.Tk()
          productos_app = Productos(productos_root)
          productos_root.mainloop()

    def ingresar_proveedor(self):
          from Frontend.GUI.Ingreso.Proveedor import Proveedores
          self.root.withdraw()
          proveedores_root = tk.Tk()
          proveedores_app = Proveedores(proveedores_root)
          proveedores_root.mainloop()

    def cerrar_sesion(self):
        # Ocultar la ventana actual
        self.root.withdraw()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def ingresar_cliente(self):
        # Obtener valores de los campos
        nombre = self.entry_nombre.get()
        apellidos = self.entry_apellidos.get()
        id_empresa = self.combo_empresa.get().split(" - ")[0]
        rfc = self.entry_rfc.get()

        # Validar que los campos no estén vacíos
        if not nombre or not apellidos or not id_empresa or not rfc:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Ingresar el cliente utilizando el repositorio
        if self.cliente_repository.insertar(nombre, apellidos, rfc, int(id_empresa)):
            messagebox.showinfo("Éxito", "El cliente se ha ingresado correctamente.")
            # Limpiar campos después de la inserción
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellidos.delete(0, tk.END)
            self.combo_empresa.set('')
            self.entry_rfc.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Error al ingresar el cliente. Por favor, revise los datos e inténtelo nuevamente.")

    def editar(self):
              from Frontend.GUI.Edicion.EClientes import EClientes
              self.root.withdraw()
              editar = tk.Tk()
              editar_app = EClientes(editar)
              editar.mainloop()
              
if __name__ == "__main__":
    root = tk.Tk()
    app = Clientes(root)
    root.mainloop()

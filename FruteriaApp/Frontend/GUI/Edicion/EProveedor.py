import tkinter as tk
from tkinter import ttk, messagebox
from Backend.Repositories.ProveedorRepository import ProveedorRepository
from Backend.Repositories.ClienteRepository import ClienteRepository
from Backend.conexion import Conexion

class EProveedores:
    def __init__(self, root):
        self.root = root
        self.root.title("Editar Proveedor")
        conexion = Conexion()
        self.idPerson=0
        self.center_window(500,350)

        # Crea una instancia de ProveedorRepository y ClienteRepository
        self.proveedor_repository = ProveedorRepository(conexion)
        self.cliente_repository = ClienteRepository(conexion)

        # Barra de menú
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Menú de Ingresar
        self.menu_ingresar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ingresar", menu=self.menu_ingresar)
        self.menu_ingresar.add_command(label="Ingresar Proveedor", command=self.ingresar_proveedor)

        # Combo box para seleccionar el proveedor
        self.label_seleccionar_proveedor = tk.Label(root, text="Seleccionar Proveedor:",fg="#29323c", font=("Helvetica", 12))
        self.label_seleccionar_proveedor.grid(row=0, column=0, padx=50, pady=15, sticky="w")

        # Obtener la lista de proveedores desde la base de datos
        proveedores = self.proveedor_repository.obtener_proveedores()

        self.combo_proveedores = ttk.Combobox(root, values=[f"{proveedor[0]} - {proveedor[1]}" for proveedor in proveedores], background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.combo_proveedores.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        self.combo_proveedores.bind("<<ComboboxSelected>>", self.cargar_datos_proveedor)

        # Campos de formulario para proveedores
        self.label_nombre = tk.Label(root, text="Nombre:",fg="#29323c", font=("Helvetica", 12))
        self.label_nombre.grid(row=1, column=0, padx=50, pady=15, sticky="w")

        self.entry_nombre = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_apellidos = tk.Label(root, text="Apellidos:", fg="#29323c", font=("Helvetica", 12))
        self.label_apellidos.grid(row=2, column=0, padx=50, pady=15, sticky="w")

        self.entry_apellidos = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_apellidos.grid(row=2, column=1, padx=10, pady=15, sticky="w")

        # Obtener la lista de empresas desde la base de datos
        empresas = self.cliente_repository.obtener_empresas()
        print("Las empresas son: ", empresas)

        self.label_empresa = tk.Label(root, text="Empresa:", fg="#29323c", font=("Helvetica", 12))
        self.label_empresa.grid(row=3, column=0, padx=50, pady=15, sticky="w")

        self.combo_empresa = ttk.Combobox(root, values=[f"{empresa[0]} - {empresa[1]}" for empresa in empresas], background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.combo_empresa.grid(row=3, column=1, padx=10, pady=15, sticky="w")

        self.label_rfc = tk.Label(root, text="RFC:", fg="#29323c", font=("Helvetica", 12))
        self.label_rfc.grid(row=4, column=0, padx=50, pady=15, sticky="w")

        self.entry_rfc = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_rfc.grid(row=4, column=1, padx=10, pady=15, sticky="w")

        # Botón para editar el proveedor
        btn_editar_proveedor = tk.Button(root, text="Editar proveedor", command=self.editar_proveedor , bg="#ff7c00", fg="white", font=("Helvetica", 12, "bold"))
        btn_editar_proveedor.grid(row=5, column=0, columnspan=2, pady=20, sticky="s", padx=130, ipadx=50, ipady=7)

    def cargar_datos_proveedor(self, event):
        # Obtener el ID del proveedor seleccionado
        selected_proveedor = self.combo_proveedores.get().split(" - ")[0]
        
        # Obtener los datos del proveedor seleccionado
        proveedor_datos = self.proveedor_repository.obtener(int(selected_proveedor))
        
        self.idPerson = self.proveedor_repository.obtener_id_persona(proveedor_datos[0][4], proveedor_datos[0][5], proveedor_datos[0][6])

        # Rellenar los campos con los datos del proveedor
        self.entry_nombre.delete(0, 'end')
        self.entry_nombre.insert(0, proveedor_datos[0][4])

        self.entry_apellidos.delete(0, 'end')
        self.entry_apellidos.insert(0, proveedor_datos[0][5])

        self.combo_empresa.set(proveedor_datos[0][7])

        self.entry_rfc.delete(0, 'end')
        self.entry_rfc.insert(0, proveedor_datos[0][6])

    def ingresar_proveedor(self):
        from Frontend.GUI.Ingreso.Proveedor import Proveedores
        self.root.withdraw()
        proveedores_root = tk.Tk()
        proveedores_app = Proveedores(proveedores_root)
        proveedores_root.mainloop()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def editar_proveedor(self):
      # Obtener la selección actual del combo_proveedores
      seleccion_proveedor = self.combo_proveedores.get()

      # Verificar que se haya seleccionado un proveedor
      if not seleccion_proveedor:
          messagebox.showwarning("Advertencia", "Por favor, selecciona un proveedor para editar.")
          return

      # Obtener los datos necesarios para la edición
      idProveedor = seleccion_proveedor.split(" - ")[0]
      nombre = self.entry_nombre.get()
      apellidos = self.entry_apellidos.get()
      idEmpresa = self.combo_empresa.get().split(" - ")[0]
      rfc = self.entry_rfc.get()  

      # Realizar la edición
      if self.proveedor_repository.editar_datos(idProveedor, nombre, apellidos, rfc, idEmpresa, self.idPerson):
          messagebox.showinfo("Éxito", "El proveedor se ha editado correctamente.")
          # Limpiar campos después de la edición
          self.entry_nombre.delete(0, 'end')
          self.entry_apellidos.delete(0, 'end')
          self.combo_empresa.set('')
          self.entry_rfc.delete(0, 'end')
      else:
          messagebox.showinfo("Error", "El proveedor no ha sido editado.")

          idProveedor = self.combo_proveedores.get().split(" - ")[0]
          nombre = self.entry_nombre.get()
          apellidos = self.entry_apellidos.get()
          idEmpresa = self.combo_empresa.get().split(" - ")[0]
          rfc = self.entry_rfc.get()  

          if self.proveedor_repository.editar_datos(idProveedor, nombre, apellidos, rfc, idEmpresa, self.idPerson):
              messagebox.showinfo("Éxito", "El proveedor se ha editado correctamente.")
              # Limpiar campos después de la edición
              self.entry_nombre.delete(0, 'end')
              self.entry_apellidos.delete(0, 'end')
              self.combo_empresa.set('')
              self.entry_rfc.delete(0, 'end')
          else:
              messagebox.showinfo("Error", "El proveedor no ha sido editado.")

if __name__ == "__main__":
    root = tk.Tk()
    conexion = Conexion()
    eproveedor_app = EProveedores(root)
    root.mainloop()

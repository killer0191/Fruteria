import tkinter as tk
from tkinter import ttk, messagebox
from Backend.Repositories.ClienteRepository import ClienteRepository
from Backend.Repositories.ProveedorRepository import ProveedorRepository
from Frontend.GUI.inventario import Inventario
from Backend.conexion import Conexion

class EClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Editar Cliente")
        self.center_window(500, 350)
        conexion = Conexion()
        self.idPerson = 0

        # Crea una instancia de ClienteRepository y ProveedorRepository
        self.cliente_repository = ClienteRepository(conexion)
        self.proveedor_repository = ProveedorRepository(conexion)

        # Barra de menú
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Menú de Ingresar
        self.menu_ingresar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ingresar", menu=self.menu_ingresar)
        self.menu_ingresar.add_command(label="Ingresar Cliente", command=self.ingresar_cliente)

        # Combo box para seleccionar el cliente
        self.label_seleccionar_cliente = tk.Label(root, text="Seleccionar Cliente:", fg="#29323c", font=("Helvetica", 12))
        self.label_seleccionar_cliente.grid(row=0, column=0, padx=50, pady=15, sticky="w")

        # Obtener la lista de clientes desde la base de datos
        clientes = self.cliente_repository.obtener_clientes()
        print(clientes)

        self.combo_clientes = ttk.Combobox(root, values=[f"{cliente[0]} - {cliente[4]}" for cliente in clientes], background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.combo_clientes.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.combo_clientes.bind("<<ComboboxSelected>>", self.cargar_datos_cliente)

        # Campos de formulario para clientes
        self.label_nombre = tk.Label(root, text="Nombre:", fg="#29323c", font=("Helvetica", 12))
        self.label_nombre.grid(row=1, column=0, padx=50, pady=15, sticky="w")

        self.entry_nombre = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_apellidos = tk.Label(root, text="Apellidos:", fg="#29323c", font=("Helvetica", 12))
        self.label_apellidos.grid(row=2, column=0, padx=50, pady=15, sticky="w")

        self.entry_apellidos = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_apellidos.grid(row=2, column=1, padx=10, pady=15, sticky="w")

        # Obtener la lista de empresas desde la base de datos
        empresas = self.proveedor_repository.obtener_empresas()
        print("Las empresas son: ", empresas)

        self.label_empresa = tk.Label(root, text="Empresa:", fg="#29323c", font=("Helvetica", 12))
        self.label_empresa.grid(row=3, column=0, padx=50, pady=15, sticky="w")

        self.combo_empresa = ttk.Combobox(root, values=[f"{empresa[0]} - {empresa[1]}" for empresa in empresas], background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.combo_empresa.grid(row=3, column=1, padx=10, pady=15, sticky="w")

        self.label_rfc = tk.Label(root, text="RFC:", fg="#29323c", font=("Helvetica", 12))
        self.label_rfc.grid(row=4, column=0, padx=50, pady=15, sticky="w")

        self.entry_rfc = tk.Entry(root, background="#ffffff", foreground="#29323c", font=("Helvetica", 12))
        self.entry_rfc.grid(row=4, column=1, padx=10, pady=15, sticky="w")

        # Botón para editar el cliente
        btn_editar_cliente = tk.Button(root, text="Editar cliente", command=self.editar_cliente, bg="#ff7c00", fg="white", font=("Helvetica", 12, "bold"))
        btn_editar_cliente.grid(row=5, column=0, columnspan=2, pady=20, sticky="s", padx=130, ipadx=50, ipady=7)
    
    def cargar_datos_cliente(self, event):
        # Obtener el ID del cliente seleccionado
        selected_cliente = self.combo_clientes.get().split(" - ")[0]

        # Obtener los datos del cliente seleccionado
        cliente_datos = self.cliente_repository.obtener(int(selected_cliente))
        print(cliente_datos)
        
        self.idPerson=self.cliente_repository.obtener_id_persona(cliente_datos[0][4],cliente_datos[0][5], cliente_datos[0][6])

        # Rellenar los campos con los datos del cliente
        self.entry_nombre.delete(0, 'end')
        self.entry_nombre.insert(0, cliente_datos[0][4])

        self.entry_apellidos.delete(0, 'end')
        self.entry_apellidos.insert(0, cliente_datos[0][5])

        self.combo_empresa.set(cliente_datos[0][7])

        self.entry_rfc.delete(0, 'end')
        self.entry_rfc.insert(0, cliente_datos[0][6])
        
    def ingresar_cliente(self):
        from Frontend.GUI.Ingreso.Clientes import Clientes
        self.root.withdraw()
        clientes_root = tk.Tk()
        clientes_app = Clientes(clientes_root)
        clientes_root.mainloop()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def editar_cliente(self):
      # Obtener el ID del cliente seleccionado
      seleccion = self.combo_clientes.get().split(" - ")
      
      if len(seleccion) != 2:
          messagebox.showwarning("Advertencia", "Por favor, selecciona un cliente antes de intentar editar.")
          return

      idCliente = seleccion[0]
      nombre = self.entry_nombre.get()
      apellidos = self.entry_apellidos.get()
      
      # Obtener el ID de la empresa seleccionada
      seleccion_empresa = self.combo_empresa.get().split(" - ")
      
      if len(seleccion_empresa) != 2:
          messagebox.showwarning("Advertencia", "Por favor, selecciona una empresa antes de intentar editar.")
          return

      idEmpresa = seleccion_empresa[0]
      rfc = self.entry_rfc.get()

      if self.cliente_repository.editar_datos(idCliente, nombre, apellidos, rfc, idEmpresa, self.idPerson):
          messagebox.showinfo("Éxito", "El cliente se ha editado correctamente.")
          # Limpiar campos después de la edición
          self.entry_nombre.delete(0, 'end')
          self.entry_apellidos.delete(0, 'end')
          self.combo_empresa.set('')
          self.entry_rfc.delete(0, 'end')
      else:
          messagebox.showinfo("Error", "El cliente no ha sido editado.")

          idCliente = self.combo_clientes.get().split(" - ")[0]
          nombre = self.entry_nombre.get()
          apellidos = self.entry_apellidos.get()
          idEmpresa = self.combo_empresa.get().split(" - ")[0]
          rfc = self.entry_rfc.get()

          if self.cliente_repository.editar_datos(idCliente, nombre, apellidos, rfc, idEmpresa, self.idPerson):
              messagebox.showinfo("Éxito", "El cliente se ha editado correctamente.")
              # Limpiar campos después de la edición
              self.entry_nombre.delete(0, 'end')
              self.entry_apellidos.delete(0, 'end')
              self.combo_empresa.set('')
              self.entry_rfc.delete(0, 'end')
          else:
              messagebox.showinfo("Error", "El cliente no ha sido editado.")

if __name__ == "__main__":
    root = tk.Tk()
    conexion = Conexion()
    eclientes_app = EClientes(root)
    root.mainloop()

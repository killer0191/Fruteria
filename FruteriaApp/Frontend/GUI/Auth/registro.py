import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Backend.Repositories.UsuarioRepository import UsuarioRepository
from Backend.conexion import Conexion
from Frontend.GUI import inventario
from Frontend.GUI.Auth.login import Login

class Registro:
    def __init__(self, root, login_screen):
        self.conexion = Conexion()
        self.usuarioRepo = UsuarioRepository(self.conexion)
        self.root = root
        self.login_screen = login_screen
        self.root.title("Registro")
        self.root.geometry("500x800")
        self.root.resizable(False, False)  # No permitir redimensionar

        # Paleta de colores
        COLOR_PRIMARIO = "#29323c"
        COLOR_SECUNDARIO = "#f1f6f8"
        COLOR_ACENTO = "#ff7c00"

        self.root.config(bg=COLOR_PRIMARIO)

        # Estilos
        style = ttk.Style()
        style.configure("TLabel", background=COLOR_PRIMARIO, foreground=COLOR_SECUNDARIO, font=("Helvetica", 14))
        style.configure("TEntry", fieldbackground=COLOR_SECUNDARIO, font=("Helvetica", 14))
        style.configure("TButton", background=COLOR_ACENTO, foreground="black", font=("Arial", 16))

        # Posicionar en el centro de la pantalla
        self.root.eval('tk::PlaceWindow . center')

        # Labels
        self.label_nombre = ttk.Label(root, text="Nombre:")
        self.label_apellidos = ttk.Label(root, text="Apellidos:")
        self.label_rfc = ttk.Label(root, text="RFC:")
        self.label_email = ttk.Label(root, text="Email:")
        self.label_password = ttk.Label(root, text="Contraseña:")

        # Entrys
        self.entry_nombre = ttk.Entry(root)
        self.entry_apellidos = ttk.Entry(root)
        self.entry_rfc = ttk.Entry(root)
        self.entry_email = ttk.Entry(root)
        self.entry_password = ttk.Entry(root, show="*")

        # Pack widgets
        self.label_nombre.pack(pady=15)
        self.entry_nombre.pack(pady=5)
        self.label_apellidos.pack(pady=15)
        self.entry_apellidos.pack(pady=5)
        self.label_rfc.pack(pady=15)
        self.entry_rfc.pack(pady=5)
        self.label_email.pack(pady=15)
        self.entry_email.pack(pady=5)
        self.label_password.pack(pady=15)
        self.entry_password.pack(pady=5)

        self.registro_button = ttk.Button(root, text="Registrar", command=self.registrar)
        self.registro_button.pack(pady=20)

        self.btn_regresar = ttk.Button(root, text="Regresar", command=self.regresar_al_login)
        self.btn_regresar.pack(pady=10)

    def registrar(self):
        nombre = self.entry_nombre.get()
        apellidos = self.entry_apellidos.get()
        rfc = self.entry_rfc.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        if nombre and apellidos and rfc and email and password:
            if self.usuarioRepo.registrar(nombre, apellidos, rfc, email, password):
                messagebox.showinfo("Éxito", "Registro exitoso")
                self.root.destroy()
                self.abrir_ventana_inventario()
            else:
                messagebox.showerror("Error", "Error al registrar")
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

    def abrir_ventana_inventario(self):
        root_inventario = tk.Tk()
        inventario_screen = inventario.Inventario(root_inventario)
        root_inventario.mainloop()

    def regresar_al_login(self):
        self.root.destroy()
        root_login = tk.Tk()
        login_screen = Login(root_login)
        root_login.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = Login(root)
    root.mainloop()

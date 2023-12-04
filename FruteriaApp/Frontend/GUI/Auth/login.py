import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Backend.Repositories.UsuarioRepository import UsuarioRepository
from Backend.conexion import Conexion
from Frontend.GUI import inventario

class Login:
    def __init__(self, root):
        self.conexion = Conexion()
        self.conexion.conectar()

        self.usuarioRepo = UsuarioRepository(self.conexion)
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x300")
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
        self.center_windows(500, 300)

        # Labels
        self.label_username = ttk.Label(root, text="Usuario: ")
        self.label_password = ttk.Label(root, text="Contraseña: ")

        # Entrys
        self.entry_username = ttk.Entry(root, width=35)  # Aumenta el ancho del campo de texto
        self.entry_password = ttk.Entry(root, width=35, show="*")  # Aumenta el ancho del campo de texto

        # Pack widgets
        self.label_username.pack(pady=15)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=15)
        self.entry_password.pack(pady=5)

        self.login_button = ttk.Button(root, text="Iniciar sesión", command=self.login)
        self.login_button.pack(pady=20)

        self.btn_registrar = ttk.Button(root, text="Registrar", command=self.abrir_ventana_registro)
        self.btn_registrar.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.usuarioRepo.iniciar_sesion(username, password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.root.destroy()
            self.abrir_ventana_inventario()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def abrir_ventana_registro(self):
        self.root.destroy()
        root_registro = tk.Tk()
        registro_screen = Registro(root_registro, self)
        root_registro.mainloop()

    def abrir_ventana_inventario(self):
        root_inventario = tk.Tk()
        inventario_screen = inventario.Inventario(root_inventario)
        root_inventario.mainloop()

    def center_windows(self, ancho, alto):
        alturap = self.root.winfo_screenheight()
        anchop = self.root.winfo_screenwidth()

        x = (anchop // 2) - (ancho // 2)
        y = (alturap // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

class Registro:
    def __init__(self, root, login_screen):
        self.conexion = Conexion()
        self.usuarioRepo = UsuarioRepository(self.conexion)
        self.root = root
        self.login_screen = login_screen
        self.root.title("Registro")
        self.root.geometry("500x600")
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
        self.center_windows(500, 600)

        # Labels
        self.label_nombre = ttk.Label(root, text="Nombre:")
        self.label_apellidos = ttk.Label(root, text="Apellidos:")
        self.label_rfc = ttk.Label(root, text="RFC:")
        self.label_email = ttk.Label(root, text="Email:")
        self.label_password = ttk.Label(root, text="Contraseña:")

        # Entrys
        self.entry_nombre = ttk.Entry(root, width=35)  # Aumenta el ancho del campo de texto
        self.entry_apellidos = ttk.Entry(root, width=35)  # Aumenta el ancho del campo de texto
        self.entry_rfc = ttk.Entry(root, width=35)  # Aumenta el ancho del campo de texto
        self.entry_email = ttk.Entry(root, width=35)  # Aumenta el ancho del campo de texto
        self.entry_password = ttk.Entry(root, width=35, show="*")  # Aumenta el ancho del campo de texto

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

    def center_windows(self, ancho, alto):
        alturap = self.root.winfo_screenheight()
        anchop = self.root.winfo_screenwidth()

        x = (anchop // 2) - (ancho // 2)
        y = (alturap // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def regresar_al_login(self):
        self.root.destroy()
        root_login = tk.Tk()
        login_screen = Login(root_login)
        root_login.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = Login(root)
    root.mainloop()

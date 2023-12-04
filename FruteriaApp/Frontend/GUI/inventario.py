import tkinter as tk
from tkinter import ttk, messagebox
from Backend.Repositories.ProductoRepository import ProductoRepository
from Backend.conexion import Conexion
import pandas as pd
from reportlab.pdfgen import canvas

class Inventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario")

        # Aplicar paleta de colores
        self.root.tk_setPalette(background="#f1f6f8")
        
        # Centrar la ventana
        self.center_window(700, 500)

        # Crear la tabla en el medio
        self.tabla_frame = tk.Frame(root, bg="#f1f6f8")
        self.tabla_frame.grid(row=1, column=0, sticky="nsew")

        # Configurar el Treeview con un estilo mejorado
        style = ttk.Style()
        style.theme_use("default")  # Usa el tema predeterminado del sistema

        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), foreground="white", background="#29323c")
        style.configure("Treeview", font=('Helvetica', 10), background="#f1f6f8", foreground="#29323c", fieldbackground="#f1f6f8")
        style.map("Treeview", background=[('selected', '#007acc')])

        self.tabla = ttk.Treeview(
            self.tabla_frame, columns=("ID", "Producto", "Cantidad", "Precio"), show="headings", selectmode="browse", style="Treeview", height=15
        )

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Producto", text="Producto")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Precio", text="Precio")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Producto", anchor="center", minwidth=200, width=327)
        self.tabla.column("Cantidad", anchor="center", minwidth=100, width=150)
        self.tabla.column("Precio", anchor="center", minwidth=100, width=150)

        # Configurar la altura de las filas
        style.configure("Treeview", rowheight=30)  # Ajusta la altura según tus preferencias

        self.tabla.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar el gestor de geometría para expandirse con la ventana
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Conectar con la base de datos y cargar datos en la tabla
        self.conexion = Conexion()
        self.producto_repo = ProductoRepository(self.conexion)
        self.cargar_datos()

        # Mejorar el diseño de la barra de menú
        self.menu_bar = tk.Menu(root, bg="#29323c", fg="white", activebackground="#29323c")
        root.config(menu=self.menu_bar)

        # Menú de Reporte
        self.menu_reporte = tk.Menu(self.menu_bar, tearoff=0, bg="#29323c", fg="white", activebackground="#29323c")
        self.menu_bar.add_cascade(label="Reporte", menu=self.menu_reporte)
        self.menu_reporte.add_command(label="Descargar PDF", command=self.descargar_reporte_pdf)
        self.menu_reporte.add_command(label="Descargar Excel", command=self.descargar_reporte_excel)

        # Menú de Ingresar
        self.menu_ingresar = tk.Menu(self.menu_bar, tearoff=0, bg="#29323c", fg="white", activebackground="#29323c")
        self.menu_bar.add_cascade(label="Ingresar", menu=self.menu_ingresar)
        self.menu_ingresar.add_command(label="Ingresar Venta", command=self.ingresar_venta)
        self.menu_ingresar.add_command(label="Ingresar Producto", command=self.ingresar_producto)
        self.menu_ingresar.add_command(label="Ingresar Cliente", command=self.ingresar_cliente)
        self.menu_ingresar.add_command(label="Ingresar Proveedor", command=self.ingresar_proveedor)

        # Menú de Sesión
        self.menu_sesion = tk.Menu(self.menu_bar, tearoff=0, bg="#29323c", fg="white", activebackground="#29323c")
        self.menu_bar.add_cascade(label="Sesión", menu=self.menu_sesion)
        self.menu_sesion.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)




    def cargar_datos(self):
        # Obtener datos desde la base de datos y cargar en la tabla
        productos = self.producto_repo.obtener_todo()

        for producto in productos:
            # Agregar fila con datos del producto
            self.tabla.insert("", "end", values=(producto[0], producto[1], producto[2], f"${producto[3]}"), tags=("editable",))

        # Configurar etiquetas de estilo para las filas
        self.tabla.tag_configure("editable", background="#ececec")

        # Configurar eventos de clic en las filas
        self.tabla.tag_bind("editable", '<ButtonRelease-1>', self.on_clic)

    def on_clic(self, event):
        item = self.tabla.selection()
        self.confirmar_borrar_producto(item)

    def confirmar_borrar_producto(self, item):
        if item:
            respuesta = messagebox.askyesno("Confirmar", "¿Deseas eliminar este producto?")
            if respuesta:
                self.borrar_producto(item)

    def borrar_producto(self, item):
        # Obtener datos del producto seleccionado
        id_producto = self.tabla.item(item)["values"][0]
        print(f"Borrar producto ID: {id_producto}")
        if self.producto_repo.borrar(id_producto):
            messagebox.showinfo("Éxito", "El producto ha sido borrado correctamente.")
            self.tabla.delete(item)
        else:
            messagebox.showinfo("Error", "El producto no puede borrarse.")
          
    def descargar_reporte_excel(self):
        # Obtener datos desde la tabla
        datos_tabla = [self.tabla.item(item)["values"] for item in self.tabla.get_children()]

        # Crear un DataFrame con los datos
        df = pd.DataFrame(datos_tabla, columns=["ID", "Producto", "Cantidad", "Precio"])

        # Guardar en un archivo Excel
        excel_filename = "reporte_inventario.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"Se ha creado el archivo Excel: {excel_filename}")

        # Mostrar mensaje emergente
        messagebox.showinfo("Éxito", "El reporte Excel se ha descargado correctamente.")

    def descargar_reporte_pdf(self):
        # Obtener datos desde la tabla
        datos_tabla = [self.tabla.item(item)["values"] for item in self.tabla.get_children()]

        # Crear un archivo PDF
        pdf_filename = "reporte_inventario.pdf"
        pdf = canvas.Canvas(pdf_filename)

        # Configurar fuente y tamaño
        pdf.setFont("Helvetica", 10)

        # Escribir encabezados
        encabezados = ["ID", "Producto", "Cantidad", "Precio"]
        for i, encabezado in enumerate(encabezados):
            pdf.drawString(i * 100 + 30, 750, encabezado)

        # Escribir datos de la tabla
        for fila, datos_fila in enumerate(datos_tabla):
            for i, dato in enumerate(datos_fila):
                pdf.drawString(i * 100 + 30, 730 - (fila + 1) * 15, str(dato))

        pdf.save()
        print(f"Se ha creado el archivo PDF: {pdf_filename}")

        # Mostrar mensaje emergente
        messagebox.showinfo("Éxito", "El reporte PDF se ha descargado correctamente.")
    
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
        self.root.withdraw()

    def center_window(self, ancho, alto):
        alturap = self.root.winfo_screenheight()
        anchop = self.root.winfo_screenwidth()

        x = (anchop // 2) - (ancho // 2)
        y = (alturap // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Inventario(root)
    root.mainloop()

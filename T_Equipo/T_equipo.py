import tkinter as tk
from tkinter import messagebox, simpledialog


class Producto:
    def __init__(self, codigo, nombre, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock
        self.siguiente = None

#Estructura del inventario
class Inventario:
    def __init__(self):
        self.head = None

    def agregar_producto(self, codigo, nombre, stock):
        nuevo = Producto(codigo, nombre, stock)
        if codigo == '' or nombre == '':
            return "Se requiere llenar todos los campos."
        ac = self.head
        while ac:
            if codigo == ac.codigo:
                return f"Los codigos deben ser unicos, intente de nuevo"
            ac = ac.siguiente
        if self.head is None:
            self.head = nuevo
        else:
            actual = self.head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        return f"Producto '{nombre}' agregado."

    def buscar_producto(self, clave):
        actual = self.head
        while actual:
            if str(actual.codigo) == str(clave) or actual.nombre.lower() == str(clave).lower():
                return actual
            actual = actual.siguiente
        return None

    def actualizar_stock(self, codigo, nuevo_stock):
        producto = self.buscar_producto(codigo)
        if producto:
            producto.stock = nuevo_stock
            return f"Stock actualizado: {producto.nombre} ahora tiene {producto.stock} unidades."
        return "Producto no encontrado."

    def eliminar_producto(self, codigo):
        actual = self.head
        anterior = None
        while actual:
            if str(actual.codigo) == str(codigo):
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.head = actual.siguiente
                return f"Producto '{actual.nombre}' eliminado."
            anterior = actual
            actual = actual.siguiente
        return "Producto no encontrado."

    def mostrar_stock_bajo(self, limite=5):
        actual = self.head
        bajos = []
        while actual:
            if actual.stock <= limite:
                bajos.append(f"{actual.nombre} (Código: {actual.codigo}, Stock: {actual.stock})")
            actual = actual.siguiente
        return bajos

    def reporte_inventario(self):
        actual = self.head
        reporte = []
        while actual:
            reporte.append(f"Codigo: {actual.codigo} | Nombre: {actual.nombre} | Stock: {actual.stock}")
            actual = actual.siguiente
        return reporte if reporte else ["Inventario vacio."]


#interfaz
class InventarioApp:
    def __init__(self, root):
        self.inv = Inventario()
        self.root = root
        self.root.title("ABARROTES CIMARRON")
        root.geometry("780x650")
        self.root.configure(bg = "#f5f5f5")
        root.iconbitmap("producto.ico")

        tk.Label(root, text = "Inventario abarrotes cimarron", background = "white", font = ("Arial, 16")).pack(pady=10)

        # Marco principal
        frame = tk.Frame(root)
        frame.pack(pady=10)
        frame.configure(bg = "white")
        frame.columnconfigure(1, weight=1)
        frame = tk.Frame(root, bg="#d9d9d9", bd=2, relief="ridge")
        frame.pack(pady=20, padx=20, anchor="w")

        tk.Label(frame, text="Name:", background = "#e0f7fa", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5,sticky="w")
        tk.Label(frame, text="Code:",  background = "#e0f7fa", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Label(frame, text="Stock:",  background = "#e0f7fa", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.codigo_entry = tk.Entry(frame, width=60, font=("Arial", 12))
        self.nombre_entry = tk.Entry(frame, width=60, font=("Arial", 12))
        self.stock_entry = tk.Entry(frame, width=60, font=("Arial", 12))

        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.stock_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Botones de acciones
        tk.Button(frame, text="Agregar", command=self.agregar_producto, font = ("Arial", 12), relief = "groove", width = "6", background = "#4CAF50", fg = "#ffffff").grid(row=0, column=2, padx=5, pady=5)
        tk.Button(frame, text="Buscar", command=self.buscar_producto, font = ("Arial", 12), relief = "groove", width = "8", background = "#2196F3", fg = "#ffffff").grid(row=1, column=2, padx=5, pady=5)
        tk.Button(frame, text="Actualizar", command=self.actualizar_stock, font = ("Arial", 12), relief = "groove", width = "8", background = "#FFC107", fg = "#ffffff").grid(row=2, column=2, padx=5, pady=5)
        tk.Button(frame, text="Eliminar", command=self.eliminar_producto, font = ("Arial", 12), relief = "groove", width = "8", background = "#F44336", fg = "#ffffff").grid(row=3, column=2, padx=5, pady=5)
        tk.Button(frame, text="Stock Bajo", command=self.mostrar_stock_bajo, font = ("Arial", 12), relief = "groove", width = "8", background = "#9C27B0", fg = "#ffffff").grid(row=4, column=2, padx=5, pady=5)
        tk.Button(frame, text="Reporte", command=self.mostrar_reporte, font = ("Arial", 12), relief = "groove", width = "8", background = "#FF9800", fg = "#ffffff").grid(row=5, column=2, padx=5, pady=5)

        # area de resultados
        self.text_area = tk.Text(root, height=12, width=70)
        self.text_area.pack(pady=10)

    def agregar_producto(self):
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        try:
            stock = int(self.stock_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El stock debe ser un numero.")
            return

        msg = self.inv.agregar_producto(codigo, nombre, stock)
        messagebox.showinfo("Éxito", msg)
        self.limpiar_campos()

    def buscar_producto(self):
        clave = simpledialog.askstring("Buscar", "Ingrese codigo o nombre del producto:")
        if clave:
            producto = self.inv.buscar_producto(clave)
            if producto:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, f"Encontrado:\nCódigo: {producto.codigo}\nNombre: {producto.nombre}\nStock: {producto.stock}")
            else:
                messagebox.showwarning("No encontrado", "Producto no encontrado.")

    def actualizar_stock(self):
        codigo = simpledialog.askstring("Actualizar", "Código del producto:")
        if not codigo:
            return
        try:
            nuevo_stock = int(simpledialog.askstring("Actualizar", "Nuevo stock:"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "El stock debe ser un número.")
            return
        msg = self.inv.actualizar_stock(codigo, nuevo_stock)
        messagebox.showinfo("Resultado", msg)

    def eliminar_producto(self):
        codigo = simpledialog.askstring("Eliminar", "Código del producto:")
        if codigo:
            msg = self.inv.eliminar_producto(codigo)
            messagebox.showinfo("Resultado", msg)

    def mostrar_stock_bajo(self):
        limite = simpledialog.askinteger("Stock bajo", "Ingrese el límite:")
        if limite is None:
            return
        productos = self.inv.mostrar_stock_bajo(limite)
        self.text_area.delete("1.0", tk.END)
        if productos:
            self.text_area.insert(tk.END, "Productos con stock bajo:\n\n" + "\n".join(productos))
        else:
            self.text_area.insert(tk.END, "No hay productos con stock bajo.")

    def mostrar_reporte(self):
        reporte = self.inv.reporte_inventario()
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "\n".join(reporte))

    def limpiar_campos(self):
        self.codigo_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)


root = tk.Tk()
app = InventarioApp(root)
root.mainloop()
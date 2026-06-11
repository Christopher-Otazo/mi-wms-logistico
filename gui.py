import customtkinter as ctk
import inventario

class WMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mini WMS - Gestion de Inventario")
        self.geometry("700x500")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.lista_frame = ctk.CTkScrollableFrame(self, label_text="Productos en Bodega")
        self.lista_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.btn_entrada = ctk.CTkButton(self.sidebar, text="Registrar Entrada", command=lambda: self.abrir_ventana_movimiento("Entrada"))
        self.btn_entrada.pack(pady=10)

        self.btn_salida = ctk.CTkButton(self.sidebar, text="Registrar Salida", command=lambda: self.abrir_ventana_movimiento("Salida"))
        self.btn_salida.pack(pady=10)

        self.btn_nuevo = ctk.CTkButton(self.sidebar, text="Nuevo Producto", command=self.abrir_ventana_nuevo)
        self.btn_nuevo.pack(pady=10)

        self.btn_cargar = ctk.CTkButton(self.sidebar, text="Refrescar", command=self.actualizar_lista)
        self.btn_cargar.pack(pady=10)

        self.actualizar_lista()

    def abrir_ventana_nuevo(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Registrar Producto Nuevo")
        ventana.geometry("300x400")

        entry_sku = ctk.CTkEntry(ventana, placeholder_text="SKU")
        entry_sku.pack(pady=5)

        entry_nombre = ctk.CTkEntry(ventana, placeholder_text="Nombre")
        entry_nombre.pack(pady=5)

        entry_stock = ctk.CTkEntry(ventana, placeholder_text="Cantidad")
        entry_stock.pack(pady=5)

        entry_min = ctk.CTkEntry(ventana, placeholder_text="Punto Critico")
        entry_min.pack(pady=5)

        entry_ubicacion = ctk.CTkEntry(ventana, placeholder_text="Ubicacion")
        entry_ubicacion.pack(pady=5)

        btn = ctk.CTkButton(ventana, text="Guardar Producto", command=lambda: self.guardar_nuevo(
            entry_sku.get(), entry_nombre.get(), entry_stock.get(), entry_min.get(), entry_ubicacion.get(), ventana))
        btn.pack(pady=20)

    def guardar_nuevo(self, sku, nombre, stock, min_stock, ubicacion, ventana):
        import sqlite3
        try:
            conn = sqlite3.connect('bodega.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO productos (sku, nombre, cantidad, punto_critico, ubicacion) VALUES (?, ?, ?, ?, ?)', (sku.upper(), nombre, int(stock), int(min_stock), ubicacion.upper()))
            conn.commit()
            conn.close()
            ventana.destroy()
            self.actualizar_lista()
        except Exception as e:
            print(f"Error al guardar: {e}")

    def abrir_ventana_movimiento(self, tipo):
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Registrar {tipo}")
        ventana.geometry("300x250")

        entry_sku = ctk.CTkEntry(ventana, placeholder_text="SKU")
        entry_sku.pack(pady=10)

        entry_cant = ctk.CTkEntry(ventana, placeholder_text="Cantidad")
        entry_cant.pack(pady=10)

        btn_confirmar = ctk.CTkButton(ventana, text="Confirmar", command=lambda: self.procesar(entry_sku.get(), entry_cant.get(), tipo, ventana))
        btn_confirmar.pack(pady=20)

    def procesar(self, sku, cant, tipo, ventana):
        cantidad = int(cant) if tipo == "Entrada" else -int(cant)
        import inventario
        inventario.realizar_movimiento(sku, cantidad)
        ventana.destroy()
        self.actualizar_lista()

    def actualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        productos = inventario.obtener_productos()

        if not productos:
            lbl = ctk.CTkLabel(self.lista_frame, text="No hay productos en Bodega.")
            lbl.pack(pady=20)
            return

        for p in productos:
            sku, nombre, cantidad, punto_critico,  ubicacion = p[0], p[1], p[2], p[3], p[4]
            color_fondo = "#8b0000" if cantidad <= punto_critico else "transparent"
            card = ctk.CTkFrame(self.lista_frame, fg_color=color_fondo)
            card.pack(fill="x", pady=5, padx=5)

            info = ctk.CTkLabel(card, text=f"[{ubicacion}] {sku} | {nombre} | Stock: {cantidad}")
            info.pack(side="left", padx=10)

if __name__ == "__main__":
    app = WMSApp()
    app.mainloop()

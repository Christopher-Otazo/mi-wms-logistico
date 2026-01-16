import sqlite3

def inicializar_db():

    conexion = sqlite3.connect('bodega.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            cantidad INTEGER DEFAULT 0,
            punto_critico INTEGER DEFAULT 5,
            ubicacion TEXT
            )
     ''')
    conexion.commit()
    conexion.close()
def agregar_producto(sku, nombre, cantidad, punto_critico, ubicacion):
    try:
        conn = sqlite3.connect('bodega.db')
        cursor = conn.cursor()
        cursor.execute('''
             INSERT INTO productos (sku, nombre, cantidad, punto_critico, ubicacion)
             VALUES (?, ?, ?, ?, ?)
             ''', (sku, nombre, cantidad, punto_critico, ubicacion))
        conn.commit()
        print(f"Producto {nombre} registrado en rack {ubicacion}.")
    except sqlite3.IntegrityError:
                    print(f"El SKU {sku} ya existe, saltando registro.")
    finally:
         conn.close()

def reporte_stock_critico():
    conn = sqlite3.connect('bodega.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sku, nombre, cantidad, punto_critico FROM productos WHERE cantidad <= punto_critico')
    alertas = cursor.fetchall()

    print("\n--- ALERTAS DE REPOSICION (Logistica SAP)---")
    if not alertas:
        print("Todo en orden. Stock suficiente.")
    for p in alertas:
        print(f"SKU: {p[0]} | {p[1]} - Stock: {p[2]} (Minimo: {p[3]})")
    conn.close()
    
if __name__ == "__main__":
     inicializar_db()
     print("Simulando ingreso de mercaderia...")
     agregar_producto("P&G-001", "Detergente Ace 1L", 20, 10, "A-12")
     agregar_producto("P&G-002", "Shampoo Head & Shoulders", 3, 15, "B-05")
     reporte_stock_critico()

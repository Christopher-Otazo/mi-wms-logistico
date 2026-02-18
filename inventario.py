import sqlite3

def inicializar_db():
    conn = sqlite3.connect('bodega.db')
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

def realizar_movimiento(sku, cantidad_cambio):
    """
    Suma o resta stock.
    cantidad_cambio positiva = Entrada (Recepcion)
    cantidad_cambio negativa = Salida (Despacho/Pickeo)
    """

    conn = sqlite3.connect('bodega.db')
    cursor = conn.cursor()

    #1. Verificar si existe y cuanto hay
    cursor.execute('SELECT cantidad, nombre FROM productos WHERE sku = ?', (sku,))
    resultado = cursor.fetchone()

    if resultado:
        stock_actual = resultado[0]
        nombre = resultado[1]
        nuevo_stock = stock_actual + cantidad_cambio

        if nuevo_stock < 0:
            print(f"ERROR: Stock insuficiente de {nombre}. Disponible: {stock_actual}")
        else:
            cursor.execute('UPDATE productos SET cantidad = ? WHERE sku = ?', (nuevo_stock, sku))
            conn.commit()
            tipo = "Entrada" if cantidad_cambio > 0 else "Salida"
            print(f"{tipo} registrada. {nombre} ahora tiene {nuevo_stock} unidades.")
    else:
        print("Error: SKU no encontrado.")

    conn.close()

def mostrar_menu():
    print("\n--- LOGISTOCK-CLI v2.0 ---")
    print("1. Ver Inventario Completo")
    print("2. Registrar Entrada")
    print("3. Registrar Salida")
    print("4. Ver Alertas de Reposicion")
    print("5. Salir")
    return input("Seleccione una opcion:  ")

def listar_productos():
    conn = sqlite3.connect('bodega.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sku, nombre, cantidad, ubicacion FROM productos')
    for p in cursor.fetchall():
        print(f"[{p[3]}] SKU: {p[0]} | {p[1]} | Stock: {p[2]}")
    conn.close()

if __name__== "__main__":
    inicializar_db()
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            listar_productos()
        elif opcion == "2":
            s = input("SKU: ")
            c = int(input("Cantidad a entrar: "))
            realizar_movimiento(s, c)
        elif opcion == "3":
            s = input("SKU: ")
            c = int(input("Cantidad a despachar: "))
            realizar_movimiento(s, -c) #Se envia negativo para restar
        elif opcion == "4":
            def reporte_stock_critico():
                conn = sqlite3.connect('bodega.db')
                cursor = conn.cursor()
                cursor.execute('SELECT sku, nombre, cantidad, punto_critico FROM productos WHERE cantidad <= punto_critico')
                alertas = cursor.fetchall()
                print("\n--- ALERTA DE REPOSICION (Logica SAP) ---")
                if not alertas:
                    print("Todo en orden. Stock suficiente.")
                for p in alertas:
                    print(f"SKU: {p[0]} | {p[1]} - Stock: {p[2]} (Minimo: {p[3]})")
        elif opcion == "5":
            print("Cerrando Sistema...")
            break

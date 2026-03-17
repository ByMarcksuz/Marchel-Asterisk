import sys

import os

import mysql.connector


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "asterisk"),
    "password": os.getenv("DB_PASSWORD", "contraseña"),
    "database": os.getenv("DB_NAME", "asterisk"),
}


if len(sys.argv) < 2:
    raise SystemExit("Uso: python scripts/subscriber_cost.py <extension>")


numero_usuario = (sys.argv[1] + "-softphone").strip()

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Consulta para obtener el costo total por usuario
    query = """
        SELECT 
            SUM(costo) AS costo_total
        FROM facturacion
        WHERE src = %s
          AND fecha >= CURDATE() - INTERVAL 1 MONTH;
    """
    cursor.execute(query, (numero_usuario,))
    resultado = cursor.fetchone()

    if resultado and resultado[0] is not None:
        costo_total = resultado[0]  # El costo total es el primer valor
        # Pasa el costo como una variable de entorno
        print(f"El coste del abonado {sys.argv[1]} es de {costo_total}")

    else:
        print("Usted no ha tenido gastos")

except mysql.connector.Error as err:
    print(f"Error de base de datos: {err}")
finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()

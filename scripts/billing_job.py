import os
from datetime import datetime

import mysql.connector


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "asterisk"),
    "password": os.getenv("DB_PASSWORD", "contraseña"),
    "database": os.getenv("DB_NAME", "asterisk"),
}


try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Consulta para obtener llamadas no facturadas
    query = """
       SELECT 
            c.uniqueid,
            c.src,
            c.dst,
            c.duration,
            t.costo_por_minuto
        FROM cdr c
        JOIN tarifas t
            ON (CASE
                    WHEN c.dst LIKE '2%' OR c.dst LIKE '200%' THEN 'nacional'
                    WHEN c.dst LIKE '6%' OR c.dst LIKE '600%' THEN 'internacional'
                END) = t.destino
            AND (CASE
                    WHEN HOUR(c.calldate) BETWEEN 22 AND 23 OR HOUR(c.calldate) BETWEEN 0 AND 6 THEN 'nocturno'
                    ELSE 'normal'
                END) = t.horario
        WHERE NOT EXISTS (SELECT 1 FROM facturacion f WHERE f.uniqueid = c.uniqueid);
    """

    cursor.execute(query)
    llamadas = cursor.fetchall()

    # Insertar los datos en la tabla de facturación
    for uniqueid, src, dst, duracion, costo_por_minuto in llamadas:
        total_costo = (duracion / 60.0) * float(costo_por_minuto)
        insert_query = """
            INSERT INTO facturacion (uniqueid, src, dst, duracion, costo, fecha)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (uniqueid, src, dst, duracion, round(total_costo, 4), datetime.now()))

    # Confirmar cambios
    conn.commit()

except mysql.connector.Error as err:
    print(f"Error de base de datos: {err}")
    conn.rollback()

finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()

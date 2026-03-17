import os

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'cambia-esta-clave-secreta')

# Configuración de la base de datos
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': 'asterisk',
    'password': os.getenv('DB_PASSWORD', 'contraseña'),
    'database': 'asterisk',
}

portal_password = os.getenv('MARCHEL_PORTAL_PASSWORD', 'Hola123')

def obtener_datos_usuario(numero):
    """Consulta el costo y estadísticas de llamadas del usuario"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    consulta_costo = """
        SELECT SUM(costo) AS total_costo
        FROM facturacion
        WHERE src = %s AND fecha >= CURDATE() - INTERVAL 1 MONTH;
    """
    consulta_estadisticas = """
        SELECT COUNT(*) AS llamadas_realizadas, SUM(duracion) AS total_duracion
        FROM facturacion
        WHERE src = %s AND fecha >= CURDATE() - INTERVAL 1 MONTH;
    """

    cursor.execute(consulta_costo, (numero,))
    costo = cursor.fetchone()

    cursor.execute(consulta_estadisticas, (numero,))
    estadisticas = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        'total_costo': costo['total_costo'] or 0,
        'llamadas_realizadas': estadisticas['llamadas_realizadas'] or 0,
        'total_duracion': estadisticas['total_duracion'] or 0
    }

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        numero = request.form['numero'] + "-softphone"
        password = request.form['password']

        # Simulación de autenticación (ajustar con base de datos si es necesario)
        if password == portal_password:
            session['usuario'] = numero
            return redirect(url_for('dashboard'))

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    datos = obtener_datos_usuario(session['usuario'])
    return render_template('dashboard.html', datos=datos)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Funciones adicionales para app.py

def obtener_estadisticas_comparativas(numero):
    """Obtiene estadísticas comparativas del usuario frente a otros usuarios"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Promedio de llamadas de todos los usuarios
    consulta_promedio = """
        SELECT AVG(total_llamadas) as promedio_llamadas
        FROM (
            SELECT COUNT(*) as total_llamadas
            FROM facturacion
            WHERE fecha >= CURDATE() - INTERVAL 1 MONTH
            GROUP BY src
        ) as llamadas_por_usuario;
    """

    # Total de llamadas del usuario actual
    consulta_usuario = """
        SELECT COUNT(*) as total_llamadas
        FROM facturacion
        WHERE src = %s AND fecha >= CURDATE() - INTERVAL 1 MONTH;
    """

    # Top 5 destinos más llamados por el usuario
    consulta_destinos = """
        SELECT dst, COUNT(*) as total_llamadas, SUM(duracion) as duracion_total
        FROM facturacion
        WHERE src = %s AND fecha >= CURDATE() - INTERVAL 1 MONTH
        GROUP BY dst
        ORDER BY total_llamadas DESC
        LIMIT 5;
    """

    # Distribución de llamadas por día de la semana
    consulta_dias = """
        SELECT DAYNAME(fecha) as dia_semana, DAYOFWEEK(fecha) as dow, COUNT(*) as total_llamadas
        FROM facturacion
        WHERE src = %s AND fecha >= CURDATE() - INTERVAL 1 MONTH
        GROUP BY dia_semana, dow
        ORDER BY dow;
    """

    # Distribución de llamadas por hora del día
    consulta_horas = """
        SELECT HOUR(fecha) as hora, COUNT(*) as total_llamadas
        FROM facturacion
        WHERE src = %s AND fecha >= CURDATE() - INTERVAL 1 MONTH
        GROUP BY hora
        ORDER BY hora;
    """

    cursor.execute(consulta_promedio)
    promedio = cursor.fetchone()

    cursor.execute(consulta_usuario, (numero,))
    usuario = cursor.fetchone()

    cursor.execute(consulta_destinos, (numero,))
    destinos = cursor.fetchall()

    cursor.execute(consulta_dias, (numero,))
    dias = cursor.fetchall()

    cursor.execute(consulta_horas, (numero,))
    horas = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        'promedio_llamadas': promedio['promedio_llamadas'] or 0,
        'llamadas_usuario': usuario['total_llamadas'] or 0,
        'destinos_frecuentes': destinos,
        'llamadas_por_dia': dias,
        'llamadas_por_hora': horas
    }

def obtener_tarifas():
    """Obtiene la tabla de tarifas actual"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    consulta_tarifas = """
        SELECT destino, horario, costo_por_minuto
        FROM tarifas
        ORDER BY costo_por_minuto;
    """

    cursor.execute(consulta_tarifas)
    tarifas = cursor.fetchall()

    cursor.close()
    conn.close()

    return tarifas

def obtener_historial_llamadas(numero, limite=50):
    """Obtiene el historial detallado de llamadas"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    consulta_historial = """
        SELECT fecha, dst, duracion, costo, 
           CASE WHEN duracion > 0 THEN 'Contestada' ELSE 'No contestada' END as estado
        FROM facturacion
        WHERE src = %s
        ORDER BY fecha DESC
        LIMIT %s;
    """
    cursor.execute(consulta_historial, (numero, limite))
    historial = cursor.fetchall()

    cursor.close()
    conn.close()

    return historial

def obtener_tendencias_consumo(numero):
    """Obtiene tendencias de consumo en los últimos 6 meses"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    consulta_tendencias = """
        SELECT DATE_FORMAT(fecha, '%Y-%m') as mes,
               SUM(costo) as costo_total,
               COUNT(*) as total_llamadas,
               SUM(duracion) as duracion_total
        FROM facturacion
        WHERE src = %s AND fecha >= CURDATE() - INTERVAL 6 MONTH
        GROUP BY DATE_FORMAT(fecha, '%Y-%m')
        ORDER BY DATE_FORMAT(fecha, '%Y-%m');
    """

    cursor.execute(consulta_tendencias, (numero,))
    tendencias = cursor.fetchall()

    cursor.close()
    conn.close()

    return tendencias

# Añadir estas rutas a app.py

@app.route('/estadisticas')
def estadisticas():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    datos = obtener_estadisticas_comparativas(session['usuario'])
    return render_template('estadisticas.html', datos=datos)

@app.route('/tarifas')
def tarifas():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    lista_tarifas = obtener_tarifas()
    return render_template('tarifas.html', tarifas=lista_tarifas)

@app.route('/historial')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    historico = obtener_historial_llamadas(session['usuario'])
    return render_template('historial.html', historial=historico)

@app.route('/tendencias')
def tendencias():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    datos_tendencias = obtener_tendencias_consumo(session['usuario'])
    return render_template('tendencias.html', tendencias=datos_tendencias)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)


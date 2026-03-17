#!/usr/bin/env python3
"""
Script de Tarificación Automática para Asterisk
===============================================

Propósito: Procesar registros de CDR y calcular automáticamente
los costos según tarifas configuradas en base de datos.

Uso:
    python3 tarificar.py
    
Configuración: .env (variables DB_*)
Ejecución: cron (cada 5 minutos recomendado)

Tabla CDR: Contiene registros de todas las llamadas
Tabla tarifas: Precios por destino y horario
Tabla facturacion: Resultado de tarificación
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, List, Tuple

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/tarificar.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuración de base de datos desde variables de entorno
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "asterisk"),
    "password": os.getenv("DB_PASSWORD", "contraseña"),
    "database": os.getenv("DB_NAME", "asterisk"),
}


def get_connection():
    """Obtiene conexión a base de datos"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        logger.error(f"Error conectando a BD: {e}")
        raise


def get_unprocessed_cdr(connection) -> List[Dict]:
    """Obtiene registros CDR no tarificados"""
    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT 
        c.id,
        c.uniqueid,
        c.src,
        c.dst,
        c.calldate,
        c.duration,
        c.billsec,
        c.disposition
    FROM cdr c
    LEFT JOIN facturacion f ON c.uniqueid = f.uniqueid
    WHERE f.id IS NULL
    AND c.disposition = 'ANSWERED'
    AND c.duration > 0
    ORDER BY c.calldate DESC
    LIMIT 100
    """
    
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    
    return records


def classify_destination(dst: str) -> str:
    """Clasifica destino como nacional o internacional"""
    # Números que comienzan con 1-8: nacional (interno)
    # Números que comienzan con 9: internacional (simulado)
    
    if dst.startswith('9'):
        return 'internacional'
    else:
        return 'nacional'


def classify_time_period(calldate: datetime) -> str:
    """Clasifica horario como normal o nocturno"""
    hour = calldate.hour
    
    # Horario normal: 08:00 a 20:00
    # Horario nocturno: 20:00 a 08:00
    
    if 8 <= hour < 20:
        return 'normal'
    else:
        return 'nocturno'


def get_tarifa(connection, destino: str, horario: str) -> Optional[float]:
    """Obtiene tarifa según destino y horario"""
    cursor = connection.cursor()
    
    query = """
    SELECT costo_por_minuto
    FROM tarifas
    WHERE destino = %s
    AND horario = %s
    """
    
    cursor.execute(query, (destino, horario))
    result = cursor.fetchone()
    cursor.close()
    
    return result[0] if result else None


def calcular_costo(connection, src: str, dst: str, 
                   calldate: datetime, billsec: int) -> Tuple[float, Dict]:
    """Calcula costo de la llamada"""
    
    # Obtener clasificaciones
    destino = classify_destination(dst)
    horario = classify_time_period(calldate)
    
    # Obtener tarifa
    costo_por_minuto = get_tarifa(connection, destino, horario)
    
    if costo_por_minuto is None:
        logger.warning(f"No se encontró tarifa para {destino}/{horario}")
        costo_total = 0.0
    else:
        # Calcular costo: (segundos / 60) * costo_por_minuto
        minutos = billsec / 60.0
        costo_total = round(minutos * costo_por_minuto, 4)
    
    detalles = {
        'destino': destino,
        'horario': horario,
        'minutos': round(billsec / 60.0, 2),
        'costo_por_minuto': costo_por_minuto,
        'costo_total': costo_total
    }
    
    return costo_total, detalles


def guardar_facturacion(connection, cdr_id: int, uniqueid: str, 
                       src: str, dst: str, billsec: int, costo: float):
    """Guarda registro en tabla facturacion"""
    cursor = connection.cursor()
    
    query = """
    INSERT INTO facturacion (uniqueid, src, dst, duracion, costo, fecha)
    VALUES (%s, %s, %s, %s, %s, NOW())
    """
    
    try:
        cursor.execute(query, (uniqueid, src, dst, billsec, costo))
        connection.commit()
        logger.info(f"Registrado: {uniqueid} - {src} → {dst} - ${costo}")
        return True
    except Error as e:
        logger.error(f"Error al guardar facturación: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()


def procesar_tarifacion():
    """Función principal de tarificación"""
    
    logger.info("=" * 60)
    logger.info("Iniciando proceso de tarificación automática")
    logger.info("=" * 60)
    
    try:
        connection = get_connection()
        
        # Obtener CDRs sin procesar
        cdrs = get_unprocessed_cdr(connection)
        logger.info(f"Encontrados {len(cdrs)} registros por procesar")
        
        if not cdrs:
            logger.info("No hay registros por procesar")
            connection.close()
            return True
        
        # Procesar cada CDR
        procesados = 0
        errores = 0
        ingresos_totales = 0.0
        
        for cdr in cdrs:
            try:
                # Calcular costo
                costo, detalles = calcular_costo(
                    connection,
                    cdr['src'],
                    cdr['dst'],
                    cdr['calldate'],
                    cdr['billsec']
                )
                
                # Guardar en facturacion
                if guardar_facturacion(
                    connection,
                    cdr['id'],
                    cdr['uniqueid'],
                    cdr['src'],
                    cdr['dst'],
                    cdr['billsec'],
                    costo
                ):
                    procesados += 1
                    ingresos_totales += costo
                    
                    # Log detallado
                    logger.debug(
                        f"  Destino: {detalles['destino']}, "
                        f"Horario: {detalles['horario']}, "
                        f"Minutos: {detalles['minutos']}, "
                        f"Costo: ${costo}"
                    )
                else:
                    errores += 1
                    
            except Exception as e:
                logger.error(f"Error procesando CDR {cdr['uniqueid']}: {e}")
                errores += 1
        
        connection.close()
        
        # Resumen
        logger.info("=" * 60)
        logger.info(f"Proceso completado:")
        logger.info(f"  ✓ Registros procesados: {procesados}")
        logger.info(f"  ✗ Errores: {errores}")
        logger.info(f"  💰 Ingresos totales: ${ingresos_totales:.2f}")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Error crítico en tarificación: {e}")
        return False


if __name__ == '__main__':
    # Ejecutar tarificación
    success = procesar_tarifacion()
    
    # Salir con código apropiado
    sys.exit(0 if success else 1)

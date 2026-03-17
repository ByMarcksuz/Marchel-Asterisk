# LRSS Asterisk - Inventario Completo de Archivos

Este documento lista todos los archivos necesarios para la práctica de Asterisk y tarificación, indicando su estado actual.

---

## 📋 RESUMEN

| Categoría | Total | Listos ✅ | Creados 🆕 | Falta |
|-----------|-------|---------|-----------|-------|
| Archivos Asterisk | 13 | 13 | 0 | 0 |
| Archivos Sistema | 8 | 3 | 5 | 0 |
| Scripts/Aplicación | 6 | 4 | 1 | 0 |
| **TOTAL** | **27** | **20** | **6** | **0** |

---

## 🔧 ARCHIVOS DE ASTERISK (`/etc/asterisk/`)

Ubicación en proyecto: `config/asterisk/`

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `pjsip.conf` | Usuarios SIP (2001-2003, 1010, 1001-1003) | ✅ EXISTE |
| `extensions.conf` | Dialplan (office-phone, operadora, soporte) | ✅ EXISTE |
| `voicemail.conf` | Buzones de voz | ✅ EXISTE |
| `musiconhold.conf` | Clases de música en espera | ✅ EXISTE |
| `indications.conf` | Tonos del país | ✅ EXISTE |
| `queues.conf` | Cola soporte-tecnico | ✅ EXISTE |
| `features.conf` | Códigos de transferencia (#1, *2) | ✅ EXISTE |
| `confbridge.conf` | Salas de conferencia | ✅ EXISTE |
| `cdr.conf` | Activa CDR logging | ✅ EXISTE |
| `res_odbc.conf` | Conexión BD vía ODBC | ✅ EXISTE |
| `extconfig.conf` | Mapeo de config externa | ✅ EXISTE |
| `cdr_odbc.conf` | Parámetros almacenamiento CDR | ✅ EXISTE |
| `cdr_adaptive_odbc.conf` | Mapeo de campos CDR a BD | ✅ EXISTE |

**Total: 13/13 ✅**

---

## 🖥️ ARCHIVOS DEL SISTEMA

### Grupo 1: Configuración Asterisk

| Archivo | Destino | Contenido | Estado |
|---------|---------|-----------|--------|
| `config/default/asterisk` | `/etc/default/asterisk` | Usuario, límites, opciones | 🆕 CREADO |
| `config/odbc/odbcinst.ini` | `/etc/odbcinst.ini` | Drivers ODBC MySQL | ✅ ACTUALIZADO |
| `config/odbc/odbc.ini` | `/etc/odbc.ini` | DSN MySQL-asterisk | ✅ EXISTE |

### Grupo 2: Festival TTS

| Archivo | Destino | Contenido | Estado |
|---------|---------|-----------|--------|
| `config/festival/festival.scm` | `/etc/festival.scm` | Config global Festival | 🆕 CREADO |
| `config/festival/festival_asterisk.scm` | `/usr/share/festival/voices/spanish/festival.scm` | Funciones TTS para Asterisk | 🆕 CREADO |
| `config/systemd/festival.service` | `/etc/systemd/system/festival.service` | Servicio systemd Festival | 🆕 CREADO |

---

## 💻 SCRIPTS Y APLICACIÓN WEB

### Scripts de Tarificación

| Archivo | Ubicación | Propósito | Estado |
|---------|-----------|----------|--------|
| `scripts/tarificar.py` | `/usr/local/bin/tarificar.py` | Tarificación automática con cron | 🆕 CREADO |
| `scripts/billing_job.py` | N/A | Alternativa billing (legacy) | ✅ EXISTE |
| `scripts/subscriber_cost.py` | N/A | Cálculo costo por suscriptor | ✅ EXISTE |

### Aplicación Web Flask

| Archivo | Ubicación | Propósito | Estado |
|---------|-----------|----------|--------|
| `app/web/app.py` | `/var/www/marchel/app.py` | App principal | ✅ EXISTE |
| `app/web/__init__.py` | `/var/www/marchel/__init__.py` | Init Python | ✅ EXISTE |
| `app/web/templates/index.html` | `/var/www/marchel/templates/` | Login | ✅ EXISTE |
| `app/web/templates/dashboard.html` | `/var/www/marchel/templates/` | Panel usuario | ✅ EXISTE |
| `app/web/templates/historial.html` | `/var/www/marchel/templates/` | Historial llamadas | ✅ EXISTE |
| `app/web/templates/tarifas.html` | `/var/www/marchel/templates/` | Tarifas | ✅ EXISTE |
| `app/web/templates/estadisticas.html` | `/var/www/marchel/templates/` | Estadísticas | ✅ EXISTE |
| `app/web/templates/tendencias.html` | `/var/www/marchel/templates/` | Tendencias | ✅ EXISTE |

---

## 📁 ESTRUCTURA DE DIRECTORIOS

```
config/
├── asterisk/              (13 archivos .conf) ✅
├── default/
│   └── asterisk           🆕
├── systemd/
│   └── festival.service   🆕
├── festival/
│   ├── festival.scm       🆕
│   └── festival_asterisk.scm 🆕
└── odbc/
    ├── odbc.ini           ✅
    └── odbcinst.ini       ✅

scripts/
├── tarificar.py           🆕
├── billing_job.py         ✅
└── subscriber_cost.py     ✅

app/web/
├── app.py                 ✅
├── __init__.py            ✅
├── static/                ✅
└── templates/             ✅
    ├── index.html         ✅
    ├── dashboard.html     ✅
    ├── historial.html     ✅
    ├── tarifas.html       ✅
    ├── estadisticas.html  ✅
    └── tendencias.html    ✅

docs/
├── legacy/practica-2-notes.md     ✅ (actualizado con Parte 3)
└── TESTING_GUIDE.md               ✅
```

---

## 🚀 ARCHIVOS RECIÉN CREADOS (6)

### 1. `config/default/asterisk`
- **Propósito:** Configuración del servicio systemd de Asterisk
- **Contenido:** Usuario, grupo, límites de archivos abiertos
- **Instalación:** `sudo cp config/default/asterisk /etc/default/asterisk`

### 2. `config/systemd/festival.service`
- **Propósito:** Servicio systemd para Festival TTS
- **Contenido:** Definición de servicio, usuario, reinicio automático
- **Instalación:** `sudo cp config/systemd/festival.service /etc/systemd/system/festival.service`

### 3. `config/festival/festival.scm`
- **Propósito:** Configuración principal de Festival
- **Contenido:** Parámetros de síntesis, voz por defecto, puerto
- **Instalación:** `sudo cp config/festival/festival.scm /etc/festival.scm`

### 4. `config/festival/festival_asterisk.scm`
- **Propósito:** Extensiones de Festival específicas para Asterisk
- **Contenido:** Función `tts_textasterisk()`, convertidores de números/fechas
- **Instalación:** `sudo cp config/festival/festival_asterisk.scm /usr/share/festival/voices/spanish/festival.scm`

### 5. `scripts/tarificar.py`
- **Propósito:** Script principal de tarificación automática
- **Contenido:** Lectura de CDR, cálculo de costos, almacenamiento en BD
- **Instalación:** `sudo cp scripts/tarificar.py /usr/local/bin/tarificar.py && sudo chmod 755 /usr/local/bin/tarificar.py`
- **Ejecución:** Cron cada 5 minutos: `*/5 * * * * /usr/bin/python3 /usr/local/bin/tarificar.py`

### 6. `config/odbc/odbcinst.ini`
- **Propósito:** Configuración de drivers ODBC
- **Contenido:** Registro de MySQL ODBC 9.2 (Unicode y ANSI)
- **Instalación:** `sudo cp config/odbc/odbcinst.ini /etc/odbcinst.ini`

---

## 📝 ARCHIVOS ACTUALIZADOS

### `docs/legacy/practica-2-notes.md`
- **Agregado:** Parte 3 - "Instalación de Archivos en el Sistema"
- **Contenido:**
  - Instrucciones de copia de archivos Asterisk
  - Pasos de configuración de usuario/drivers/DSN
  - Setup de Festival TTS como servicio
  - Instalación de scripts y app web
  - Checklist de instalación
  - Troubleshooting

### `config/odbc/odbcinst.ini`
- **Mejorado:** Documentación más completa
- **Agregado:** Drivers alternativos y notas

---

## ✅ VERIFICACIÓN POST-INSTALACIÓN

### Copiar todos los archivos (script bash)

```bash
#!/bin/bash
#  install_all.sh - Copia todos los archivos a sus ubicaciones finales

# Archivos Asterisk
sudo cp config/asterisk/*.conf /etc/asterisk/
sudo chown asterisk:asterisk /etc/asterisk/*.conf
sudo chmod 640 /etc/asterisk/*.conf

# Archivos del sistema
sudo cp config/default/asterisk /etc/default/asterisk
sudo chown root:root /etc/default/asterisk
sudo chmod 644 /etc/default/asterisk

sudo cp config/odbc/odbcinst.ini /etc/odbcinst.ini
sudo cp config/odbc/odbc.ini /etc/odbc.ini
sudo chown root:root /etc/odbc.ini
sudo chmod 644 /etc/odbc.ini

sudo cp config/festival/festival.scm /etc/festival.scm
sudo chown root:root /etc/festival.scm
sudo chmod 644 /etc/festival.scm

sudo cp config/systemd/festival.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable festival.service

# Scripts
sudo cp scripts/tarificar.py /usr/local/bin/tarificar.py
sudo chmod 755 /usr/local/bin/tarificar.py

# Aplicación web
sudo mkdir -p /var/www/marchel
sudo cp -r app/web/* /var/www/marchel/
sudo chown -R www-data:www-data /var/www/marchel
sudo chmod 755 /var/www/marchel

echo "✅ Todos los archivos instalados"
```

### Verificar instalación

```bash
# Archivos Asterisk
ls -la /etc/asterisk/*.conf | wc -l  # Debe ser 13

# Archivos sistema
ls -la /etc/default/asterisk
ls -la /etc/odbcinst.ini
ls -la /etc/odbc.ini
ls -la /etc/festival.scm

# Servicio Festival
systemctl status festival.service

# Script tarificación
ls -la /usr/local/bin/tarificar.py
/usr/local/bin/tarificar.py --help

# App web
ls -la /var/www/marchel/
```

---

## 🎯 PRÓXIMO PASO

Ver [TESTING_GUIDE.md](TESTING_GUIDE.md) para validar la configuración sin necesidad de VM completa.

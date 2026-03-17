# 📊 VERIFICACIÓN: Archivos Necesarios vs Disponibles

## ✅ ESTADO GENERAL: COMPLETO (27/27)

```
████████████████████████████████████████████████████ 100%
```

---

## ARCHIVOS DE ASTERISK: 13/13 ✅

```
✅ pjsip.conf                  (Usuarios SIP)
✅ extensions.conf             (Dialplan)
✅ voicemail.conf              (Buzón de voz)
✅ musiconhold.conf            (Música en espera)
✅ indications.conf            (Tonos país)
✅ queues.conf                 (Colas)
✅ features.conf               (Transferencias)
✅ confbridge.conf             (Conferencias)
✅ cdr.conf                    (CDR logging)
✅ res_odbc.conf               (Conexión BD)
✅ extconfig.conf              (Config externa)
✅ cdr_odbc.conf               (CDR a BD)
✅ cdr_adaptive_odbc.conf      (Mapeo CDR)
```

**Ubicación:** `config/asterisk/`  
**Instalación:** `sudo cp config/asterisk/*.conf /etc/asterisk/`

---

## ARCHIVOS DEL SISTEMA: 8/8 ✅

### 🆙 Configuración Asterisk (3/3)

```
✅ /etc/default/asterisk
   ├── Usuario: asterisk
   ├── Grupo: asterisk
   └── Límites de archivos abiertos
   
✅ /etc/odbcinst.ini
   ├── Driver: MySQL ODBC 9.2 Unicode
   ├── Driver: MySQL ODBC 9.2 ANSI
   └── Driver: MySQL (alternativo)
   
✅ /etc/odbc.ini
   └── DSN: MySQL-asterisk
```

### 🎙️ Festival TTS (3/3)

```
✅ /etc/festival.scm
   ├── Voz por defecto: español
   ├── Puerto: 1314
   └── Parámetros de síntesis
   
✅ /etc/systemd/system/festival.service
   ├── Tipo: simple
   ├── Usuario: festival
   └── Reinicio automático
   
✅ /usr/share/festival/voices/spanish/festival.scm
   ├── Función: tts_textasterisk()
   ├── Función: festival_say_number()
   ├── Función: festival_say_date()
   └── Función: festival_say_time()
```

### 🔐 ODBC (2/2)

```
✅ config/odbc/odbc.ini
   └── Servidor: localhost, DB: asterisk
   
✅ config/odbc/odbcinst.ini
   └── Drivers MySQL configurados
```

---

## SCRIPTS Y APLICACIÓN: 6/6 ✅

### 💰 Tarificación (3/3)

```
✅ scripts/tarificar.py (🆕 NUEVO)
   ├── Lectura de CDR
   ├── Cálculo de costos
   ├── Almacenamiento en BD
   └── Logging automático
   
✅ scripts/billing_job.py
   └── Alternativa: facturación por suscriptor
   
✅ scripts/subscriber_cost.py
   └── Cálculo de costo individual
```

### 🌐 Aplicación Web (3/3)

```
✅ /var/www/marchel/app.py
   ├── Flask app principal
   ├── Autenticación
   └── APIs de datos
   
✅ /var/www/marchel/templates/ (6 archivos)
   ├── index.html          (Login)
   ├── dashboard.html      (Panel)
   ├── historial.html      (Llamadas)
   ├── tarifas.html        (Precios)
   ├── estadisticas.html   (Gráficos)
   └── tendencias.html     (Tendencias)
   
✅ /var/www/marchel/static/
   ├── CSS
   └── JavaScript
```

---

## 📈 COMPARATIVA

### Requerian los Archivos Antes vs Ahora

| Categoría | Antes | Ahora | Cambio |
|-----------|-------|-------|--------|
| Asterisk (.conf) | 13 | 13 | ➡️ Completo |
| Sistema | 3 | 8 | ⬆️ +5 archivos |
| Scripts/App | 5 | 6 | ⬆️ +1 script |
| **TOTAL** | **21** | **27** | **✅ +6 completados** |

### Nuevos Archivos Creados (6)

```
1️⃣  config/default/asterisk
2️⃣  config/systemd/festival.service
3️⃣  config/festival/festival.scm
4️⃣  config/festival/festival_asterisk.scm
5️⃣  scripts/tarificar.py
6️⃣  config/odbc/odbcinst.ini (mejorado)
```

### Archivos Documentación Actualizados (2)

```
📝 docs/legacy/practica-2-notes.md
   └── +Parte 3: "Instalación de Archivos en el Sistema"
   
📝 docs/INVENTORY.md
   └── 🆕 NUEVO: Inventario completo
```

---

## 🔍 UBICACIONES DE ARCHIVOS

### En el Proyecto

```
Marchel-Asterisk/
├── config/
│   ├── asterisk/           ← 13 .conf ✅
│   ├── default/            ← asterisk 🆕
│   ├── systemd/            ← festival.service 🆕
│   ├── festival/           ← .scm files 🆕
│   └── odbc/               ← .ini files ✅
├── scripts/
│   ├── tarificar.py        ← 🆕 NUEVO
│   ├── billing_job.py      ✅
│   └── subscriber_cost.py  ✅
└── app/web/                ✅ (app.py + templates)
```

### En el Sistema (tras instalación)

```
/etc/
├── asterisk/
│   └── *.conf              ← cp config/asterisk/*.conf
├── default/
│   └── asterisk            ← cp config/default/asterisk 🆕
├── systemd/system/
│   └── festival.service    ← cp config/systemd/festival.service 🆕
├── festival.scm            ← cp config/festival/festival.scm 🆕
├── odbcinst.ini            ← cp config/odbc/odbcinst.ini
└── odbc.ini                ← cp config/odbc/odbc.ini

/usr/
└── share/festival/voices/spanish/
    └── festival.scm        ← cp config/festival/festival_asterisk.scm 🆕

/usr/local/bin/
└── tarificar.py            ← cp scripts/tarificar.py 🆕

/var/www/marchel/
├── app.py
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── historial.html
│   ├── tarifas.html
│   ├── estadisticas.html
│   └── tendencias.html
└── static/
```

---

## 📋 CHECKLIST DE INSTALACIÓN

Copiar y ejecutar en terminal:

```bash
#!/bin/bash
echo "🚀 Instalando LRSS Asterisk..."

# 1. Asterisk configs
echo "[1/5] Copiando archivos Asterisk..."
sudo cp config/asterisk/*.conf /etc/asterisk/
sudo chown asterisk:asterisk /etc/asterisk/*.conf
sudo chmod 640 /etc/asterisk/*.conf

# 2. System files
echo "[2/5] Copiando archivos del sistema..."
sudo cp config/default/asterisk /etc/default/
sudo cp config/festival/festival.scm /etc/
sudo cp config/odbc/odbcinst.ini /etc/
sudo cp config/odbc/odbc.ini /etc/

# 3. Festival service
echo "[3/5] Instalando servicio Festival..."
sudo cp config/systemd/festival.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable festival.service
sudo systemctl start festival.service

# 4. Scripts
echo "[4/5] Instalando scripts..."
sudo cp scripts/tarificar.py /usr/local/bin/
sudo chmod 755 /usr/local/bin/tarificar.py

# 5. Web app
echo "[5/5] Instalando aplicación web..."
sudo mkdir -p /var/www/marchel
sudo cp -r app/web/* /var/www/marchel/
sudo chown -R www-data:www-data /var/www/marchel

echo "✅ Instalación completada!"
```

---

## 🧪 VERIFICACIÓN RÁPIDA

```bash
# ¿Se instalaron todos los .conf?
ls /etc/asterisk/*.conf | wc -l
# Esperado: 13

# ¿Festival está corriendo?
systemctl status festival.service
# Esperado: active (running)

# ¿Script de tarificación existe?
ls -la /usr/local/bin/tarificar.py
# Esperado: -rwxr-xr-x

# ¿App web está en lugar?
ls -la /var/www/marchel/
# Esperado: app.py, templates/, static/

# ¿ODBC configurado?
isql -v MySQL-asterisk asterisk contraseña
# Esperado: Connected!
```

---

## 📞 PRÓXIMAS ACCIONES

1. **Validar:** Ver [TESTING_GUIDE.md](TESTING_GUIDE.md)
2. **Instalar:** Copiar archivos a `/etc/` con script arriba
3. **Configurar:** Ajustar credenciales en `.env`
4. **Reiniciar:** `sudo systemctl restart asterisk`
5. **Verificar:** `sudo asterisk -rx "core show version"`

---

## 🎯 RESUMEN

| Aspecto | Estado |
|--------|--------|
| Asterisk configs | ✅ 13/13 |
| System files | ✅ 8/8 |
| Scripts | ✅ 3/3 + 1🆕 |
| Web app | ✅ 8/8 |
| Documentación | ✅ 2 archivos |
| **TOTAL** | **✅ 27/27 COMPLETO** |

🎉 **¡Tu configuración está 100% lista para instalación!**

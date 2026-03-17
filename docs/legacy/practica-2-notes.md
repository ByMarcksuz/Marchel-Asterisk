# LRSS - Práctica Asterisk y Tarificación

**Proyecto de Laboratorio de Redes, Sistemas y Servicios**

Realizado por:
- Marcos Santos Aragón
- Chelsea Fernández Hernández
- Grupo: 3D2

---

## 1. Configuración de Asterisk

### Archivos principales a configurar

Los siguientes archivos de Asterisk necesitan ser modificados en `/etc/asterisk/`:

- `extensions.conf` - Dialplan (extensiones y flujos de llamada)
- `pjsip.conf` - Configuración de usuarios SIP
- `voicemail.conf` - Buzón de voz
- `musiconhold.conf` - Música mientras espera
- `indications.conf` - Tonos e indicadores (activar para país = es)
- `queues.conf` - Colas de atención
- `features.conf` - Características de transferencia (redirecciones)
- `confbridge.conf` - Sala de conferencias
- `cdr.conf` - Call Detail Records (registro de llamadas)
- `res_odbc.conf` - Conexión con base de datos
- `extconfig.conf` - Almacenamiento externo de configuración
- `cdr_odbc.conf` - Almacenamiento de CDR en base de datos
- `cdr_adaptive_odbc.conf` - Mapeo de campos CDR a base de datos

### Verificar estado de Asterisk en consola

```bash
sudo asterisk -rvvvvvvvvvc
```

### Notas sobre estrategias de colas

- **ringall** - Suena en todos al mismo tiempo hasta que alguien conteste
- **linear** - Llama a los miembros en orden secuencial
- **leastrecent** - Llama al agente que no ha atendido llamadas recientemente
- **random** - Llama a los agentes de forma aleatoria

### Conversión de archivos de audio

Para convertir archivos WAV al formato correcto (mono, 8 kHz):

```bash
sox /var/lib/asterisk/sounds/custom/archivo-original.wav -c 1 -r 8000 -t wav /var/lib/asterisk/sounds/custom/archivo.wav
```

---

## 2. Configuración de usuarios SIP (pjsip.conf)

### Requisitos previos

Festival TTS debe estar activo:
```bash
sudo festival --server
```

### Usuarios de oficina (2001 a 2003)

Cada usuario necesita tres secciones: endpoint, auth y aor.

```
[2001-softphone]
type=endpoint
context=office-phone
disallow=all
allow=ulaw
auth=2001-auth
aors=2001-softphone
language=es1

[2001-auth]
type=auth
auth_type=userpass
username=2001-softphone
password=Hola123

[2001-softphone]
type=aor
max_contacts=1
```

Repetir la misma estructura para 2002 y 2003.

### Usuario operadora (1010)

```
[1010]
type=endpoint
context=operadora-menu
disallow=all
allow=ulaw
auth=1010-auth
aors=1010

[1010-auth]
type=auth
auth_type=userpass
username=1010
password=Hola123

[1010]
type=aor
max_contacts=1
```

### Usuarios de soporte técnico (1001, 1002, 1003)

```
[1001-support]
type=endpoint
context=soporte-tecnico
disallow=all
allow=ulaw
auth=1001-auth
aors=1001-support

[1001-auth]
type=auth
auth_type=userpass
username=1001-support
password=Hola123

[1001-support]
type=aor
max_contacts=1
```

Repetir para 1002 y 1003.

---

## 3. Dialplan (extensions.conf)

### Contexto de oficina (office-phone)

```
[office-phone]
exten => 2001,1,Answer()
exten => 2001,n,Dial(PJSIP/2001-softphone,20,m)
exten => 2001,n,Set(CHANNEL(musicclass)=minecraft)
exten => 2001,n,VoiceMail(2001,u)
exten => 2001,n,Hangup()

exten => 2002,1,Answer()
exten => 2002,n,Dial(PJSIP/2002-softphone,20,m)
exten => 2002,n,Set(CHANNEL(musicclass)=minecraft)
exten => 2002,n,VoiceMail(2002,u)
exten => 2002,n,Hangup()

exten => 2003,1,Answer()
exten => 2003,n,Dial(PJSIP/2003-softphone,20,m)
exten => 2003,n,Set(CHANNEL(musicclass)=minecraft)
exten => 2003,n,VoiceMail(2003,u)
exten => 2003,n,Hangup()

; Buzón de voz
exten => 1000,1,VoiceMailMain(${CALLERID(num)})
exten => 1000,n,Hangup()

; Menú operadora
exten => 1010,1,Goto(operadora-menu,s,1)

; Llamada grupal (usuario)
exten => 9000,1,Answer()
exten => 9000,n,ConfBridge(1234,default_bridge,default_user)
exten => 9000,n,Hangup()

; Llamada grupal (administrador)
exten => 9001,1,Answer()
exten => 9001,n,ConfBridge(1234,default_bridge,default_admin)
exten => 9001,n,Hangup()
```

### Menú operadora (operadora-menu)

```
[operadora-menu]
exten => s,1,Answer()
exten => s,2,Playback(custom/BienvenidoMenu)
exten => s,3,Read(NUMBER,beep,9)
exten => s,n,BackGround(custom/NumCorrectos)
exten => s,n,SayDigits(${NUMBER})
exten => s,n,WaitExten()

exten => 1,1,Goto(operadora-submenu,s,1)
exten => 2,1,Goto(s,2)

exten => i,1,Verbose(1, Extensión inválida)
exten => i,n,Playback(custom/OpcionVal)
exten => i,n,Goto(s,3)

exten => t,1,Verbose(1,Colgado por Timeout)
exten => t,n,Congestion(3)
exten => t,n,Hangup()
```

### Submenú operadora (operadora-submenu)

```
[operadora-submenu]
exten => s,1,BackGround(custom/SubmenuAccs)
exten => s,n,WaitExten()

exten => 1,1,Answer()
exten => 1,n,Dial(PJSIP/2002-softphone)
exten => 1,n,Congestion(3)

exten => 2,1,Playback(custom/ReinicioRouter)
exten => 2,n,Congestion(3)
exten => 2,n,Hangup()

exten => 3,1,Playback(custom/DescribaBrev)
exten => 3,n,Record(/tmp/numero.wav,3,10,q)
exten => 3,n,Playback(custom/AgenteContacto)
exten => 3,n,Goto(soporte-tecnico,1000,1)

exten => t,1,Verbose(1,Colgado por Timeout)
exten => t,n,Hangup()

exten => i,1,Verbose(1, Extensión inválida)
exten => i,n,Playback(custom/OpcionVal)
exten => i,n,Goto(s,1)
```

### Contexto de soporte técnico (soporte-tecnico)

```
[soporte-tecnico]
exten => 1000,1,Answer()
exten => 1000,n,Playback(custom/EsperaUnMom)
exten => 1000,n,Queue(soporte-tecnico,t,,,45)
exten => 1000,n,Playback(custom/NoContactar)
exten => 1000,n,Congestion(3)
exten => 1000,n,Hangup()
```

---

## 4. Archivos de soporte Asterisk (24-27 de Febrero 2025)

### Buzón de voz (voicemail.conf)

```
[default]
2001 => 1234,2001-softphone
2002 => 1234,2002-softphone
2003 => 1234,2003-softphone
```

### Música en espera (musiconhold.conf)

```
[default]
mode=files
directory=/var/lib/asterisk/moh/minecraft
```

### Características de transferencia (features.conf)

```
[general]
atxfernoanswertimeout = 15

[featuremap]
blindxfer => #1
atxfer => *2
```

### Colas (queues.conf)

```
[soporte-tecnico]
musicclass = default
strategy = ringall
timeout = 15
retry = 5
maxlen = 5
wrapuptime = 10

member => PJSIP/1001-support
member => PJSIP/1002-support
member => PJSIP/1003-support
```

### Conferencias (confbridge.conf)

```
[default_user]
type=user
music_on_hold_when_empty=yes
quiet=no
announce_user_count=yes
announce_join_leave=yes
wait_marked=no
end_marked=no
dsp_drop_silence=no

[default_bridge]
type=bridge
language=es1

[default_admin]
type=user
marked=yes
admin=yes
pin=1234

[sample_user_menu]
type=menu
*=playback_and_continue(conf-usermenu)
*1=toggle_mute
1=toggle_mute
*4=decrease_listening_volume
4=decrease_listening_volume
*6=increase_listening_volume
6=increase_listening_volume
*7=decrease_talking_volume
7=decrease_talking_volume
*8=leave_conference
8=leave_conference
*9=increase_talking_volume
9=increase_talking_volume

[sample_admin_menu]
type=menu
*=playback_and_continue(conf-adminmenu)
*1=toggle_mute
1=toggle_mute
*2=admin_toggle_conference_lock
2=admin_toggle_conference_lock
*3=admin_kick_last
3=admin_kick_last
*4=decrease_listening_volume
4=decrease_listening_volume
*6=increase_listening_volume
6=increase_listening_volume
*7=decrease_talking_volume
7=decrease_talking_volume
*8=no_op
8=no_op
*9=increase_talking_volume
9=increase_talking_volume
```

---

## PARTE 2: Integración con Base de Datos MariaDB

### Instalación y Configuración

1. **Actualizar sistema**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Instalar MariaDB**
```bash
sudo apt install mariadb-server mariadb-client -y
sudo systemctl enable mariadb
```

3. **Verificar estado**
```bash
sudo systemctl status mariadb
```

4. **Configurar seguridad**
```bash
sudo mysql_secure_installation
```
Responder "Sí" a todas las opciones.

5. **Acceder a MariaDB**
```bash
sudo mysql -u root -p
```

6. **Crear base de datos y usuario**
```sql
CREATE DATABASE asterisk;
CREATE USER 'asterisk'@'localhost' IDENTIFIED BY 'contraseña';
GRANT ALL PRIVILEGES ON asterisk.* TO 'asterisk'@'localhost';
FLUSH PRIVILEGES;
```

7. **Verificar creación**
```sql
SELECT user, host FROM mysql.user;
SHOW GRANTS FOR 'asterisk'@'localhost';
```

### Crear tabla CDR

```sql
USE asterisk;
CREATE TABLE cdr (
    id INT PRIMARY KEY AUTO_INCREMENT,
    calldate DATETIME NOT NULL,
    clid VARCHAR(80) NOT NULL,
    src VARCHAR(80) NOT NULL,
    dst VARCHAR(80) NOT NULL,
    dcontext VARCHAR(80) NOT NULL,
    channel VARCHAR(80) NOT NULL,
    dstchannel VARCHAR(80),
    lastapp VARCHAR(80) NOT NULL,
    lastdata VARCHAR(80) NOT NULL,
    duration INT NOT NULL,
    billsec INT NOT NULL,
    disposition VARCHAR(45) NOT NULL,
    amaflags INT NOT NULL,
    accountcode VARCHAR(20),
    uniqueid VARCHAR(32) NOT NULL,
    userfield VARCHAR(255),
    peeraccount VARCHAR(80),
    linkedid VARCHAR(32),
    sequence INT
);
```

### Instalar conectores ODBC

```bash
sudo apt install -y libmariadb-dev libmariadb-dev-compat
sudo apt-get install unixodbc unixodbc-dev
sudo wget https://dev.mysql.com/get/Downloads/Connector-ODBC/9.2/mysql-connector-odbc_9.2.0-1ubuntu24.04_amd64.deb
sudo dpkg -i mysql-connector-odbc_9.2.0-1ubuntu24.04_amd64.deb
sudo apt install odbcinst
```

### Configurar Asterisk para base de datos

**res_odbc.conf**
```
[asterisk]
enabled => yes
dsn => MySQL-asterisk
username => asterisk
password => contraseña
pre-connect => yes
```

**extconfig.conf**
```
[settings]
cdr => odbc,asterisk,cdr
```

**cdr.conf**
```
[general]
enabled = yes
usegmtime = no
```

**cdr_odbc.conf**
```
[global]
dsn=MySQL-asterisk
username=asterisk
password=contraseña
loguniqueid=yes
dispositionstring=yes
table=cdr
usegmtime=no
```

**cdr_adaptive_odbc.conf**
```
[asterisk]
connection=asterisk
table=cdr
alias start => calldate
```

**odbc.ini**
```
[MySQL-asterisk]
Driver=MySQL ODBC 9.2 Unicode Driver
Description=MariaDB connection to 'asterisk' database
Server=localhost
Database=asterisk
User=asterisk
Password=contraseña
Port=3306
Option = 3
Socket=/var/run/mysqld/mysqld.sock
```

**odbcinst.ini**
```
[MySQL ODBC 9.2 Unicode Driver]
DRIVER=/usr/lib/x86_64-linux-gnu/odbc/libmyodbc9w.so
UsageCount=1
```

### Verificar conexión ODBC

```bash
isql -v MySQL-asterisk
```
(Escribir `quit` para salir)

### Reiniciar Asterisk y verificar

```bash
sudo systemctl restart asterisk
sudo asterisk -rx "odbc show"
```

### Probar almacenamiento de CDR

Hacer una llamada y verificar:
```sql
SELECT * FROM cdr ORDER BY calldate DESC;
```

---

## Tarificación

### Crear tabla de tarifas

```sql
CREATE TABLE tarifas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    destino VARCHAR(80) NOT NULL,
    horario VARCHAR(20) NOT NULL,
    costo_por_minuto DECIMAL(10,4) NOT NULL
);
INSERT INTO tarifas (destino, horario, costo_por_minuto) VALUES
('nacional', 'normal', 0.05),
('nacional', 'nocturno', 0.02),
('internacional', 'normal', 0.15),
('internacional', 'nocturno', 0.10);
```

### Crear tabla de facturación

```sql
CREATE TABLE facturacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    uniqueid VARCHAR(32) NOT NULL,
    src VARCHAR(80) NOT NULL,
    dst VARCHAR(80) NOT NULL,
    duracion INT NOT NULL,
    costo DECIMAL(10,4) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Automatizar tarificación con cron

```bash
crontab -e
```

Agregar línea:
```
*/5 * * * * /usr/bin/python3 /usr/local/bin/tarificar.py >> /var/log/tarificar.log 2>&1
```

Verificar cron:
```bash
crontab -l
sudo systemctl status cron
grep CRON /var/log/syslog
```

### Consultas útiles

Ver facturación:
```sql
SELECT * FROM facturacion ORDER BY fecha DESC;
```

Costo total de un usuario (último mes):
```sql
SELECT src, SUM(costo) AS costo_total
FROM facturacion
WHERE src = '2001' AND fecha >= CURDATE() - INTERVAL 1 MONTH
GROUP BY src;
```

---

## PARTE 3: Instalación de Archivos en el Sistema

### Archivos de configuración de Asterisk

**Ubicación:** `/etc/asterisk/`

Los siguientes archivos deben copiarse desde `config/asterisk/` a `/etc/asterisk/`:

```bash
sudo cp config/asterisk/*.conf /etc/asterisk/
sudo chown asterisk:asterisk /etc/asterisk/*.conf
sudo chmod 640 /etc/asterisk/*.conf
```

**Archivos a instalar:**
- `pjsip.conf` - Usuarios SIP y transporte
- `extensions.conf` - Dialplan completo
- `voicemail.conf` - Configuración buzón de voz
- `musiconhold.conf` - Clases de música en espera
- `features.conf` - Códigos de transferencia
- `confbridge.conf` - Salas de conferencia
- `queues.conf` - Colas de atención
- `cdr.conf` - Activa registro de llamadas
- `res_odbc.conf` - Conexión a BD vía ODBC
- `extconfig.conf` - Mapeo de config externa
- `cdr_odbc.conf` - Parámetros almacenamiento CDR
- `cdr_adaptive_odbc.conf` - Mapeo de campos CDR
- `indications.conf` - Tonos del país

### Archivos del sistema

**1. Configuración de usuario Asterisk**

**Ubicación:** `/etc/default/asterisk`

```bash
sudo cp config/default/asterisk /etc/default/asterisk
sudo chown root:root /etc/default/asterisk
sudo chmod 644 /etc/default/asterisk
```

**Contenido:**
```bash
AST_USER="asterisk"
AST_GROUP="asterisk"
ULIMIT_OPEN_FILES=65536
UMASK="0022"
ASTETCDIR="/etc/asterisk"
OPTIONS="-p"
```

**2. Drivers ODBC**

**Ubicación:** `/etc/odbcinst.ini`

```bash
sudo cp config/odbc/odbcinst.ini /etc/odbcinst.ini
sudo chown root:root /etc/odbcinst.ini
sudo chmod 644 /etc/odbcinst.ini
```

**Contenido:** Configuración de drivers MySQL ODBC 9.2

**3. Data Source Names (DSN)**

**Ubicación:** `/etc/odbc.ini`

```bash
sudo cp config/odbc/odbc.ini /etc/odbc.ini
sudo chown root:root /etc/odbc.ini
sudo chmod 644 /etc/odbc.ini
```

**Contenido:**
```ini
[MySQL-asterisk]
Driver=MySQL ODBC 9.2 Unicode Driver
Server=localhost
Database=asterisk
User=asterisk
Password=contraseña
Port=3306
```

**4. Configuración de Festival TTS**

**Ubicación:** `/etc/festival.scm`

```bash
sudo cp config/festival/festival.scm /etc/festival.scm
sudo chown root:root /etc/festival.scm
sudo chmod 644 /etc/festival.scm
```

**Servidor Festival como servicio systemd**

**Ubicación:** `/etc/systemd/system/festival.service`

```bash
sudo cp config/systemd/festival.service /etc/systemd/system/festival.service
sudo systemctl daemon-reload
sudo systemctl enable festival.service
sudo systemctl start festival.service
sudo systemctl status festival.service
```

**Contenido del servicio:**
```ini
[Unit]
Description=Festival TTS Service for Asterisk
After=syslog.target network.target

[Service]
Type=simple
User=festival
Group=festival
ExecStart=/usr/bin/festival --server
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### Aplicación Web y Scripts

**1. Script de Tarificación Automática**

**Ubicación:** `/usr/local/bin/tarificar.py`

```bash
sudo cp scripts/tarificar.py /usr/local/bin/tarificar.py
sudo chmod 755 /usr/local/bin/tarificar.py
```

**Ejecución automática con cron:**

```bash
sudo su - asterisk
crontab -e
```

Agregar línea:
```cron
*/5 * * * * /usr/bin/python3 /usr/local/bin/tarificar.py >> /var/log/tarificar.log 2>&1
```

**2. Aplicación Web Flask**

**Ubicación:** `/var/www/marchel/`

```bash
sudo mkdir -p /var/www/marchel
sudo cp -r app/web/* /var/www/marchel/
sudo chown -R www-data:www-data /var/www/marchel
sudo chmod 755 /var/www/marchel
```

**Estructura de directorios:**
```
/var/www/marchel/
├── app.py                  # Aplicación principal
├── __init__.py
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
└── templates/              # Plantillas HTML
    ├── index.html          # Página de login
    ├── dashboard.html      # Panel de usuario
    ├── historial.html      # Historial de llamadas
    ├── tarifas.html        # Tarifas configuradas
    ├── estadisticas.html   # Gráficos de estadísticas
    └── tendencias.html     # Tendencias de uso
```

**3. Ejecutar aplicación web**

Con gunicorn (recomendado):
```bash
cd /var/www/marchel
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5050 app:app
```

Con desarrollo (Flask):
```bash
cd /var/www/marchel
python3 app.py
```

### Permisos y usuarios recomendados

```bash
# Usuario Asterisk
sudo useradd -r -s /bin/false -d /var/lib/asterisk -m asterisk

# Usuario Festival (opcional)
sudo useradd -r -s /bin/false -d /var/lib/festival -m festival

# Usuario www-data ya existe generalmente
id www-data

# Verificar permisos
ls -la /etc/asterisk/*.conf
ls -la /etc/default/asterisk
ls -la /etc/odbc.ini
ls -la /etc/systemd/system/festival.service
```

### Checklist de instalación

- [ ] Todos los archivos .conf copiados a `/etc/asterisk/`
- [ ] `/etc/default/asterisk` configurado
- [ ] `/etc/odbcinst.ini` instalado
- [ ] `/etc/odbc.ini` con credenciales correctas
- [ ] Festival TTS servicio habilitado (`systemctl status festival`)
- [ ] `/usr/local/bin/tarificar.py` ejecutable
- [ ] Aplicación web en `/var/www/marchel/`
- [ ] Cron job configurado para tarificación
- [ ] Base de datos con tablas: cdr, tarifas, facturacion
- [ ] Asterisk reiniciado: `sudo systemctl restart asterisk`
- [ ] Verificar: `sudo asterisk -rx "core show version"`

### Troubleshooting de instalación

**Si ODBC no conecta:**
```bash
# Verificar drivers
odbcinst -j

# Probar DSN
isql -v MySQL-asterisk asterisk contraseña

# Ver logs
tail -f /var/log/syslog | grep odbc
```

**Si Festival no funciona:**
```bash
# Verificar servicio
systemctl status festival.service

# Probar conectar al servidor
echo "WAVE" | festival --tts
telnet localhost 1314
```

**Si las tarifas no se calculan:**
```bash
# Ejecutar script manualmente
/usr/bin/python3 /usr/local/bin/tarificar.py

# Ver logs
tail -f /var/log/tarificar.log

# Verificar tabla facturacion
mysql -u asterisk -pcontraseña asterisk -e "SELECT * FROM facturacion LIMIT 5;"
```

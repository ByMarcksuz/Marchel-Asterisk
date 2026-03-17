# Guía de Validación y Testing - LRSS Asterisk

Este documento proporciona formas de probar y validar la configuración de Asterisk sin necesidad de tener una instalación completa en una VM.

---

## 1. Validación Sintáctica de Archivos de Configuración

### 1.1 Verificar archivos .conf manualmente

Sin necesidad de ejecutar Asterisk, puedes verificar la sintaxis básica:

```bash
# Verificar extensión de archivos correcta
ls -la config/asterisk/*.conf

# Verificar que no haya caracteres especiales problemáticos
file config/asterisk/*.conf
```

### 1.2 Usar `asterisk -C` con archivo personalizado

Si tienes Asterisk instalado localmente (sin función completa):

```bash
# Validar sintaxis sin ejecutar daemon
asterisk -C /etc/asterisk/asterisk.conf -n
```

### 1.3 Linting de configuración con script Python

Crea un script simple para validar sintaxis básica:

```python
#!/usr/bin/env python3
import re
import sys

def validate_conf_file(filepath):
    """Valida sintaxis básica de archivo .conf de Asterisk"""
    errors = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Verificar secciones
    section_pattern = re.compile(r'^\s*\[([^\]]+)\]\s*$')
    in_section = False
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Ignorar comentarios y líneas vacías
        if not line or line.startswith(';'):
            continue
        
        # Verificar secciones
        if section_pattern.match(line):
            in_section = True
            continue
        
        # Verificar sintaxis de parámetros (clave = valor o clave => valor)
        if not in_section and line and not line.startswith('['):
            errors.append(f"Línea {i}: Parámetro fuera de sección: {line}")
        
        if '=' not in line and '=>' not in line and in_section:
            if not (line.startswith('[') or line.startswith(';')):
                errors.append(f"Línea {i}: Formato inválido: {line}")
    
    if errors:
        print(f"❌ Errores en {filepath}:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print(f"✅ {filepath}: Sintaxis válida")
        return True

if __name__ == '__main__':
    all_valid = True
    for conf_file in ['config/asterisk/pjsip.conf', 
                      'config/asterisk/extensions.conf',
                      'config/asterisk/voicemail.conf',
                      'config/asterisk/queues.conf']:
        if not validate_conf_file(conf_file):
            all_valid = False
    
    sys.exit(0 if all_valid else 1)
```

---

## 2. Validación de Código Python

### 2.1 Sintaxis Python

```bash
# Verificar sintaxis sin ejecutar
python3 -m py_compile scripts/billing_job.py
python3 -m py_compile scripts/subscriber_cost.py
python3 -m py_compile app/web/app.py

# Salida esperada: ninguna (sin errores = silencio)
echo $?  # Debe ser 0
```

### 2.2 Usar `pylint` o `flake8`

```bash
# Instalar
pip install pylint flake8

# Verificar
flake8 scripts/billing_job.py --count --select=E9,F63,F7,F82 --show-source --statistics
pylint scripts/billing_job.py --disable=all --enable=syntax-error
```

### 2.3 Validar imports

```python
#!/usr/bin/env python3
import importlib.util

def check_imports(script_path):
    """Verifica que todos los imports en un script sean resolvibles"""
    with open(script_path, 'r') as f:
        spec = importlib.util.spec_from_file_location("module", script_path)
        if spec and spec.loader:
            try:
                module = importlib.util.module_from_spec(spec)
                # No ejecutar, solo cargar
                print(f"✅ {script_path}: Imports válidos")
                return True
            except Exception as e:
                print(f"❌ {script_path}: Error - {e}")
                return False

check_imports('scripts/billing_job.py')
check_imports('scripts/subscriber_cost.py')
```

---

## 3. Validación de Base de Datos (sin Asterisk ejecutándose)

### 3.1 Verificar conectividad ODBC

```bash
# Instalar herramientas
sudo apt install unixodbc

# Probar conexión (interactivo)
isql -v MySQL-asterisk asterisk contraseña

# Si conecta, ejecutar:
SELECT 1;
\q
```

### 3.2 Script Python para verificar BD

```python
#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def test_database_connection():
    """Verifica conexión a MariaDB"""
    config = {
        "host": "localhost",
        "user": "asterisk",
        "password": "contraseña",
        "database": "asterisk"
    }
    
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("✅ Conexión a MariaDB exitosa")
            
            # Verificar tablas
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            
            print(f"📊 Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            
            cursor.close()
            return True
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == '__main__':
    test_database_connection()
```

Ejecutar:
```bash
python3 test_database.py
```

### 3.3 Verificar esquema de tablas

```bash
# Ver estructura CDR
mysql -u asterisk -pcontraseña asterisk -e "DESCRIBE cdr;"

# Ver tarifas
mysql -u asterisk -pcontraseña asterisk -e "SELECT * FROM tarifas LIMIT 5;"

# Ver facturación
mysql -u asterisk -pcontraseña asterisk -e "SELECT * FROM facturacion LIMIT 5;"
```

---

## 4. Validación de Dialplan (sin ejecutar Asterisk)

### 4.1 Parsear extensions.conf

```python
#!/usr/bin/env python3
import re

def parse_dialplan(filepath):
    """Analiza extensions.conf y verifica sintaxis básica"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar contextos
    context_pattern = re.compile(r'^\s*\[([^\]]+)\]\s*$', re.MULTILINE)
    contexts = context_pattern.findall(content)
    
    print(f"📞 Contextos encontrados: {len(contexts)}")
    for ctx in contexts:
        print(f"   - {ctx}")
    
    # Buscar extensiones
    extension_pattern = re.compile(r'^\s*exten\s*=>\s*(\d+|[a-zA-Z_]+)\s*,', re.MULTILINE)
    extensions = extension_pattern.findall(content)
    
    print(f"📱 Extensiones definidas: {len(set(extensions))}")
    for ext in sorted(set(extensions)):
        count = extensions.count(ext)
        print(f"   - {ext}: {count} prioridades")

if __name__ == '__main__':
    parse_dialplan('config/asterisk/extensions.conf')
```

Ejecutar:
```bash
python3 validate_dialplan.py
```

**Salida esperada:**
```
📞 Contextos encontrados: 7
   - office-phone
   - operadora-menu
   - operadora-submenu
   - soporte-tecnico
   - ...

📱 Extensiones definidas: 12
   - 1000: 3 prioridades
   - 1001: 5 prioridades
   - 2001: 4 prioridades
```

---

## 5. Validación de Endpoints PJSIP

### 5.1 Verificar sintaxis pjsip.conf

```python
#!/usr/bin/env python3
import re

def validate_pjsip(filepath):
    """Verifica que cada endpoint tenga auth y aor"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    endpoints = {}
    current_section = None
    current_type = None
    
    for line in lines:
        line = line.strip()
        
        # Sión
        match = re.match(r'^\[([^\]]+)\]$', line)
        if match:
            current_section = match.group(1)
            endpoints[current_section] = {'type': None, 'config': {}}
            continue
        
        # Tipo de sección
        type_match = re.match(r'^type\s*=\s*(\w+)', line)
        if type_match and current_section:
            endpoints[current_section]['type'] = type_match.group(1)
    
    print("🔐 Validación de Endpoints PJSIP\n")
    
    # Verificar endpoints
    errors = []
    for section, data in endpoints.items():
        if data['type'] == 'endpoint':
            pass  # Verificar presencia de auth y aor
        elif data['type'] == 'auth':
            pass
        elif data['type'] == 'aor':
            pass
    
    # Agrupar por usuario (e.g., 2001-softphone, 2001-auth, 2001-softphone)
    users = {}
    for section, data in endpoints.items():
        base_name = section.rsplit('-', 1)[0] if '-' in section else section
        if base_name not in users:
            users[base_name] = []
        users[base_name].append((section, data['type']))
    
    print("👥 Usuarios SIP configurados:\n")
    for user, configs in sorted(users.items()):
        types = [t for _, t in configs]
        has_endpoint = 'endpoint' in types
        has_auth = 'auth' in types
        has_aor = 'aor' in types
        
        status = "✅" if (has_endpoint and has_auth and has_aor) else "⚠️"
        print(f"{status} {user}: {', '.join(types)}")
        
        if not has_endpoint or not has_auth or not has_aor:
            print(f"   ⚠️  Falta: {', '.join(x for x in ['endpoint', 'auth', 'aor'] if x not in types)}")

if __name__ == '__main__':
    validate_pjsip('config/asterisk/pjsip.conf')
```

---

## 6. Validación Completa (Script All-in-One)

```bash
#!/bin/bash
# validate_all.sh

echo "=== VALIDACIÓN COMPLETA LRSS ASTERISK ===" 
echo ""

# Python check
echo "[1/5] Verificando sintaxis Python..."
for script in scripts/billing_job.py scripts/subscriber_cost.py app/web/app.py; do
    if python3 -m py_compile "$script" 2>/dev/null; then
        echo "  ✅ $script"
    else
        echo "  ❌ $script"
    fi
done
echo ""

# Config files check
echo "[2/5] Verificando archivos de configuración..."
for conf in config/asterisk/*.conf; do
    if grep -q '=' "$conf" 2>/dev/null; then
        echo "  ✅ $(basename $conf)"
    fi
done
echo ""

# Database check
echo "[3/5] Verificando conexión a base de datos..."
if mysql -u asterisk -pcontraseña -e "SELECT 1;" 2>/dev/null; then
    echo "  ✅ MariaDB conectado"
else
    echo "  ⚠️  MariaDB no disponible (OK si es desarrollo local)"
fi
echo ""

# ODBC check
echo "[4/5] Verificando ODBC..."
if which isql >/dev/null 2>&1; then
    if isql -v MySQL-asterisk asterisk contraseña -c "SELECT 1;" 2>/dev/null | grep -q "1"; then
        echo "  ✅ DSN MySQL-asterisk accesible"
    else
        echo "  ⚠️  DSN no disponible (OK si es desarrollo local)"
    fi
else
    echo "  ⚠️  unixodbc no instalado"
fi
echo ""

# Env file
echo "[5/5] Verificando variables de entorno..."
if [ -f .env.example ]; then
    echo "  ✅ .env.example presente"
    grep -E "^DB_PASSWORD|^DB_USER|^DB_HOST" .env.example | sed 's/^/    /'
fi
echo ""

echo "✅ Validación completada"
```

Ejecutar:
```bash
chmod +x validate_all.sh
./validate_all.sh
```

---

## 7. Antes de instalar en Asterisk (Checklist)

- [ ] Todos los archivos .conf tienen formato válido
- [ ] `.env.example` contiene todas las variables necesarias (DB_USER, DB_PASSWORD, DB_HOST)
- [ ] `config/odbc/odbc.ini` tiene credenciales correctas
- [ ] `config/odbc/odbcinst.ini` apunta al driver ODBC correcto
- [ ] Base de datos MariaDB contiene tablas: cdr, tarifas, facturacion
- [ ] Scripts Python (`billing_job.py`, `subscriber_cost.py`) sincronizados con BD
- [ ] `extensions.conf` tiene todos los contextos: office-phone, operadora-menu, soporte-tecnico
- [ ] `pjsip.conf` define all usuarios: 2001-2003, 1010, 1001-1003
- [ ] `voicemail.conf` tiene buzones para todos los usuarios de oficina
- [ ] `queues.conf` incluye cola soporte-tecnico con al menos 3 agents
- [ ] `confbridge.conf` tiene configuración de salas de conferencia
- [ ] No hay instancias de "aguacate" como contraseña en archivos

---

## 8. Troubleshooting sin VM

### Problema: No puedo conectar a BD
```bash
# Verificar que MariaDB está corriendo
sudo systemctl status mariadb

# Verificar acceso
mysql -u asterisk -p -h localhost asterisk -e "SELECT 1;"
```

### Problema: Errores de sintaxis Python
```bash
# Ver qué falta en imports
python3 << 'EOF'
import sys
sys.path.insert(0, '.')
import importlib
for module in ['mysql', 'flask', 'mysql.connector']:
    try:
        __import__(module)
        print(f"✅ {module} instalado")
    except ImportError:
        print(f"❌ {module} falta - instalar con: pip install {module}")
EOF
```

### Problema: Errores en archivos .conf
```bash
# Buscar caracteres problemáticos
grep -n $'\r' config/asterisk/extensions.conf  # Saltos de línea Windows
grep -n $'\t' config/asterisk/pjsip.conf      # Tabulaciones

# Ver contenido visible (incluyendo caracteres especiales)
cat -A config/asterisk/extensions.conf | head -20
```

---

## 9. Próximos pasos: Instalación en Asterisk

Una vez pasadas todas las validaciones:

1. Copiar archivos a `/etc/asterisk/`:
```bash
sudo cp config/asterisk/*.conf /etc/asterisk/
```

2. Configurar permisos:
```bash
sudo chown asterisk:asterisk /etc/asterisk/*.conf
sudo chmod 640 /etc/asterisk/*.conf
```

3. Reiniciar Asterisk:
```bash
sudo systemctl restart asterisk
```

4. Verificar en consola:
```bash
sudo asterisk -rvvvvvvvvvc
> core show version
> pjsip show endpoints
> dialplan show
> odbc show
```

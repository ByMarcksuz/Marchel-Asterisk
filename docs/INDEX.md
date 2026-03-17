# 📚 Índice de Documentación - LRSS Asterisk y Tarificación

Guía de referencia rápida para todos los documentos del proyecto.

---

## 📖 DOCUMENTOS DISPONIBLES

### 1. **practica-2-notes.md** ⭐ [LEER PRIMERO]
   - **Contenido:** Guía completa de configuración
   - **Secciones:**
     1. Configuración de Asterisk (usuarios, dialplan, buzón, colas)
     2. Integración con MariaDB (instalación, ODBC, tarifación)
     3. Instalación de archivos en el sistema
   - **Uso:** Referencia técnica principal
   - **Audiencia:** Administradores, desarrolladores

### 2. **STATUS_CHECK.md** 📊 [VERIFICACIÓN RÁPIDA]
   - **Contenido:** Estado de completitud de todos los archivos
   - **Información:**
     - Comparativa antes/después
     - Lista de archivos nuevos creados (6)
     - Checklist de instalación
     - Script bash para instalación completa
   - **Uso:** Verificar que nada falta
   - **Audiencia:** Cualquiera (visual y simple)

### 3. **INVENTORY.md** 📋 [DETALLE COMPLETO]
   - **Contenido:** Inventario detallado de cada archivo
   - **Estructura:**
     - Tabla resumen de 27 archivos
     - Desglose por categoría
     - Instrucciones de instalación
     - Troubleshooting básico
   - **Uso:** Referencia técnica detallada
   - **Audiencia:** Técnicos, integradores

### 4. **TESTING_GUIDE.md** 🧪 [VALIDACIÓN]
   - **Contenido:** Cómo probar sin VM completa
   - **Secciones:**
     1. Validación sintáctica de archivos
     2. Testing de código Python
     3. Validación de base de datos
     4. Análisis del dialplan
     5. Verificación de endpoints PJSIP
     6. Script de validación completa
     7. Troubleshooting
     8. Checklist pre-instalación
   - **Uso:** Validar configuración antes de instalar
   - **Audiencia:** Developers, QA

### 5. **Este documento (INDEX.md)** 🗂️ [ORIENTACIÓN]
   - **Contenido:** Guía de qué leer y en qué orden
   - **Uso:** Punto de entrada principal
   - **Audiencia:** Todos (punto de inicio)

---

## 🚀 FLUJOS DE TRABAJO

### Flujo 1: Verificación Rápida (5 minutos)
```
1. Lee: STATUS_CHECK.md    → ¿Está todo?
2. Verifica: Checklist     → ¿Qué instalar?
3. Actúa: Script bash      → Instala todo
```

### Flujo 2: Implementación Completa (1 hora)
```
1. Lee: practica-2-notes.md          → Entiende arquitectura
2. Revisa: INVENTORY.md              → Conoce cada archivo
3. Valida: TESTING_GUIDE.md          → Prueba sin VM
4. Lee: STATUS_CHECK.md              → Checklist final
5. Ejecuta: Script instalación bash  → Deploy
```

### Flujo 3: Troubleshooting (según error)
```
1. Consulta: TESTING_GUIDE.md        → Sección troubleshooting
2. O revisa: INVENTORY.md            → Sección específica
3. O lee: practica-2-notes.md       → Contexto completo
```

### Flujo 4: Referencias Técnicas (desarrollador)
```
1. practica-2-notes.md              → Detalles técnicos
2. Archivos en config/asterisk/     → Ejemplos reales
3. scripts/tarificar.py             → Código comentado
4. app/web/app.py                   → API Flask
```

---

## 📍 LOCALIZACIÓN DE ARCHIVOS

### Documentación (`/docs`)
```
LRSS-Asterisk/docs/
├── INDEX.md                    ← Estás aquí
├── STATUS_CHECK.md             ← ✅ Estado de archivos
├── INVENTORY.md                ← 📋 Inventario detallado
├── TESTING_GUIDE.md            ← 🧪 Validación
└── legacy/
    └── practica-2-notes.md     ← 📖 Guía técnica
```

### Configuración (`/config`)
```
config/
├── asterisk/                   ← 13 .conf de Asterisk
├── default/asterisk            ← 🆕 Configuración servicio
├── systemd/festival.service    ← 🆕 Servicio Festival
├── festival/                   ← 🆕 Config Festival TTS
└── odbc/                       ← ODBC drivers y DSN
```

### Aplicación (`/app`)
```
app/web/
├── app.py                      ← Flask app
├── templates/                  ← 6 páginas HTML
└── static/                     ← CSS, JS, imágenes
```

### Scripts (`/scripts`)
```
scripts/
├── tarificar.py               ← 🆕 Script tarificación
├── billing_job.py             ← Billing alternativo
└── subscriber_cost.py         ← Cálculo costos
```

---

## 🎯 GUÍA DE LECTURA POR PERFIL

### 👨‍💼 Gestor de Proyecto
```
→ STATUS_CHECK.md (2 min)
  ¿Todo está listo? ✅
→ TESTING_GUIDE.md - sección "Próximos pasos" (3 min)
  ¿Cómo verificar que funciona?
```

### 🔧 Administrador de Sistemas
```
→ practica-2-notes.md - Parte 3 (10 min)
  Instalación de archivos del sistema
→ STATUS_CHECK.md - Checklist (5 min)
  Pasos de instalación
→ INVENTORY.md - Troubleshooting (consultar según sea necesario)
  Resolver problemas
```

### 👨‍💻 Desarrollador
```
→ practica-2-notes.md - Secciones 1-2 (15 min)
  Arquitectura y dialplan
→ TESTING_GUIDE.md (20 min)
  Cómo validar código
→ app/web/app.py (30 min)
  Código de la aplicación
→ scripts/tarificar.py (30 min)
  Lógica de tarificación
```

### 🔬 QA / Tester
```
→ TESTING_GUIDE.md (30 min)
  Plan de validación completo
→ STATUS_CHECK.md - Checklist (5 min)
  Verificación pre-instalación
→ INVENTORY.md - Troubleshooting (según fallos)
  Diagnóstico
```

### 👨‍🎓 Estudiante (primera vez)
```
→ ESTE DOCUMENTO (2 min)
  Conocer la estructura
→ STATUS_CHECK.md (5 min)
  Ver qué se ha hecho
→ practica-2-notes.md - Introducción (10 min)
  Entender la práctica
→ Archivos en config/asterisk/ (30 min)
  Leer ejemplos reales
→ TESTING_GUIDE.md (20 min)
  Validar lo aprendido
```

---

## 📊 MATRICES DE CONTENIDO

### Contenido por Tema

| Tema | practica-2-notes | STATUS_CHECK | INVENTORY | TESTING |
|------|------------------|--------------|-----------|---------|
| Usuarios SIP | ✅ Ejemplos | ✅ Checklist | — | — |
| Dialplan | ✅ Completo | ✅ Checklist | — | ✅ Test |
| BD/ODBC | ✅ Setup | ✅ Checklist | ✅ Detalle | ✅ Validate |
| Festival TTS | ✅ Config | ✅ Checklist | ✅ Detalle | — |
| Tarificación | ✅ SQL | ✅ Checklist | ✅ Paths | ✅ Script |
| Web App | — | ✅ Checklist | ✅ Paths | — |
| Installation | ✅ Parte 3 | ✅ Script | ✅ Detalle | — |
| Validation | — | ✅ Checklist | ✅ Post | ✅ Completo |
| Troubleshooting | — | — | ✅ Sección | ✅ Sección |

### Profundidad por Tema

| Tema | Novato | Intermedio | Avanzado |
|------|--------|-----------|----------|
| Usuarios SIP | STATUS_CHECK | practica-2-notes | config/asterisk/ |
| Dialplan | STATUS_CHECK | practica-2-notes | TESTING_GUIDE |
| ODBC/BD | INVENTORY | practica-2-notes | scripts/tarificar.py |
| TTS Festival | INVENTORY | practica-2-notes | config/festival/ |
| Tarificación | STATUS_CHECK | TESTING_GUIDE | scripts/tarificar.py |
| Web App | STATUS_CHECK | INVENTORY | app/web/app.py |

---

## 🔄 CICLO DE VIDA DEL PROYECTO

### Fase 1: Comprensión (30 min)
```
INDEX.md → STATUS_CHECK.md → practica-2-notes.md (Intro)
```
**Entender qué se hace y por qué**

### Fase 2: Validación (20 min)
```
TESTING_GUIDE.md (Secciones 1-6)
```
**Verificar que todo está bien antes de instalar**

### Fase 3: Instalación (30 min)
```
STATUS_CHECK.md (Script) + practica-2-notes.md (Parte 3)
```
**Copiar archivos y configurar**

### Fase 4: Verificación (10 min)
```
TESTING_GUIDE.md (Sección 9) + STATUS_CHECK.md (Checklist)
```
**Confirmar que funciona**

### Fase 5: Operación (Ongoing)
```
INVENTORY.md (Troubleshooting) + practica-2-notes.md (Referencias)
```
**Mantener y resolver problemas**

---

## 💡 TIPS Y ATAJOS

### Buscar rápidamente
```bash
# En tu editor, usa Ctrl+F (Cmd+F en Mac):

# Si necesitas…                    → Busca en…
# Sintaxis pjsip.conf              → practica-2-notes.md
# Comando instalación              → STATUS_CHECK.md
# Ruta de archivo                  → INVENTORY.md
# Cómo probar ODBC                 → TESTING_GUIDE.md
# Error de Festival                → INVENTORY.md (Troubleshooting)
```

### Comandos rápidos
```bash
# Ver estado de instalación
cat docs/STATUS_CHECK.md | grep -A5 "VERIFICACIÓN RÁPIDA"

# Ver lista de archivos creados
grep "🆕 NUEVO" docs/INVENTORY.md

# Ver checklist de instalación
grep -A20 "CHECKLIST" docs/STATUS_CHECK.md
```

---

## ✅ CHECKLIST: ¿QUÉ DEBO LEER?

- [ ] Este documento (INDEX.md) - orientación general
- [ ] STATUS_CHECK.md - verificar estado rápido
- [ ] practica-2-notes.md - detalles técnicos según necesidad
- [ ] TESTING_GUIDE.md - si vas a validar
- [ ] INVENTORY.md - si necesitas referencia detallada

---

## 📞 REFERENCIAS CRUZADAS

### Dentro de documentos
Cada documento tiene referencias cruzadas:
- `→ Ver TESTING_GUIDE.md` para validar
- `← Ver practica-2-notes.md` para contexto
- `↔️ Ver INVENTORY.md` para detalles

### Estructura proyectos
```
Este documento     STATUS_CHECK.md     INVENTORY.md
      ↓                  ↓                   ↓
  Orientación      Verificación        Detalle
      ↓                  ↓                   ↓
practica-2-notes.md ← TESTING_GUIDE.md
   Técnica              Validación
```

---

## 🎓 APÉNDICES

### A. Lista de Cambios (desde sesión anterior)
- ✅ Reorganizado practica-2-notes.md (Parte 1 y 2)
- ✅ Reemplazadas 7 instancias de "aguacate" → "contraseña"
- 🆕 Creados 6 archivos nuevos
- 🆕 Creadas 3 guías de documentación

### B. Archivos por Primera Vez
1. config/default/asterisk
2. config/systemd/festival.service
3. config/festival/festival.scm
4. config/festival/festival_asterisk.scm
5. scripts/tarificar.py
6. docs/INVENTORY.md (+ STATUS_CHECK.md + este INDEX)

### C. Archivos Mejorados
- practica-2-notes.md (agregada Parte 3)
- config/odbc/odbcinst.ini (mejorada documentación)

---

## 🚀 LISTO PARA EMPEZAR

**Elige tu camino:**

- 🟢 **Rápido (5 min)** → [STATUS_CHECK.md](STATUS_CHECK.md)
- 🟡 **Estándar (1 hora)** → Lee en orden: STATUS → practica-2-notes → TESTING
- 🔴 **Detallado (2+ horas)** → Todos los docs + explorar archivos

---

**Última actualización:** Marzo 2026  
**Estado:** ✅ 27/27 archivos completados  
**Versión:** 1.0 - Completo

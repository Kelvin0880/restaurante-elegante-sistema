# 🍽️ Restaurante Elegante - Sistema de Gestión

Un sistema completo de gestión para restaurante desarrollado con Django 5.2.4, que incluye menú interactivo, carrito de compras, sistema de pedidos y panel administrativo personalizado.

## � Autores del Proyecto
- **Kelvin** 👨‍💻
- **Josmar** 👨‍💻
- **Samuel** 👨‍💻
- **Angela** 👩‍💻

## �📋 Características Principales

- ✅ **Menú Interactivo**: Navegación por categorías con imágenes
- ✅ **Sistema de Usuarios**: Registro, login y perfiles de usuario
- ✅ **Carrito de Compras**: Funcionalidad completa con cálculo de impuestos
- ✅ **Gestión de Pedidos**: Sistema completo de pedidos con estados
- ✅ **Panel Administrativo**: Dashboard personalizado para gestión
- ✅ **Noticias**: Sistema de publicación de noticias
- ✅ **Contacto**: Formulario de contacto integrado
- ✅ **Responsive Design**: Compatible con dispositivos móviles

## 🔧 Requisitos del Sistema

### Software Necesario (Windows)
- **Python 3.8 o superior** - [Descargar Python](https://www.python.org/downloads/windows/)
- **PowerShell** (incluido en Windows 10/11)
- **Navegador Web** (Chrome, Firefox, Edge)

### Verificar Instalación de Python
Abrir **PowerShell** como Administrador y ejecutar:
```powershell
python --version
```
Debe mostrar Python 3.8 o superior.

## 📦 Instalación y Configuración (PowerShell)

### Paso 1: Preparar el Entorno
1. **Extraer el proyecto** a una carpeta (ejemplo: `C:\RestauranteElegante`)
2. **Abrir PowerShell como Administrador**
```

### Paso 2: Configurar Política de Ejecución (Si es necesario)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Paso 3: Crear Entorno Virtual
```powershell
python -m venv venv
```

### Paso 4: Activar Entorno Virtual
```powershell
.\venv\Scripts\Activate.ps1
```
**Nota**: Verás que aparece `(venv)` al inicio de la línea del comando.

### Paso 5: Instalar Dependencias
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Paso 6: Configurar Base de Datos
```powershell
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

### Paso 7: Crear Usuario Administrador
```powershell
.\venv\Scripts\python.exe crear_admin.py
```
**Credenciales del Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`

### Paso 8: Poblar Base de Datos con Datos de Prueba
```powershell
.\venv\Scripts\python.exe populate_data.py
```

### Paso 9: Recopilar Archivos Estáticos
```powershell
.\venv\Scripts\python.exe manage.py collectstatic --noinput
```

### Paso 10: Iniciar Servidor de Desarrollo
```powershell
.\venv\Scripts\python.exe manage.py runserver 8000
```

## 🌐 Acceder al Sistema

Una vez iniciado el servidor, abrir cualquier navegador web y visitar:

### 🖥️ URLs del Sistema
- **🏠 Página Principal**: http://127.0.0.1:8000/
- **⚙️ Panel Admin Personalizado**: http://127.0.0.1:8000/admin-dashboard/
- **🔧 Django Admin**: http://127.0.0.1:8000/admin/

## 👥 Cuentas de Prueba Predefinidas

### 👨‍💼 Administrador
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Acceso**: Panel administrativo completo, gestión de pedidos, contenido

### 👤 Cliente de Prueba
- **Usuario**: `cliente_test`
- **Contraseña**: `test1234`
- **Acceso**: Funcionalidades de cliente (carrito, pedidos, perfil)

## 🚀 Funcionalidades del Sistema

### 👥 Para Usuarios Finales
1. **🍽️ Navegación del Menú**: Ver platos organizados por categorías
2. **🛒 Carrito de Compras**: Agregar/quitar productos con cálculo automático
3. **📝 Realizar Pedidos**: Checkout completo con notas especiales
4. **📋 Historial de Pedidos**: Seguimiento de pedidos realizados
5. **📰 Noticias**: Leer actualizaciones del restaurante
6. **📞 Contacto**: Enviar mensajes al restaurante

### 👨‍💼 Para Administradores
1. **📊 Dashboard**: Estadísticas en tiempo real
2. **📋 Gestión de Pedidos**: Ver, actualizar estados, detalles completos
3. **🔧 Admin Django**: Acceso completo al panel administrativo
4. **📝 Gestión de Contenido**: Platos, categorías, noticias, usuarios

## 🛠️ Solución de Problemas Comunes

### ❌ Error: "No module named 'django'" (Problema más común)
**Causa**: Django no está instalado en el entorno virtual  
**Síntomas**: Aparece el error aunque se vea `(venv)` en PowerShell
**Solución**: Instalar Django específicamente en el entorno virtual
```powershell
# Verificar que el entorno virtual está activo (debe aparecer (venv))
.\venv\Scripts\Activate.ps1

# Instalar dependencias en el entorno virtual
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Verificar que Django funciona
.\venv\Scripts\python.exe -c "import django; print('Django version:', django.get_version())"

# Iniciar servidor usando Python del entorno virtual
.\venv\Scripts\python.exe manage.py runserver 8000
```

### ❌ Error: "Port already in use"
**Solución**: Usar otro puerto
```powershell
.\venv\Scripts\python.exe manage.py runserver 8001
```

### ❌ Error de Política de Ejecución PowerShell
**Causa**: PowerShell bloquea la ejecución de scripts  
**Solución**: Cambiar política temporalmente
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### ❌ Error con Archivos Estáticos
**Solución**: Recopilar archivos estáticos
```powershell
.\venv\Scripts\python.exe manage.py collectstatic --noinput
```

### ❌ Base de Datos Corrupta
**Solución**: Reiniciar base de datos
```powershell
Remove-Item db.sqlite3 -Force
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe crear_admin.py
.\venv\Scripts\python.exe populate_data.py
```

### ❌ Entorno Virtual No Se Activa Correctamente
**Solución**: Usar rutas completas de Python
```powershell
# En lugar de solo "python", usar la ruta completa:
.\venv\Scripts\python.exe manage.py [comando]
```

## 🖥️ Navegadores Compatibles

- ✅ **Google Chrome** (Recomendado)
- ✅ **Mozilla Firefox**
- ✅ **Microsoft Edge**
- ✅ **Safari**

## 🔒 Características de Seguridad

- 🔐 **Contraseñas**: Hasheadas con algoritmos seguros de Django
- 🛡️ **Protección CSRF**: En todos los formularios
- ✅ **Validación**: Entrada de datos validada
- 👥 **Permisos**: Separación clara administrador/usuario

## 🧪 Pruebas del Sistema

### 👤 Flujo Completo de Usuario:
1. Visitar http://127.0.0.1:8000/
2. Crear cuenta nueva o usar `cliente_test` / `test1234`
3. Explorar menú por categorías
4. Agregar productos al carrito
5. Realizar pedido con notas
6. Verificar en "Mis Pedidos"

### 👨‍💼 Flujo de Administrador:
1. Login con `admin` / `admin123`
2. Acceder a Dashboard administrativo
3. Gestionar pedidos (cambiar estados: pendiente → preparando → listo → entregado)
4. Ver detalles completos de pedidos
5. Usar Django admin para gestión avanzada

## 📦 Dependencias del Proyecto

### requirements.txt
```txt
Django==5.2.4
Pillow==10.0.0
```

### Información Técnica
- **Framework**: Django 5.2.4
- **Base de Datos**: SQLite (incluida con Python)
- **Imágenes**: Pillow para procesamiento
- **Arquitectura**: MVT (Model-View-Template)

## 📝 Comandos Útiles PowerShell

### Gestión del Servidor
```powershell
# Iniciar servidor
.\venv\Scripts\python.exe manage.py runserver 8000

# Iniciar en otro puerto
.\venv\Scripts\python.exe manage.py runserver 8001

# Verificar sistema
.\venv\Scripts\python.exe manage.py check
```

### Gestión de Base de Datos
```powershell
# Crear migraciones
.\venv\Scripts\python.exe manage.py makemigrations

# Aplicar migraciones
.\venv\Scripts\python.exe manage.py migrate

# Shell de Django
.\venv\Scripts\python.exe manage.py shell
```

### Gestión de Archivos Estáticos
```powershell
# Recopilar archivos estáticos
.\venv\Scripts\python.exe manage.py collectstatic --noinput

# Limpiar archivos estáticos
Remove-Item -Recurse -Force staticfiles\
```

## 🔄 Reinicio Completo del Proyecto

Si necesitas empezar desde cero:
```powershell
# Detener servidor (Ctrl+C)
# Limpiar archivos generados
Remove-Item db.sqlite3 -Force
Remove-Item -Recurse -Force media\ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force staticfiles\ -ErrorAction SilentlyContinue

# Recrear todo usando Python del entorno virtual
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe crear_admin.py
.\venv\Scripts\python.exe populate_data.py
.\venv\Scripts\python.exe manage.py collectstatic --noinput
.\venv\Scripts\python.exe manage.py runserver 8000
```

## ✅ Lista de Verificación de Instalación

Marcar cada paso completado:

- [ ] ✅ Python 3.8+ instalado
- [ ] ✅ PowerShell abierto como Administrador
- [ ] ✅ Proyecto extraído en carpeta
- [ ] ✅ Entorno virtual creado
- [ ] ✅ Entorno virtual activado `(venv)`
- [ ] ✅ Dependencias instaladas
- [ ] ✅ Migraciones aplicadas
- [ ] ✅ Usuario admin creado
- [ ] ✅ Datos de prueba cargados
- [ ] ✅ Archivos estáticos recopilados
- [ ] ✅ Servidor iniciado
- [ ] ✅ Página principal carga: http://127.0.0.1:8000/
- [ ] ✅ Login admin funciona: `admin` / `admin123`
- [ ] ✅ Dashboard admin accesible: http://127.0.0.1:8000/admin-dashboard/

## 🎯 Funcionalidades Clave Verificadas

- [ ] ✅ **Registro/Login**: Usuarios pueden registrarse e iniciar sesión
- [ ] ✅ **Menú**: Platos se muestran con imágenes y categorías
- [ ] ✅ **Carrito**: Agregar/quitar productos funciona
- [ ] ✅ **Pedidos**: Se pueden realizar y ver historial
- [ ] ✅ **Admin Dashboard**: Panel personalizado funciona
- [ ] ✅ **Gestión Pedidos**: Estados se actualizan correctamente
- [ ] ✅ **Noticias**: Sistema de noticias operativo
- [ ] ✅ **Contacto**: Formulario envía mensajes

## 📞 Soporte y Contacto

**Proyecto Desarrollado por:**
- 👨‍💻 **Kelvin** - Desarrollo Backend y Frontend
- 👨‍💻 **Josmar** - Diseño UI/UX y Frontend  
- 👨‍💻 **Samuel** - Base de Datos y Testing
- 👩‍💻 **Angela** - Gestión de Proyecto y QA

**Tecnologías Utilizadas:**
- 🐍 Python 3.8+
- 🌐 Django 5.2.4
- 🗄️ SQLite
- 🎨 HTML5, CSS3, JavaScript
- 📱 Bootstrap (Responsive)

---

## 🎉 ¡Proyecto Listo para Usar!

El sistema **Restaurante Elegante** está completamente funcional y listo para demostración. Todos los componentes han sido probados y funcionan correctamente.

**Fecha de Entrega:** Julio 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Producción Lista

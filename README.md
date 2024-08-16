# 🏨 Sistema De Reserva de Hotel

Bienvenido al **Sistema de Reservas de Hoteles**. Este proyecto es una aplicación web desarrollada con Django y Django Rest Framework (DRF) para gestionar reservas, habitaciones y estancias en un hotel.

## 📋 Características

- 🔍 **Búsqueda de habitaciones**: Los usuarios pueden buscar y ver la disponibilidad de habitaciones.
- 📅 **Reservas**: Los clientes pueden realizar, editar o cancelar reservas.
- 🏠 **Gestión de estancias**: Administración de las estancias durante la reserva.
- 👤 **Autenticación**: Registro, inicio de sesión y gestión de perfiles de usuario.
- 🛠 **Panel de administración**: Gestión de habitaciones, reservas y usuarios para administradores.
- 🔐 **Seguridad**: Control de acceso basado en roles (Clientes y Administradores).

## 🚀 Tecnologías

- **Lenguaje**: Python 🐍
- **Framework**: Django, Django Rest Framework 🧰
- **Base de datos**: SQLite 🗄️
- **Frontend**: Django Templates con Bootstrap 5 🎨
- **Control de versiones**: Git 📂

## ⚙️ Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/LeXScripterX/Hoctel_Reservaciones.git
cd Hoctel_Reservaciones
```

### 2. Crea y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instala dependencias
```bash
pip install -r requirements.txt
```

### 4. Realizar Migraciones
```bash
python manage.py migrate

```

### 5. Crear un Super Usuario
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

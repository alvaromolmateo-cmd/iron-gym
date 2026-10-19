# Iron Gym

Aplicación web de gestión y reserva de instalaciones deportivas para un centro con varias pistas o espacios.

Proyecto de fin de grado superior de Desarrollo de Aplicaciones Web.

## Idea

Un centro deportivo necesita que sus socios puedan reservar las instalaciones sin llamadas ni papel, y que el personal pueda controlar horarios, bloqueos y ocupación desde un único sitio. Iron Gym cubre las dos partes en la misma aplicación.

## Funcionalidad prevista

### Usuarios

- Registro e inicio de sesión
- Consulta de instalaciones y de sus horarios disponibles
- Creación de reservas
- Gestión de las próximas reservas propias
- Comprobación de disponibilidad para que una misma instalación no se reserve dos veces en el mismo horario

### Administración

- Gestión de instalaciones
- Gestión de horarios
- Gestión de usuarios
- Gestión de reservas
- Bloqueo de franjas por mantenimiento

La interfaz está pensada para móvil y para ordenador.

## Objetivo técnico

Desarrollar una aplicación completa con frontend, backend y base de datos relacional, incluyendo:

- Autenticación
- Permisos distintos según el tipo de usuario
- Validación de datos
- Despliegue

## Ampliaciones si el tiempo lo permite

- Confirmaciones por correo
- Estadísticas de ocupación

## Tecnologías

| Capa | Decisión |
| --- | --- |
| Frontend | HTML, CSS y JavaScript con Vite |
| Backend | Python con Django 5.2 (LTS) |
| API | Django REST Framework |
| Base de datos | SQLite en desarrollo; motor de producción por determinar |

Sobre el backend: se usa Django porque es lo que se trabaja este curso en clase y trae de serie el ORM, la autenticación y el panel de administración. Se ha elegido la versión 5.2 por ser la última LTS (soporte hasta abril de 2028). El razonamiento completo está en la propuesta del Hito 0.

El frontend usa Vite sin framework (plantilla *vanilla*): sigue siendo HTML, CSS y JavaScript, pero con servidor de desarrollo con recarga automática y variables de entorno.

## Estructura del repositorio

```
iron-gym/
├── backend/            Proyecto Django (config/ = ajustes, core/ = app principal)
├── frontend/           Proyecto Vite (HTML, CSS y JavaScript)
├── docs/               Documentación técnica
├── .vscode/launch.json Configuración para arrancar con F5 en VS Code
├── .env.example        Variables de entorno necesarias (sin secretos)
├── docker-compose.yml  Arranque opcional con Docker
└── README.md
```

## Puesta en marcha en local

Requisitos: **Git**, **Python 3.12 o superior** y **Node.js 20.19 o superior** (con npm).

Los comandos se ejecutan desde la raíz del repositorio salvo que se indique otra cosa. Cuando cambian entre Windows y Linux/macOS, aparecen los dos.

### 1. Clonar el repositorio

```bash
git clone https://github.com/alvaromolmateo-cmd/iron-gym.git
cd iron-gym
```

### 2. Configurar las variables de entorno

```bash
cp .env.example .env
```

| Variable | Qué poner |
| --- | --- |
| `DJANGO_SECRET_KEY` | Una clave aleatoria. Genérala con `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DJANGO_DEBUG` | `True` en local |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` en local |
| `CORS_ALLOWED_ORIGINS` | URL del frontend: `http://localhost:5173,http://127.0.0.1:5173` |
| `VITE_API_URL` | URL de la API: `http://localhost:8000/api` |

Con los valores de ejemplo ya funciona en local; solo conviene cambiar `DJANGO_SECRET_KEY`.

### 3. Instalar las dependencias

Backend (con un entorno virtual de Python):

```bash
cd backend
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate
pip install -r requirements.txt
cd ..
```

Frontend:

```bash
cd frontend
npm install
cd ..
```

### 4. Preparar la base de datos

En desarrollo se usa SQLite, así que no hay que instalar nada: el archivo `backend/db.sqlite3` se crea al migrar. Con el entorno virtual activado:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser   # opcional, para entrar en /admin
```

Por ahora no hay *seeders*.

### 5. Arrancar el backend

Con el entorno virtual activado y desde `backend/`:

```bash
python manage.py runserver
```

Queda disponible en **http://localhost:8000** (API en `/api/` y administración en `/admin/`).

### 6. Arrancar el frontend

En otra terminal, desde `frontend/`:

```bash
npm run dev
```

Queda disponible en **http://localhost:5173**.

### 7. Comprobar que funciona

- Abre **http://localhost:8000/api/health**. Debe devolver un JSON con `"status": "ok"`.
- Abre **http://localhost:5173**. Debe aparecer *Backend conectado: ok* junto a la respuesta del endpoint. Eso demuestra que el frontend y el backend se comunican.

### Arrancar con F5 en VS Code

En `.vscode/launch.json` hay tres configuraciones (pestaña *Ejecución y depuración*):

- **Backend: Django (runserver)**: arranca Django con el depurador. Usa el intérprete de `backend/.venv`, así que antes hay que completar el paso 3.
- **Frontend: Vite (npm run dev)**: arranca el servidor de Vite.
- **Iron Gym: Backend + Frontend**: arranca los dos a la vez.

Hace falta la extensión *Python Debugger* (debugpy) de Microsoft.

## Arranque con Docker (opcional)

Con Docker Desktop en marcha y el `.env` creado (paso 2):

```bash
docker compose up --build
```

Levanta el backend en http://localhost:8000 (aplica las migraciones al arrancar) y el frontend en http://localhost:5173. La base de datos SQLite se guarda en el volumen `backend-data`. Para pararlo, usa `docker compose down`.

## Documentación

- [Instalación y configuración del entorno](docs/instalacion.md)

## Estado

Hito 1: estructura base (*boilerplate*) del backend y del frontend, comunicados mediante `/api/health`. También están definidos los modelos principales (`Usuario`, `Instalacion`, `Horario`, `Reserva` y `Bloqueo`) y registrados en el panel de administración.

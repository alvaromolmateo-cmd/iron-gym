# Instalación y configuración del entorno

Este documento recoge los pasos seguidos para crear la estructura base de Iron Gym (Hito 1), las pruebas de funcionamiento y los problemas encontrados.

## Entorno utilizado

| Herramienta | Versión |
| --- | --- |
| Sistema operativo | Windows 11 |
| Python | 3.13 |
| Django | 5.2 (LTS) |
| Django REST Framework | 3.18 |
| Node.js | 24 |
| Vite | 8 |
| Editor | Visual Studio Code |

## Backend (Django)

1. Se crea la carpeta `backend/` y, dentro, un entorno virtual para aislar las dependencias del proyecto:

   ```bash
   python -m venv .venv
   ```

2. Se instala Django. Siguiendo el criterio de la UD3, se elige la **última versión LTS (5.2)**. Tiene soporte hasta abril de 2028 y es más compatible con paquetes de terceros que la última versión no LTS:

   ```bash
   pip install "Django>=5.2,<5.3"
   ```

   Se fija la rama 5.2 en lugar de `Django==5.2` exacto para recibir los parches de seguridad de esa versión.

3. Se instalan las dependencias para la API y la configuración:

   - `djangorestframework`: para construir la API REST.
   - `django-cors-headers`: para que el frontend, que va en otro puerto, pueda llamar a la API.
   - `python-dotenv`: para leer la configuración desde `.env`.

4. Se guardan las dependencias:

   ```bash
   pip freeze > requirements.txt
   ```

5. Se crea el proyecto y la aplicación principal:

   ```bash
   django-admin startproject config .
   python manage.py startapp core
   ```

   El proyecto se llama `config` porque solo contiene la configuración. La lógica va en la app `core`.

6. Cambios en `config/settings.py`:
   - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y `CORS_ALLOWED_ORIGINS` se leen de variables de entorno.
   - Se añaden `rest_framework`, `corsheaders` y `core` a `INSTALLED_APPS`, y `CorsMiddleware` a `MIDDLEWARE`.
   - Idioma `es-es` y zona horaria `Europe/Madrid`.
   - `AUTH_USER_MODEL = 'core.Usuario'`: usuario propio con rol (socio o administrador). Se define **antes de la primera migración**, porque cambiarlo después es muy costoso.

7. Se definen los modelos principales en `core/models.py` y se registran en `core/admin.py`:

   | Modelo | Para qué sirve |
   | --- | --- |
   | `Usuario` | Socios y administradores (extiende `AbstractUser`) |
   | `Instalacion` | Pistas, salas y otros espacios reservables |
   | `Horario` | Horario de apertura por instalación y día de la semana, dividido en franjas |
   | `Reserva` | Reserva de una franja; impide dos reservas confirmadas que se solapen |
   | `Bloqueo` | Periodos sin reservas por mantenimiento |

8. Se crean y aplican las migraciones:

   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   ```

9. Se crea el endpoint de prueba `GET /api/health` en `core/views.py`. Devuelve el estado del servicio y comprueba la conexión con la base de datos.

## Frontend (Vite)

1. Se genera el proyecto con la plantilla *vanilla* (HTML, CSS y JavaScript sin framework):

   ```bash
   npm create vite@latest frontend -- --template vanilla
   cd frontend
   npm install
   ```

2. Se quita el contenido de ejemplo de la plantilla. `src/main.js` pasa a ser una página que llama a `${VITE_API_URL}/health` y muestra la respuesta.

3. En `vite.config.js` se configura `envDir: '..'` para que el frontend use el mismo `.env` de la raíz que el backend.

## Variables de entorno

Se usa un único `.env` en la raíz, creado a partir de `.env.example`. Django lo carga con `python-dotenv` y Vite solo expone las variables que empiezan por `VITE_`. El `.env` está en `.gitignore`.

## Docker (opcional)

- `backend/Dockerfile`: imagen `python:3.13-slim`. Aplica las migraciones y arranca `runserver` en `0.0.0.0:8000`.
- `frontend/Dockerfile`: imagen `node:24-alpine` con `npm run dev`.
- `docker-compose.yml`: levanta los dos servicios. La base de datos SQLite se guarda en un volumen.

## Pruebas de funcionamiento

> Pendiente: añadir las capturas en `docs/capturas/` con los nombres de abajo.

### Backend

`http://localhost:8000/api/health` devuelve:

```json
{"status": "ok", "servicio": "Iron Gym API", "base_de_datos": "sqlite", "hora": "..."}
```

![Backend: /api/health](capturas/backend-health.png)

### Panel de administración

![Panel de administración con los modelos](capturas/admin.png)

### Frontend y comunicación con el backend

`http://localhost:5173` muestra *Backend conectado: ok* junto con la respuesta JSON del endpoint.

![Frontend mostrando la respuesta del backend](capturas/frontend-health.png)

## Problemas encontrados y soluciones

| Problema | Solución |
| --- | --- |
| El frontend (puerto 5173) no podía llamar a la API (puerto 8000) por la política de CORS del navegador. | Se instala `django-cors-headers` y se permiten los orígenes del frontend en `CORS_ALLOWED_ORIGINS`. |
| La `SECRET_KEY` generada por Django puede contener `$`, y Docker Compose lo interpreta como una variable dentro del `.env`. | Se genera la clave con `secrets.token_urlsafe(50)`, que no incluye `$`. |
| `/api/health` y `/api/health/` se trataban como rutas distintas. | La ruta se define con `re_path(r"^health/?$")` para aceptar las dos formas. |
| Cambiar el modelo de usuario cuando ya hay migraciones obliga a rehacer la base de datos. | Se define `AUTH_USER_MODEL` desde el principio, antes de la primera migración. |

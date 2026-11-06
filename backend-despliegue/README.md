# Backend de despliegue - Iron Gym

API de la actividad Backend 2, creada con Laravel 13 y PHP 8.4 dentro de Docker.
El proyecto está aislado en `backend-despliegue`; no necesita el backend anterior.

## Arranque con VS Code

1. Instala Git, Docker Desktop y VS Code con la extensión Dev Containers.
2. Arranca Docker Desktop y abre la raíz del repositorio en VS Code.
3. Ejecuta **Dev Containers: Reopen in Container** desde la paleta de comandos.
4. En la terminal del contenedor ejecuta:

```bash
cd backend-despliegue
composer install
cp .env.example .env
php artisan key:generate
touch database/database.sqlite
php artisan migrate
php artisan serve --host=0.0.0.0 --port=8000
```

Estos comandos de preparación son para un clon nuevo. Si ya tienes `.env`, consérvalo
junto con su `APP_KEY`. Para posteriores arranques basta con iniciar el servidor.
Abre http://localhost:8000/api/hello. La página de bienvenida está en `/`.
No hace falta instalar PHP ni Composer en Windows, ni compilar assets para esta API.

La configuración `.devcontainer/devcontainer.json` está en la raíz y también sirve
para la siguiente actividad de frontend. Usa un volumen Docker para `vendor`:
la extracción de dependencias sobre una carpeta Windows superó el timeout de Composer.
El código permanece en el repositorio y las dependencias se regeneran con `composer install`.

### Contenedor de comprobación de este equipo

El puerto 8000 ya estaba ocupado por WordPress, por lo que se dejó Laravel en:

http://localhost:18000/api/hello?name=Ana

El contenedor se llama `iron-gym-laravel-despliegue` y solo monta esta carpeta.
Para volver a arrancarlo desde PowerShell:

```powershell
docker start iron-gym-laravel-despliegue
docker exec -d iron-gym-laravel-despliegue php artisan serve --host=0.0.0.0 --port=8000
```

Ejecuta el segundo comando solo si el servidor aún no está iniciado.
Para pararlo: `docker stop iron-gym-laravel-despliegue`.
Si usas VS Code y el 8000 local sigue ocupado, consulta el puerto asignado en la pestaña
**Puertos** o cambia su puerto local. No hace falta parar WordPress.

## Contrato de la API

| Petición | Respuesta (200, application/json) |
| --- | --- |
| `GET /api/hello` | `{"message":"Hello World"}` |
| `GET /api/hello?name=Ana` | `{"message":"Hello World Ana"}` |
| `GET /api/hello?name=` | `{"message":"Hello World"}` |

Se eliminan los espacios al principio y al final del nombre. Se admiten acentos.
La ruta usa `HelloController@index` y es pública. `/api/user` conserva la protección
`auth:sanctum` instalada con `php artisan install:api`.

## CORS

En `.env` y en su plantilla `.env.example`:

```dotenv
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Los orígenes se separan por comas sin espacios. Después de cambiar esta variable:

```bash
php artisan config:clear
```

Al desplegar, sustituye los orígenes por los dominios reales del frontend, incluyendo
su protocolo. Un origen no autorizado sigue recibiendo HTTP 200, pero sin
`Access-Control-Allow-Origin`: es el navegador quien impide que JavaScript lea la respuesta.
CORS no sustituye a la autenticación.

## Pruebas

Dentro del contenedor, desde `backend-despliegue`:

```bash
php artisan route:list --path=api
php artisan test --compact
```

También puedes abrir `peticiones.http` con REST Client y pulsar **Send Request**.
Cambia `@baseUrl` a `http://localhost:18000` para el contenedor de comprobación.

```bash
curl http://localhost:8000/api/hello
curl 'http://localhost:8000/api/hello?name=Ana'
curl 'http://localhost:8000/api/hello?name=Ana%20Garc%C3%ADa'
curl 'http://localhost:8000/api/hello?name='
curl -i -H 'Origin: http://localhost:5173' http://localhost:8000/api/hello
curl -i -H 'Origin: http://web-maliciosa.com' http://localhost:8000/api/hello
curl -i -X OPTIONS -H 'Origin: http://localhost:5173' -H 'Access-Control-Request-Method: GET' http://localhost:8000/api/hello
```

En PowerShell usa `curl.exe`. Los tests comprueban el contrato, espacios, acentos,
ambos orígenes permitidos, origen denegado, preflight, prefijo API y la ruta protegida.
Validación realizada: 15 tests correctos, 48 aserciones, formato PHP comprobado con Pint
y peticiones HTTP al servidor Docker.

## Explicación de los checkpoints

- PHP está instalado en el contenedor. `forwardPorts` permite acceder desde el ordenador
  al puerto del servidor del contenedor. Un compañero necesita Git, Docker Desktop,
  VS Code y Dev Containers, además de instalar las dependencias del proyecto.
- La API responde con estado 200 y `Content-Type: application/json`. `/hello` devuelve
  404 porque las rutas de `routes/api.php` se registran con el prefijo `/api`.
  Para traducir el saludo habría que cambiar las cadenas del controlador y los tests;
  esta actividad mantiene `Hello World` porque forma parte del contrato obligatorio.
- `curl` no aplica CORS. El navegador sí. En producción se configura el origen real del
  frontend. Usar `*` permitiría a cualquier web leer respuestas públicas sin credenciales;
  no concede por sí mismo autenticación ni evita controles de acceso.

## Qué hace cada parte

- `app`: controladores, modelos y lógica de la aplicación.
- `bootstrap`: arranque y registro de rutas y middleware.
- `config`: configuración, incluyendo CORS y Sanctum.
- `routes`: definición de rutas web y API.
- `database`: migraciones, factories y seeders; SQLite local se excluye de Git.
- `vendor`: dependencias de Composer, excluidas de Git.
- `.env`: configuración local y secretos; no se sube.
- `.env.example`: plantilla compartida, sin claves reales.

`query('name')` lee la query string; `input('name')` también puede leer el cuerpo de
la petición. El controlador convierte el valor a cadena y aplica `trim` para tratar
un nombre vacío o compuesto solo por espacios como un saludo sin nombre.
`--host=0.0.0.0` hace que el servidor escuche conexiones que llegan desde fuera del contenedor.

`install:api` instala Sanctum, registra `routes/api.php` y añade la migración de tokens.
El saludo no necesita autenticación. El trait `HasApiTokens` se necesitaría para emitir tokens.
Una petición preflight es un `OPTIONS` con el que el navegador consulta los permisos
antes de determinadas peticiones entre orígenes distintos (protocolo, host o puerto).

`composer install` respeta las versiones de `composer.lock`; `composer update` vuelve
a resolverlas y actualiza ese fichero. Se versiona el lock para reproducir la instalación.
Laravel Boost se incluye como dependencia de desarrollo siguiendo el `AGENTS.md` de la plantilla.

Los commits separan entorno, ajuste para Windows, proyecto base, API, CORS y pruebas.
Se usa Conventional Commits (`chore`, `fix`, `feat`, `test`, `docs`) para indicar la finalidad.
Se conserva la rama `develop` del proyecto; no se renombra a `main` ni se modifica el README raíz.

Se han incluido los extras de tests y documentación. La validación de 50 caracteres
y la implementación alternativa en Express/FastAPI quedan como retos opcionales del PDF.

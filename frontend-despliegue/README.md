# Frontend 2 — Iron Gym

Vue 3 + Vite + Vue Router, con Carbon White según DESIGN.md.

## Arranque

Reconstruye el dev container con **Dev Containers: Rebuild Container** para
instalar Node.js LTS y habilitar el puerto 5173. Comprueba node -v, npm -v y php -v.

Terminal 1 (desde la raíz del repositorio):

```sh
cd backend-despliegue
php artisan serve --host=0.0.0.0 --port=8000
```

Terminal 2 (desde la raíz del repositorio):

```sh
cd frontend-despliegue
npm ci
npm run dev
```

Abre http://localhost:5173 para coincidir con CORS. Vite falla si el puerto está
ocupado. La URL está en `.env.development`; reinicia Vite si la cambias.
Para producción configura VITE_API_URL durante la compilación o mediante
`.env.production.local`. Las variables VITE_ son públicas: no pongas secretos.
El servidor de producción debe devolver index.html para las rutas de la SPA.

## Estructura

- src/main.js inicia Vue, router y estilos.
- src/App.vue contiene cabecera, navegación, contenido y pie.
- src/router/index.js define / y /hello, con carga diferida de Hello.
- src/views contiene las páginas y el estado del formulario.
- src/components/HelloResult.vue muestra los cuatro estados.
- src/services/helloService.js aísla HTTP y valida la respuesta.
- src/assets contiene los tokens Carbon y los estilos adaptables.
- boceto.html conserva la simulación original de Interfaces 2.

## Verificación

```sh
npm test
npm run build
```

Las pruebas simulan fetch; no sustituyen la comprobación con Laravel activo.

1. Navega entre Inicio y Hello y abre /hello directamente.
2. Saluda sin nombre: Hello World.
3. Prueba Ana, Ana García y Ana & Luis; deben conservarse los caracteres.
4. Con red lenta comprueba Cargando y el botón deshabilitado.
5. Detén Laravel, saluda y comprueba el error. Arráncalo y reintenta.
6. Navega con Tab y Enter y comprueba foco, etiqueta y anuncio del resultado.
7. Revisa en móvil: formulario y resultado se apilan.

## Conceptos

El servicio separa HTTP de la presentación y permite probarlo sin montar Vue.
async/await espera promesas; URL.searchParams codifica tildes y & correctamente.
ref mantiene estado reactivo, v-model sincroniza el campo y @submit.prevent evita
la recarga. finally restaura el botón tanto en éxito como en error. Las variables
CSS centralizan el diseño. Vue Router cambia las vistas sin recargar la SPA;
la carga diferida descarga Hello cuando se visita. Las features instalan herramientas
de forma reproducible al reconstruir el contenedor.

## Entrega

Revisa el diff y crea commits separados para .devcontainer y frontend-despliegue,
y después sube la rama al remoto. node_modules, dist y archivos locales se ignoran.

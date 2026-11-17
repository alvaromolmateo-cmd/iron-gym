# Iron Gym

## Descripción

Iron Gym será una aplicación web para gestionar las reservas de un centro deportivo.
Resolverá la organización manual de la disponibilidad de pistas y salas.
Los socios podrán consultar las instalaciones y los horarios disponibles.
Podrán realizar y consultar sus reservas desde la web.
El personal del centro gestionará las instalaciones, los horarios y los socios.
También podrá bloquear horarios cuando una instalación no esté disponible.
El objetivo será centralizar la información y evitar reservas incompatibles.

## Tecnologías

### Guía de estilo / diseño

Se utilizará un diseño propio con HTML semántico y CSS adaptable a móviles y escritorio. Esto permitirá practicar los contenidos de Interfaces y ajustar formularios, navegación y estados de disponibilidad a las necesidades del centro, manteniendo colores, tipografía y espaciados coherentes.

### Backend

Python con Django 5.2 LTS, por ser el framework trabajado en el módulo de Servidor. Su ORM, migraciones, autenticación y panel de administración facilitan la gestión de datos y usuarios. Se elige una versión LTS para disponer de una base con soporte prolongado.

### Frontend

HTML, CSS y JavaScript con Vite. JavaScript permitirá consultar el backend y actualizar la interfaz; Vite proporcionará el servidor de desarrollo y la compilación de recursos. Para el alcance inicial no se necesita un framework adicional de componentes.

### Base de datos

SQLite como motor relacional inicial. Socios, instalaciones, horarios y reservas tienen relaciones claras y necesitan restricciones de integridad. SQLite se integra con Django y permite trabajar en local sin instalar un servidor de base de datos independiente.

### Documentación

Markdown dentro del repositorio, con el README como punto de entrada. Permite mantener las explicaciones y decisiones junto al código, revisar sus cambios con Git y leerlas directamente en GitHub. En hitos posteriores se añadirá la documentación técnica en docs/.

### Librerías y dependencias

- Autenticación, validación, ORM y migraciones de Django: cubren las necesidades iniciales aprovechando las herramientas del framework.
- Sistema de pruebas de Django: permitirá comprobar las reglas de reservas y las respuestas del backend.
- django-cors-headers: permitirá la comunicación del frontend con el backend cuando se ejecuten en orígenes distintos durante el desarrollo.
- python-dotenv: facilitará cargar la configuración local desde variables de entorno sin incluir secretos en Git.
- Vite: gestionará el desarrollo y la construcción del frontend.

### Control de versiones

Se usará Git con GitHub para conservar el historial y facilitar la revisión del profesor. El acceso al remoto será por HTTPS, compatible con la red WIFI_EDU.

La rama principal será main y develop se usará para integrar el trabajo. Las tareas se desarrollarán en ramas feature/nombre y se integrarán mediante revisión. Los commits serán pequeños y descriptivos, con prefijos como docs:, feat: y fix: para indicar su propósito.

Si el repositorio es privado, se dará acceso al profesor como colaborador.

## Estado y entrega del Hito 0

Este hito contiene la definición del proyecto y sus tecnologías. La estructura ejecutable y la conexión entre frontend y backend se realizarán en el Hito 1.

Repositorio: https://github.com/alvaromolmateo-cmd/iron-gym

Para entregar, hay que confirmar y subir este README al repositorio y enviar el enlace por el canal indicado por el profesor.

Enunciado: https://github.com/jpaniorte/2daw-daw-2627/blob/main/proyectos/pdf/hito0.pdf

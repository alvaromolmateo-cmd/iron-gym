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
| Frontend | HTML, CSS y JavaScript |
| Backend | Python, a decidir entre Django y FastAPI |
| Base de datos | Relacional, motor por determinar |

Sobre el backend – Django es la opción más probable, porque es lo que se va a trabajar este curso en clase y trae de serie el ORM, la autenticación y el panel de administración.

## Estado

Fase inicial. Por ahora solo está definida la propuesta.

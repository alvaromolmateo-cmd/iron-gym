# Iron Gym — Entrega UD4 de Servidor

Aplicación Django con las apps `billing`, `core` y `common`. Esta entrega incluye
el código, las plantillas, las migraciones y las pruebas de la actividad UD4.

## Preparación y arranque

Requisito: Python 3.13. Desde la carpeta `backend` descomprimida, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

En Linux o macOS, sustituir `.\.venv\Scripts\python.exe` por `.venv/bin/python`.
Abrir http://127.0.0.1:8000/. El administrador está en `/admin/`.

La base de datos no se incluye: `migrate` crea una nueva y carga los catálogos
de tipos de perfil, tipos de instalación, estados de reserva y días de la semana.
No se incluyen usuarios, contraseñas ni registros de la base de datos local.
El superusuario creado permite entrar al administrador y se puede seleccionar
en los formularios que necesitan un usuario.

## Recorrido de comprobación

Los formularios se pueden abrir directamente:

- `/cliente_create/`, `/factura_create/`, `/cobro_create/`.
- `/perfil_create/`, `/instalacion_create/`, `/horario_create/`.
- `/reserva_create/`, `/bloqueo_create/`.

Crear primero un cliente y una factura antes de registrar sus cobros.
Crear primero una instalación antes de registrar horarios, reservas o bloqueos.
Tras guardar se abre la pantalla de actualización. Su botón Eliminar lleva a
la confirmación de borrado. Las rutas de edición y borrado incluyen el id:
por ejemplo, `/cliente_update/1/` y `/cliente_delete/1/`.

Los listados admiten `?ordering=asc` y `?ordering=desc`, por ejemplo:
`/instalacion_list/?ordering=desc`.

## Correspondencia con los apartados

| Apartado | Archivos principales |
| --- | --- |
| UD4.1 | Comentarios identificativos y `billing/tests.py`, `core/tests.py` |
| UD4.2a | `billing/views.py`, `core/views.py` |
| UD4.2b | `irongym/urls.py` |
| UD4.2c–f | `common/mixins.py`, `templates/base_create_update.html`, `templates/base_confirm_delete.html` |
| UD4.2g | `billing/mixins.py` |
| UD4.2h | `core/mixins.py` |
| UD4.2i | `common/mixins.py`, `templates/common/pagination.html` |
| UD4.3a–c | `billing/forms.py`, `core/forms.py` |
| UD4.4a | `common/mixins.py`, vistas, configuración y `templates/common/messages.html` |
| UD4.4b | `requirements.txt`, `irongym/settings.py`, plantilla de formulario |
| UD4.4c–e | Helpers y layouts en los dos archivos `forms.py` |

Hay ocho clases ModelForm, una por pareja CreateView–UpdateView, utilizadas
por las dieciséis vistas de creación y actualización.

## Pruebas

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test billing core
```

Las 16 pruebas usan una base de datos temporal independiente. Comprueban las
vistas, los importes, los intervalos, la ordenación, los mensajes, el borrado
protegido y los formularios Crispy. El aspecto visual se revisa en el navegador.
Bootstrap se carga mediante CDN y necesita conexión a Internet para sus estilos.

## Contenido de la entrega

No se incluyen entornos virtuales, `.git`, cachés, dependencias instaladas,
estáticos recopilados ni la base de datos local. Los estáticos del administrador
los proporciona Django en desarrollo. La configuración es de desarrollo.

El documento de actividades y la autoevaluación se entregan por separado con
los textos y tablas completados por el alumno.

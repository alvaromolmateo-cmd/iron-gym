# Interfaces 2 — Iron Gym

Material preparatorio de diseño para la actividad Frontend 2.

- `DESIGN.md`: comparación Carbon/Fluent, guía elegida, tokens y fuentes oficiales.
- `index.html`: boceto interactivo de Inicio y Hello, con los cuatro estados.
- `REVISION.md`: correcciones, comprobaciones y límites de la revisión.

## Abrir el boceto

Abre `index.html` directamente en tu navegador. No requiere npm, compilación ni backend.
Opcionalmente, desde la raíz del repositorio:

```powershell
python -m http.server 5173 --bind 127.0.0.1 --directory frontend-despliegue
```

Después abre http://127.0.0.1:5173. Detén el servidor con Ctrl+C.
IBM Plex Sans se carga desde Google Fonts; sin internet se usa Arial como alternativa.

## Probar

Navega entre Inicio y Hello. Envía el formulario sin nombre o con «Ana».
El boceto simula una espera breve y muestra `Hello World` o `Hello World Ana`.
Los botones de la galería muestran cada estado; la vista previa de carga permanece
visible hasta seleccionar otro estado. Desde error puedes pulsar Saludar otra vez.

La galería es material de revisión, no un elemento previsto para el producto final.
La integración real con `/api/hello` se realizará en la actividad Frontend 2.
Se ha conservado la rama `develop`, con commits separados para guía, boceto y revisión.

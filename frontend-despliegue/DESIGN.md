# DESIGN.md — Iron Gym / Hello

Ficha de trabajo de Actividades Interfaces 2. Consulta de fuentes: 6 de noviembre de 2026.
El boceto es `index.html`: HTML, CSS y JavaScript sin dependencias de ejecución.
Simula las respuestas; la conexión real a la API corresponde a Frontend 2.

## Guía elegida

- **Carbon Design System, tema White**, de IBM.
- Fuente: https://www.carbondesignsystem.com/
- Motivo: jerarquía clara, componentes sobrios y tokens verificables. Una pequeña
  herramienta de saludo permite practicar formularios y feedback sin decoración innecesaria.
- Alcance: interpretación en HTML de los tokens y patrones seleccionados, no uso de
  la librería oficial ni certificación de conformidad con todo Carbon.

## Exploración: Carbon y Fluent 2

| Aspecto | Carbon | Fluent 2 |
| --- | --- | --- |
| Color | Temas y roles semánticos; aquí se selecciona White y azul para la acción | Paletas neutrales, compartidas y de marca |
| Tipografía | IBM Plex; bases productiva de 14 px y expresiva de 16 px | Segoe UI y alternativas nativas; Body 1 web de 14/20 px |
| Botones | Geometría rectangular, texto en estilo oración y estados definidos | Esquinas redondeadas según componente; variantes para acciones |
| Espaciado | Escala con incrementos de 2, 4 y 8 px | Unidad base de 4 px |
| Campos | Etiqueta externa, superficie de campo y borde inferior | Etiqueta persistente; el placeholder no reemplaza instrucciones esenciales |
| Accesibilidad | Foco contrastado y estados distinguibles | Jerarquía legible y pautas de teclado y etiquetado |
| Encaje propuesto | Herramientas de datos y gestión | Herramientas de productividad y colaboración |

La última fila es una valoración para este proyecto, no una restricción de las guías.
Fuentes consultadas: [Carbon color](https://www.carbondesignsystem.com/building-blocks/foundations/color/tokens),
[tipografía](https://www.carbondesignsystem.com/building-blocks/foundations/typography/type-sets),
[botones](https://www.carbondesignsystem.com/building-blocks/core/components/button/specifications),
[campos](https://www.carbondesignsystem.com/building-blocks/core/components/text-input/specifications),
[espaciado](https://www.carbondesignsystem.com/building-blocks/foundations/spacing/overview);
[Fluent color](https://fluent2.microsoft.design/color),
[tipografía](https://fluent2.microsoft.design/typography), [forma](https://fluent2.microsoft.design/shapes),
[layout](https://fluent2.microsoft.design/layout),
[botón](https://fluent2.microsoft.design/components/web/react/core/button/usage),
[input](https://fluent2.microsoft.design/components/web/react/core/input/usage).

### Datos contrastados

1. Carbon White usa `#0f62fe` para `$button-primary`, no un azul elegido a ojo.
2. Fluent Body 1 web es 14 px con interlineado 20 px; no se presupone 16 px universal.
3. Carbon no tiene una escala exclusivamente de 8 px: incluye 2 y 4 px.
4. El input Carbon usa borde inferior; no se sustituye por un campo redondeado genérico.

## Colores (design tokens)

Los nombres CSS son alias locales. Los valores proceden de la tabla oficial
[Carbon, tema White](https://www.carbondesignsystem.com/building-blocks/foundations/color/tokens).

| Token CSS | Valor | Token Carbon | Uso |
| --- | --- | --- | --- |
| color-primary | #0f62fe | button-primary | Acción principal |
| color-primary-hover | #0050e6 | button-primary-hover | Hover |
| color-primary-active | #002d9c | button-primary-active | Pulsación |
| color-on-primary | #ffffff | text-on-color | Texto de botón |
| color-surface | #ffffff | background | Página |
| color-layer | #f4f4f4 | layer-01 | Paneles |
| color-on-surface | #161616 | text-primary | Texto |
| color-secondary | #525252 | text-secondary | Ayuda |
| color-error | #da1e28 | text-error | Error |
| color-success | #198038 | support-success | Icono de éxito |
| color-border | #8d8d8d | border-strong-01 | Campo |
| color-divider | #e0e0e0 | border-subtle-01 | Separadores |
| color-disabled | #c6c6c6 | button-disabled | Botón inactivo |
| color-on-disabled | #8d8d8d | text-on-color-disabled | Etiqueta inactiva |
| color-focus | #0f62fe | focus | Foco |

## Tipografía

- Familia: IBM Plex Sans, con fallback `Arial, sans-serif`.
- El boceto carga IBM Plex Sans desde Google Fonts; sin conexión funciona con fallback.
- Cuerpo: 16/24 px, peso 400, selección de la escala expresiva de Carbon.
- Título de página: 42/50 px, peso 300; en móvil 32/40 px.
- Títulos de sección: 20/28 px, peso 400. Etiquetas y botones: 14/18 px, peso 400.
- Pesos utilizados: 300, 400 y 600. Metadatos: 12/16 px.
- Fuente: [type sets](https://www.carbondesignsystem.com/building-blocks/foundations/typography/type-sets).
  La asignación de cada estilo a esta pantalla y el cambio móvil son decisiones locales.

## Espaciado y forma

- Base práctica: 4 px; escala usada: 4, 8, 16, 24, 32, 48, 64 y 96 px.
- s = 8 px, m = 16 px, l = 32 px. Radio de botones y campos: 0.
- Campo de 48 px y botón principal de 48 px; separación cómoda para teclado y tacto.
- Contenedor máximo de 1200 px; dos columnas en escritorio y una en móvil.
- Escala: [Carbon spacing](https://www.carbondesignsystem.com/building-blocks/foundations/spacing/overview).
  Ancho, composición y breakpoint de 720 px son decisiones del boceto.

## Componentes

- **Navegación:** Inicio y Hello, página activa subrayada y `aria-current="page"`.
- **Botón principal:** rectangular azul, etiqueta «Saludar», sin mayúsculas forzadas;
  hover azul, active azul oscuro; deshabilitado gris durante la espera. Foco con
  contorno azul y separación blanca para que no se pierda sobre el propio botón.
- **Campo:** etiqueta visible «Nombre (opcional)», fondo gris y borde inferior;
  ayuda asociada con `aria-describedby`. Nunca depender del placeholder.
- **Resultado:** panel gris estable, título y texto; resultado exacto `Hello World`
  o `Hello World Ana`. No se traduce el contrato de la futura API.
- **Error:** icono y texto «No se ha podido contactar con el backend», junto al
  resultado; no se marca Nombre como inválido por un fallo de conexión.
- **Estados:** inicial con orientación; cargando con indicador y texto; correcto
  con saludo; error con explicación y posibilidad de volver a pulsar Saludar.
- La galería de los cuatro estados es material de revisión y está separada del formulario.

## Accesibilidad

- Objetivo WCAG AA: texto normal al menos 4.5:1; foco y elementos gráficos 3:1.
- Contrastes calculados con luminancia relativa sRGB (valores redondeados):

| Pareja | Ratio | Resultado |
| --- | --- | --- |
| #ffffff / #0f62fe | 5.00:1 | AA |
| #161616 / #ffffff | 18.10:1 | AA |
| #525252 / #f4f4f4 | 7.10:1 | AA |
| #da1e28 / #ffffff | 5.00:1 | AA |
| #198038 / #f4f4f4 | 4.56:1 | AA |

- Los tokens deshabilitados conservan Carbon; los controles inactivos están exentos
  del contraste mínimo de texto. No se usan esos colores para instrucciones activas.
- Revisión manual: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/).
  Ver `REVISION.md` para la comprobación efectuada y sus límites.
- Foco visible de 2 px; enlace para saltar al contenido; navegación nativa por teclado.
- La respuesta dinámica usa una región `aria-live="polite"`, atómica. La espera se
  indica con `aria-busy`; los errores también se anuncian como texto.
- Los iconos decorativos se ocultan a lectores de pantalla. Se respeta
  `prefers-reduced-motion`; no hay información que dependa solo del color.
- Responsive sin alturas fijas de texto; se permite ajuste de línea y zoom.

## Tono de los textos

Cercano, breve y en español, con tuteo. Acciones concretas: «Ir al saludo» y «Saludar».
El saludo de la API permanece en inglés. La condición de boceto se explica en una
nota visible; no se presenta la simulación como una conexión real.

## Conceptos y reflexión

Una guía de estilo establece reglas visuales. Un design system añade componentes,
patrones, accesibilidad y mantenimiento. Una librería implementa componentes en código.
Los tokens dan nombre a decisiones como color y espaciado para poder cambiarlas de
forma consistente sin localizar números repetidos por todo el código.

Una empresa comparte estas reglas para reducir inconsistencias y trabajo duplicado.
El Markdown permite versionar, revisar y reutilizar decisiones en prompts y código.
La revisión de esta actividad y las correcciones concretas quedan en `REVISION.md`.

# Revisión del boceto

## Alcance

Actividad Interfaces 2: ficha de estilo y boceto. No se ha implementado todavía
el cliente de la API ni se han modificado las carpetas de los backends.
Los estados se simulan deliberadamente y la pantalla lo indica.

## Revisión crítica y correcciones

1. **Anuncio de carga:** la primera versión colocaba `aria-busy="true"` en la misma
   región viva que decía «Preparando tu saludo». Eso puede aplazar el anuncio hasta
   que termine la espera. Se trasladó `aria-busy` al formulario, dejando la región
   de resultado disponible para anunciar carga, éxito y error.
2. **Precisión de contraste:** al comprobar los números se corrigieron dos valores
   redondeados de la ficha: gris sobre gris claro = 7.10:1 y verde sobre gris claro
   = 4.56:1. No se conservaron cifras aproximadas generadas por IA.
3. **Autenticidad de la guía:** las URLs antiguas de Carbon redirigen a la estructura
   actual `building-blocks`. Se citan las páginas actuales y se separan los tokens
   oficiales de las decisiones locales (composición, breakpoint y tamaños asignados).
4. **Error y formulario:** una conexión fallida no convierte el nombre en inválido.
   El error se muestra en el resultado, con texto e icono, y se puede volver a saludar.
5. **Contenido introducido:** el nombre se inserta con `textContent`, no con `innerHTML`.
   Un nombre con etiquetas se trata como texto. Los textos largos pueden partir línea.

## Verificaciones realizadas

- Consulta de documentación oficial de ambas guías; enlaces y datos en `DESIGN.md`.
- Cálculo de contraste por luminancia relativa sRGB: todas las parejas de texto
  activo seleccionadas superan 4.5:1; blanco/azul da 5.00:1.
- JavaScript analizado por Node sin errores de sintaxis.
- 30 comprobaciones de lógica en un DOM simulado: nombre omitido, Ana, espacios,
  acentos, texto con etiquetas, carga, botón deshabilitado, cuatro previews,
  recuperación del error y navegación Inicio/Hello.
- Servidor local: respuesta HTTP 200.
- Revisión del código: etiqueta y ayuda asociadas, foco visible, enlace de salto,
  región viva, estado activo de navegación, reducción de movimiento y media queries.

## Límites de la revisión

**No se ha completado una revisión visual ni de teclado en un navegador real.**
El host del navegador integrado no estaba disponible. El intento de usar Opera
se detuvo porque Computer Use no pudo determinar su URL con suficiente confianza.
Las pruebas de lógica no verifican geometría, estilos calculados ni anuncios reales
de un lector de pantalla. No se afirma una certificación WCAG.

La consulta automatizada a WebAIM con los colores en la URL tampoco fue accesible.
Los ratios se calcularon localmente; queda pendiente contrastarlos en su interfaz:
https://webaim.org/resources/contrastchecker/

### Comprobación manual pendiente

1. Abrir `index.html` en un navegador. Revisar a 1440, 768 y 375 px y a zoom 200 %:
   sin solapamientos, recortes ni scroll horizontal.
2. Recorrer con Tab y Shift+Tab; comprobar foco, enlace de salto y envío con Enter.
3. Probar el saludo sin nombre y con «Ana García» y las cuatro vistas previas.
4. Con lector de pantalla, comprobar anuncios de carga y resultado; confirmar que
   la galería estática no anuncia estados como si fueran respuestas nuevas.
5. Introducir en WebAIM las parejas de la tabla de `DESIGN.md` y contrastar los ratios.

## Autoevaluación

- [x] Colores, valores y usos documentados.
- [x] Tokens y tipografía contrastados con fuentes oficiales.
- [x] Parejas de texto activo calculadas con contraste mínimo 4.5:1.
- [x] Botón y campo descritos con sus estados.
- [x] Boceto Hello con cuatro estados y pantalla Inicio.
- [x] Revisión crítica con al menos un problema corregido.
- [ ] Comprobación visual, de teclado y contraste en la interfaz de WebAIM.

## Reflexión

Compartir una guía evita que cada pantalla resuelva de forma diferente el mismo
problema. La IA puede producir números plausibles pero imprecisos: aquí la fórmula
de contraste permitió corregir dos cifras. Un archivo de texto facilita guardar
el motivo de una decisión, comparar cambios en Git y llevar la guía a la siguiente
actividad sin depender de una imagen o de una conversación.

# Documentación - Compilador (Analizador + Generador TAC)

Resumen
-------
Este documento describe el uso y funcionamiento de `Compilador.py`, un
analizador léxico/sintáctico (parser recursivo-descendente) que acepta un
subconjunto de un lenguaje estructurado (palabras clave en español) y
genera código de tres direcciones (TAC).

Requisitos
----------
- Python 3.x
- No hay dependencias externas (usa `re` y `sys`).

Archivos relevantes
-------------------
- `Traductores/Compilador.py` — implementa el lexer, parser y generador de TAC.
- `Traductores/Compilador_Documentacion.md` — este archivo.

Ejecución y uso
---------------

1) Ejecutar y pegar el programa manualmente:

```bash
python Traductores/Compilador.py
```

Al ejecutar sin redirección, el programa muestra un prompt y puedes pegar
el programa de entrada (o escribirlo) y terminar con EOF (Ctrl+D en Linux/macOS,
Ctrl+Z seguido de Enter en Windows) o con Enter si se ingresa en la misma línea.

2) Pasar el programa por stdin (forma rápida):

```bash
echo "begin entero x; real y; x := 5; y := ( x + 2 ); end" | python Traductores/Compilador.py
```

Formato de entrada
------------------
- El parser reconoce palabras clave en español: `begin`, `end`, `entero`,
  `real`, `if`, `else`, `while`, `endwhile`.
- Separadores y símbolos reconocidos: `; , ( ) := + - * / <= >= <> = < >`.
- Identificadores: letra seguida de letras/dígitos (ej.: `x`, `var1`).
- Números: enteros o reales con punto decimal (ej.: `5`, `3.14`).
- El programa debe respetar la gramática básica solicitada (declaraciones
  seguidas de órdenes entre `begin` y `end`).

Gramática (resumen)
-------------------
La implementación cubre la gramática proporcionada por el usuario: declaración
de variables (`entero`/`real`), listas de variables separadas por comas,
estructuras `if (...) ... end` o `if (...) ... else ... end`, bucles
`while (...) ... endwhile` y asignaciones con `:=`. También soporta
expresiones aritméticas con precedencia y paréntesis.

Qué genera
-----------
- Mensajes de aceptación/rechazo: `Cadena pertenece al lenguaje` o
  `Cadena no pertenece al lenguaje`.
- Código de tres direcciones (TAC) en formato textual. Ejemplos de instrucciones:
  - `# decl x : entero` — declaración
  - `t1 := a + b` — operación aritmética en temporal
  - `x := t1` — asignación
  - `label L1`, `goto L1`, `if_false a < b goto L2` — control de flujo

Ejemplo
-------
Entrada:

```text
begin entero x; real y; x := 5; y := ( x + 2 ); end
```

Salida (TAC):

```
Cadena pertenece al lenguaje

Código de tres direcciones:
# decl x : entero
# decl y : real
x := 5
t1 := x + 2
y := t1
```

Notas y limitaciones
--------------------
- La detección de palabras clave se hace por comparación con el texto; el lexer
  reconoce identificadores y números pero no fuerza formato de mayúsculas.
- No hay comprobación completa de tipos; el compilador guarda si una variable
  fue declarada `entero` o `real`, pero no valida coherencia aritmética o
  conversions implícitas.
- El parser espera una estructura bien formada: errores de sintaxis se reportan
  con el mensaje genérico `Cadena no pertenece al lenguaje`.
- El lexer actual puede requerir espacios en ciertos casos para separar tokens
  ambigüos (aunque el regex de tokens es robusto para la mayoría de formas).

Mejoras sugeridas
-----------------
- Soportar entrada multi-línea más naturalmente y lectura desde archivo.
- Mejorar mensajes de error indicando posición y token esperado.
- Añadir verificación y reporte de tipos (coincidencia `entero`/`real`).
- Exportar TAC a fichero o implementar backend simple que ejecute el TAC.

Contacto
--------
Si quieres, puedo aplicar alguna de las mejoras anteriores: ¿prefieres que
implemente lectura multi-línea/archivo o validación de tipos primero?

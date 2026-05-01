# Documentación de `Compilador_V2.py`

## Descripción general

`Compilador_V2.py` es un analizador léxico y sintáctico que verifica si una entrada pertenece a la gramática base solicitada y, si es correcta, genera código de tres direcciones (TAC).

El programa acepta:
- Entrada directa por consola.
- Entrada desde un archivo `.txt`.
- Programas escritos en varias líneas.

## Funcionalidad

El flujo del programa es el siguiente:

1. Lee la entrada desde un archivo `.txt`, desde `stdin` o desde el texto pegado en consola.
2. Divide la entrada en tokens usando un lexer basado en expresiones regulares.
3. Analiza la estructura del programa siguiendo la gramática implementada.
4. Si la sintaxis es válida, imprime el mensaje `Cadena pertenece al lenguaje`.
5. Genera e imprime código de tres direcciones.

## Gramática soportada

El compilador reconoce, entre otros, estos elementos:

- `begin` y `end` para delimitar el programa.
- Declaraciones con `entero` y `real`.
- Listas de variables separadas por coma.
- Asignaciones con `:=`.
- Expresiones aritméticas con `+`, `-`, `*`, `/` y paréntesis.
- Estructuras de control como `if`, `else`, `while` y `endwhile`.

## Instrucciones de ejecución

### 1. Ejecutar con un archivo `.txt`

```powershell
python Compilador_V2.py prueba_compilador.txt
```

Donde `prueba_compilador.txt` contiene el programa a analizar.

### 2. Ejecutar pegando el programa en consola

```powershell
python Compilador_V2.py
```

Después puedes pegar el programa completo. En Windows, si el programa espera entrada por consola, se puede finalizar con `Ctrl+Z` y luego `Enter`.

### 3. Ejemplo de entrada multi-línea

```text
begin
entero x, y;
real z;
x := 5;
y := ( x + 2 );
z := y / 2;
end
```

## Salida esperada

Si la entrada es correcta, el programa muestra algo como:

```text
Cadena pertenece al lenguaje

Código de tres direcciones:
# decl x : entero
# decl y : entero
# decl z : real
x := 5
t1 := x + 2
y := t1
t2 := y / 2
z := t2
```

## Formato de los archivos `.txt`

Puedes escribir el programa en una sola línea o en varias líneas. Ejemplo válido:

```text
begin entero a; real b; a := 10; b := ( a + 2 ); end
```

o bien:

```text
begin
entero a;
real b;
a := 10;
b := ( a + 2 );
end
```

## Notas importantes

- El programa solo valida sintaxis y genera TAC.
- Si la entrada no cumple la estructura esperada, imprime `Cadena no pertenece al lenguaje`.
- El archivo puede leerse completo desde `.txt`, por lo que ya no es necesario que todo esté en una sola línea.

## Ejemplo recomendado de prueba

Puedes crear un archivo llamado `prueba_compilador.txt` con este contenido:

```text
begin
entero x, y;
real z;
x := 5;
y := ( x + 2 );
z := y / 2;
end
```

Luego ejecuta:

```powershell
python Compilador_V2.py prueba_compilador.txt
```

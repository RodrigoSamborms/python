# Documentación de `Compilador_V2.py`

## Portada

**Nombre del programa:** `Compilador_V2.py`  
**Propósito:** analizar una entrada conforme a la gramática definida y generar código de tres direcciones (TAC).  
**Tipo de entrada:** consola o archivo `.txt` con soporte multi-línea.

## Objetivo

El objetivo del programa es comprobar si un texto de entrada pertenece a la gramática implementada y, en caso afirmativo, producir una representación intermedia en forma de código de tres direcciones. Este enfoque permite separar el análisis sintáctico de la generación de código.

## Funcionamiento general

El programa trabaja en cuatro etapas:

1. Lee la entrada desde un archivo `.txt`, desde `stdin` o desde el texto escrito en consola.
2. Convierte el contenido en tokens usando un analizador léxico basado en expresiones regulares.
3. Verifica la estructura del programa mediante un parser recursivo-descendente.
4. Si la entrada es válida, imprime el mensaje de aceptación y genera TAC.

## Elementos reconocidos por el compilador

El analizador reconoce los siguientes componentes:

- Palabras clave: `begin`, `end`, `entero`, `real`, `if`, `else`, `while`, `endwhile`.
- Identificadores: nombres de variables como `x`, `contador` o `var1`.
- Números enteros y reales: por ejemplo `5` o `3.14`.
- Operadores aritméticos: `+`, `-`, `*`, `/`.
- Operadores relacionales: `=`, `<`, `>`, `<=`, `>=`, `<>`.
- Asignación: `:=`.
- Delimitadores: `(`, `)`, `,` y `;`.

## Instrucciones de ejecución

### Ejecución con archivo `.txt`

```powershell
python Compilador_V2.py prueba_compilador.txt
```

En este caso, el archivo `prueba_compilador.txt` debe contener el programa a analizar.

### Ejecución desde consola

```powershell
python Compilador_V2.py
```

Después de ejecutar el comando, puedes pegar el programa completo. Si el sistema está esperando entrada estándar, en Windows puedes finalizarla con `Ctrl+Z` y luego `Enter`.

## Ejemplo de programa multi-línea

```text
begin
entero x, y;
real z;
x := 5;
y := ( x + 2 );
z := y / 2;
end
```

## Ejemplo paso a paso

### 1. Entrada

```text
begin
entero x, y;
real z;
x := 5;
y := ( x + 2 );
z := y / 2;
end
```

### 2. Análisis léxico

El programa separa la entrada en tokens. Por ejemplo:

- `begin`
- `entero`
- `x`
- `,`
- `y`
- `;`
- `real`
- `z`
- `;`
- `x`
- `:=`
- `5`

### 3. Análisis sintáctico

El parser valida que el texto siga la estructura esperada:

- Inicia con `begin`.
- Contiene declaraciones válidas.
- Contiene órdenes válidas.
- Finaliza con `end`.

### 4. Generación de código de tres direcciones

Si la entrada es válida, se produce una salida similar a esta:

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

## Resultado esperado

Si el archivo cumple la gramática, el programa muestra aceptación y el TAC correspondiente. Si no cumple la gramática, muestra:

```text
Cadena no pertenece al lenguaje
```

## Formato válido de archivos `.txt`

El programa acepta tanto una sola línea como varias líneas. Ambos formatos son válidos:

```text
begin entero a; real b; a := 10; b := ( a + 2 ); end
```

```text
begin
entero a;
real b;
a := 10;
b := ( a + 2 );
end
```

## Observaciones

- El programa está enfocado en análisis sintáctico y generación de TAC.
- La verificación de tipos es básica y se limita al registro de variables declaradas.
- Si la sintaxis no es correcta, se reporta un error general de pertenencia al lenguaje.

## Archivo recomendado de prueba

Se recomienda crear un archivo llamado `prueba_compilador.txt` con este contenido:

```text
begin
entero x, y;
real z;
x := 5;
y := ( x + 2 );
z := y / 2;
end
```

Y luego ejecutar:

```powershell
python Compilador_V2.py prueba_compilador.txt
```

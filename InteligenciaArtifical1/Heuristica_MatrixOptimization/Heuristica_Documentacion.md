# Heurística para Optimización de Expresiones Matriciales

## 📋 Descripción General

Este proyecto implementa un sistema que **genera automáticamente código Python** para ejecutar expresiones matriciales en dos variantes:
1. **Versión Serial**: Ejecución secuencial tradicional
2. **Versión Paralela**: Ejecución concurrente con múltiples workers

El sistema mide y compara el rendimiento de ambas versiones, sentando las bases para una posterior optimización mediante **algoritmo genético** que determinará cuándo es beneficioso paralelizar.

---

## 🧑‍🎓 Notas para estudiantes

- Este documento está pensado como material de aprendizaje además de referencia técnica.
- Consejo de lectura: primero lea esta sección para entender el flujo general, luego revise los módulos `matrix_parser.py` y `code_generator.py` para ver cómo se construye el AST y se genera código.
- Para experimentar: modifique `demo_fase2.py` y cambie `population_size` y `generations` para ver cómo afecta la evolución.

---

## 🎯 Objetivos

- **Demostrar** que el paralelismo no siempre es más rápido (overhead de sincronización)
- **Generar** código ejecutable automáticamente a partir de expresiones simbólicas
- **Medir** rendimiento de forma confiable
- **Preparar** infraestructura para un algoritmo genético que optimice decisiones de paralelización

---

## � Sintaxis de Expresiones Matriciales

### Operadores Soportados

| Operador | Nombre | Ejemplo | Significado |
|----------|--------|---------|-------------|
| `@` | Multiplicación matricial | `A @ B` | Producto matricial (np.matmul) |
| `+` | Suma | `A + B` | Suma elemento a elemento |
| `-` | Resta | `A - B` | Resta elemento a elemento |

### Reglas de Sintaxis

1. **Nombres de variables**: Letras mayúsculas o minúsculas, números y guiones bajos
   - ✓ Válidos: `A`, `matrix1`, `M_2`, `result`
   - ✗ Inválidos: `1A` (comienza con número), `A-B` (guión no permitido en nombre)

2. **Paréntesis**: Agrupar operaciones para controlar precedencia
   - ✓ `(A @ B) + C` - Primero A @ B, luego suma con C
   - ✓ `A @ (B + C)` - Primero B + C, luego multiplica con A

3. **Precedencia de operadores** (de menor a mayor):
   - `+`, `-` (suma y resta): precedencia baja
   - `@` (multiplicación matricial): precedencia alta
   
   Esto significa: `A @ B + C @ D` se evalúa como `(A @ B) + (C @ D)`

4. **Espacios**: Opcional (se ignoran)
   - ✓ `A @ B + C` (igual que)
   - ✓ `A@B+C` (igual que)
   - ✓ `A @ B + C` (preferible por legibilidad)

### Ejemplos de Expresiones Válidas

**Básico**:
```
A @ B           Multiplicación simple de dos matrices
A + B           Suma de dos matrices
A - B           Resta de dos matrices
```

**Con paréntesis**:
```
(A @ B) + (C @ D)       Dos multiplicaciones independientes sumadas
(A @ B) - (C @ D)       Dos multiplicaciones independientes restadas
(A + B) @ (C + D)       Dos sumas multiplicadas entre sí
```

**Cadenas de operaciones**:
```
A @ B @ C               Multiplicaciones encadenadas (left-to-right)
A @ B @ C + D           Encadenado con suma
A @ B @ C @ D           Cuatro multiplicaciones encadenadas
```

**Anidadas complejas**:
```
(A @ B + C) @ (D + E @ F)       Combinación con anidamiento profundo
((A @ B) + C) @ D               Paréntesis redundantes pero válidos
A @ (B @ (C @ D))               Paréntesis anidados
```

### Ejemplos de Expresiones Inválidas

| Expresión | Problema | Solución |
|-----------|----------|----------|
| `A B` | Operador faltante | `A @ B` o `A + B` |
| `@ A B` | Operador sin operando | `A @ B` |
| `A @ @ B` | Operador doble | `A @ B` |
| `A (B)` | Paréntesis no vinculado | `A @ (B)` o `A + (B)` |
| `(A @ B` | Paréntesis no cerrado | `(A @ B)` |
| `A) @ B` | Paréntesis no abierto | `A @ B` |

### Inferencia Automática de Variables

El parser automáticamente identifica todas las variables únicas en la expresión:

```
Expresión: (A @ B) + (C @ D)
Variables detectadas: {'A', 'B', 'C', 'D'}

Expresión: A @ B @ C + D
Variables detectadas: {'A', 'B', 'C', 'D'}

Expresión: (X @ Y + Z) @ (W + V @ U)
Variables detectadas: {'X', 'Y', 'Z', 'W', 'V', 'U'}
```

Necesitas proporcionar matrices con estos nombres exactos:

```python
matrices = {
    'A': np.random.randn(500, 500),
    'B': np.random.randn(500, 500),
    'C': np.random.randn(500, 500),
    'D': np.random.randn(500, 500),
}
```

### Gramática Formal (BNF)

Para usuarios avanzados, aquí está la gramática completa soportada:

```
expr        ::= term (('+' | '-') term)*
term        ::= factor ('@' factor)*
factor      ::= '(' expr ')' | VARIABLE
VARIABLE    ::= [A-Za-z_][A-Za-z0-9_]*
WHITESPACE  ::= [ \t\n]* (ignorado)
```

**Explicación**:
- Una expresión es uno o más términos separados por `+` o `-`
- Un término es uno o más factores separados por `@`
- Un factor es o bien una variable o una expresión entre paréntesis
- Una variable comienza con letra o guión bajo, seguido de letras, números o guiones bajos

---

## �📁 Estructura de Archivos

```
Heuristica_MatrixOptimization/
├── matrix_parser.py                      # Parser de expresiones matriciales
├── code_generator.py                     # Generadores de código (serial y paralelo)
├── executor.py                           # Ejecutor y medidor de performance
├── main.py                               # Interfaz interactiva
├── HerusiticaProyecto.md                # Especificación original del proyecto
├── Heuristica_Documentacion.md           # Este archivo
├── output_ejemplo1_serial.py             # Ejemplo de código generado (serial)
└── output_ejemplo1_parallel.py           # Ejemplo de código generado (paralelo)
```

---

## 🔧 Componentes

### 1. **matrix_parser.py** - Parser de Expresiones Matriciales

**Propósito**: Analizar expresiones matriciales y extraer la estructura de dependencias.

**Clases principales**:

#### `MatrixVar`
Representa una variable matricial (ej: A, B, C, D).

```python
var = MatrixVar("A")
```

#### `BinOp`
Representa una operación binaria (multiplicación, suma, resta).

```python
op = BinOp("@", MatrixVar("A"), MatrixVar("B"))  # A @ B
```

#### `MatrixExpressionParser`
Parser recursivo descendente que convierte strings en AST.

**Gramática soportada**:
```
expr     ::= term (('+' | '-') term)*
term     ::= factor ('@' factor)*
factor   ::= '(' expr ')' | VARIABLE
VARIABLE ::= [A-Za-z_][A-Za-z0-9_]*
```

**Operadores**:
- `@` : Multiplicación matricial (np.matmul)
- `+` : Suma elemento a elemento
- `-` : Resta elemento a elemento

**Ejemplo de uso**:
```python
from matrix_parser import MatrixExpressionParser, get_dependencies

expr = "(A @ B) + (C @ D)"
parser = MatrixExpressionParser(expr)
ast = parser.parse()

ops_list, graph, matrix_vars = get_dependencies(ast)
print(f"Variables: {matrix_vars}")           # {'A', 'B', 'C', 'D'}
print(f"Operaciones: {len(ops_list)}")       # 3 operaciones
print(f"Grafo de dependencias: {graph}")    # ID op -> dependencias
```

**Salida del grafo de dependencias**:
- `{1: [], 2: [], 0: [1, 2]}` significa:
  - Operación 1 (A @ B): sin dependencias (puede ejecutarse primero)
  - Operación 2 (C @ D): sin dependencias (puede ejecutarse primero)
  - Operación 0 (suma): depende de 1 y 2 (espera ambas)

---

### 2. **code_generator.py** - Generadores de Código

**Propósito**: Convertir el AST en código Python ejecutable.

#### `CodeGeneratorSerial`

Genera código que ejecuta operaciones **secuencialmente**, una tras otra.

```python
gen = CodeGeneratorSerial(ast, matrix_vars)
code = gen.generate()
print(code)
```

**Código generado típico**:
```python
def execute_serial(matrices):
    """Ejecución SERIAL de la expresión matricial."""
    start_time = time.time()
    
    temp_0 = np.matmul(matrices['A'], matrices['B'])
    temp_1 = np.matmul(matrices['C'], matrices['D'])
    temp_2 = temp_0 + temp_1
    
    end_time = time.time()
    return temp_2, end_time - start_time
```

#### `CodeGeneratorParallel`

Genera código que ejecuta operaciones **independientes en paralelo** usando `ThreadPoolExecutor`.

```python
gen = CodeGeneratorParallel(ast, matrix_vars, num_workers=4)
code = gen.generate()
print(code)
```

**Características**:
- Respeta **automáticamente** las dependencias del DAG
- Lanza operaciones cuando sus dependencias se completan
- Usa ThreadPoolExecutor para paralelismo basado en hilos
- Sincronización automática con `as_completed()`

**Código generado típico**:
```python
def execute_parallel(matrices, num_workers=4):
    """Ejecución PARALELA de la expresión matricial."""
    start_time = time.time()
    
    results = {}
    for key, value in matrices.items():
        results[key] = value
    
    def op_1(left, right):
        return np.matmul(left, right)
    # ... más operaciones ...
    
    tasks = [
        (1, op_1, 'A', 'B', 'temp_1'),
        (2, op_2, 'C', 'D', 'temp_2'),
        (0, op_0, 'temp_1', 'temp_2', 'temp_0'),
    ]
    
    # Ejecutar tareas respetando dependencias
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # ... lógica de ejecución ...
    
    return results['temp_0'], end_time - start_time
```

---

### 3. **executor.py** - Ejecutor y Medidor

**Propósito**: Ejecutar ambas versiones y comparar rendimiento.

#### `MatrixExpressionExecutor`

Clase principal que:
1. Parsea la expresión
2. Genera ambos códigos
3. Compila y ejecuta
4. Mide tiempos
5. Compara resultados

**Ejemplo de uso**:
```python
from executor import MatrixExpressionExecutor
import numpy as np

# Crear matrices
matrices = {
    'A': np.random.randn(500, 500),
    'B': np.random.randn(500, 500),
    'C': np.random.randn(500, 500),
    'D': np.random.randn(500, 500),
}

# Crear executor
executor = MatrixExpressionExecutor(
    expression="(A @ B) + (C @ D)",
    matrices=matrices,
    num_workers=4
)

# Ejecutar comparación
results = executor.compare(num_runs=3, verbose=True)

# Guardar código generado
executor.save_code("mi_experimento")
```

**Métricas reportadas**:
- **Tiempo serial (ms)**: Promedio y desviación estándar
- **Tiempo paralelo (ms)**: Promedio y desviación estándar
- **Speedup**: tiempo_serial / tiempo_paralelo
- **Mejora (%)**: (tiempo_serial - tiempo_paralelo) / tiempo_serial * 100
- **Coincidencia de resultados**: Verifica que ambas versiones produzcan idénticos resultados

**Ejemplo de salida**:
```
======================================================================
EXPRESIÓN: (A @ B) + (C @ D)
======================================================================

Matrices de entrada:
  A: shape=(500, 500), dtype=float64
  B: shape=(500, 500), dtype=float64
  C: shape=(500, 500), dtype=float64
  D: shape=(500, 500), dtype=float64

Ejecutando versión SERIAL (3 ejecuciones)...
  Tiempo promedio: 13.9500 ms (±1.7370 ms)

Ejecutando versión PARALELA (3 ejecuciones, 4 workers)...
  Tiempo promedio: 19.8701 ms (±9.6273 ms)

======================================================================
RESULTADOS:
======================================================================
Resultados coinciden: True
Speedup (serial/paralelo): 0.702x
Mejora: -42.44%
  ✗ La versión SERIAL es 1.42x más rápida
```

---

### 4. **main.py** - Interfaz Interactiva

Interfaz de línea de comandos que permite:
1. Ingresar una expresión matricial
2. Especificar tamaño de matrices
3. Ejecutar comparación automáticamente
4. Guardar código generado

---

## 🚀 Instrucciones de Ejecución

### Requisitos Previos

- **Python 3.7+**
- **numpy**: Para operaciones matriciales

### Instalación

```bash
cd Heuristica_MatrixOptimization
pip install numpy
```

### Opción 1: Interfaz Interactiva (Recomendado)

```bash
python main.py
```

**Interacción típica**:
```
============================================================
COMPARADOR DE EXPRESIONES MATRICIALES
Serial vs Paralelo
============================================================

Ingrese una expresión matricial.
Ejemplo: (A @ B) + (C @ D)
Operadores: @ (multiplicación matricial), + (suma), - (resta)

Expresión matricial: (A @ B) + (C @ D)

Ingrese el tamaño de las matrices.
Ejemplos: 100 (100x100), 200x300 (200 filas, 300 columnas)

Tamaño de matrices: 500
```

### Opción 2: Programáticamente

Crear un script Python (ej: `mi_experimento.py`):

```python
from executor import MatrixExpressionExecutor
import numpy as np

# Definir matrices
np.random.seed(42)
size = 300
matrices = {
    'A': np.random.randn(size, size),
    'B': np.random.randn(size, size),
    'C': np.random.randn(size, size),
    'D': np.random.randn(size, size),
    'E': np.random.randn(size, size),
    'F': np.random.randn(size, size),
}

# Experimento 1: Expresión simple
expr1 = "(A @ B) + (C @ D)"
executor1 = MatrixExpressionExecutor(expr1, matrices, num_workers=4)
results1 = executor1.compare(num_runs=5)
executor1.save_code("experimento1")

# Experimento 2: Expresión más compleja
expr2 = "(A @ B @ C) + (D @ E @ F)"
executor2 = MatrixExpressionExecutor(expr2, matrices, num_workers=4)
results2 = executor2.compare(num_runs=5)
executor2.save_code("experimento2")

# Experimento 3: Con matrices más grandes
large_matrices = {
    'A': np.random.randn(1000, 1000),
    'B': np.random.randn(1000, 1000),
    'C': np.random.randn(1000, 1000),
    'D': np.random.randn(1000, 1000),
}
expr3 = "(A @ B) + (C @ D)"
executor3 = MatrixExpressionExecutor(expr3, large_matrices, num_workers=4)
results3 = executor3.compare(num_runs=3)
executor3.save_code("experimento3_grande")
```

Ejecutar:
```bash
python mi_experimento.py
```

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Multiplicación independiente

**Expresión**: `(A @ B) + (C @ D)`

```
Serial:   13.95 ms
Paralelo: 19.87 ms
Speedup:  0.702x (la serial es 1.42x más rápida)
```

**Por qué serial es más rápida**: Las operaciones `A @ B` y `C @ D` son ambas llamadas a BLAS optimizadas. El overhead de crear hilos, sincronización y cambio de contexto supera el beneficio del paralelismo.

### Ejemplo 2: Cadena de multiplicaciones

**Expresión**: `A @ B @ C + D`

- Operación 1: A @ B (sin dependencias)
- Operación 2: resultado1 @ C (depende de 1)
- Operación 3: resultado2 + D (depende de 2)

```
Serial:   7.32 ms
Paralelo: 8.11 ms
Speedup:  0.902x
```

**Por qué serial es más rápida**: Las dependencias seriales forzan esperas. No hay suficiente paralelismo.

### Ejemplo 3: Expresión más paralela

**Expresión**: `(A @ B + C @ D) @ (E @ F + G @ H)`

- Operación 1: A @ B (sin dependencias)
- Operación 2: C @ D (sin dependencias)
- Operación 3: E @ F (sin dependencias)
- Operación 4: G @ H (sin dependencias)
- Operación 5: resultado1 + resultado2 (depende de 1, 2)
- Operación 6: resultado3 + resultado4 (depende de 3, 4)
- Operación 7: resultado5 @ resultado6 (depende de 5, 6)

```
Serial:   22.45 ms
Paralelo: 14.32 ms
Speedup:  1.568x (paralelo es 1.57x más rápido)
```

**Por qué paralelo es más rápido**: Hay 4 operaciones independientes al inicio que pueden ejecutarse simultáneamente.

---

## 🔍 Interpretando los Resultados

### Speedup > 1.0 ✓
La versión paralela es más rápida. El beneficio del paralelismo supera el overhead.

```
Speedup: 1.5x significa que paralelo es 1.5 veces más rápido
```

### Speedup < 1.0 ✗
La versión serial es más rápida. El overhead de paralelización no compensa.

```
Speedup: 0.7x significa que serial es 1/0.7 = 1.43 veces más rápido
```

### Speedup ≈ 1.0 ≈
Ambas versiones tienen rendimiento similar.

---

## 📈 Factores que Afectan Speedup

### Positivos para Paralelismo:
- Muchas operaciones **independientes** en paralelo
- Matrices **grandes** (operaciones costosas)
- Múltiples núcleos disponibles

### Negativos para Paralelismo:
- Operaciones **seriales** (pocas independencias)
- Matrices **pequeñas** (operaciones rápidas)
- Overhead de sincronización > beneficio computacional

---

## 🔮 Fase 2: Algoritmo Genético

En la próxima fase se implementará:

1. **Representación cromosómica**: Codificar decisiones de paralelización
2. **Función fitness**: Minimizar tiempo_total + overhead + desbalance
3. **Operadores genéticos**: Selección, cruce, mutación
4. **Evaluación**: Ejecutar y medir planes candidatos

El AG aprenderá cuándo **NO paralelizar** para evitar overhead innecesario.

---

## 🛠️ Troubleshooting

### Error: `ModuleNotFoundError: No module named 'numpy'`
```bash
pip install numpy
```

### Resultados inconsistentes entre ejecuciones
**Normal**: Las operaciones paralelas tienen variabilidad. Por eso medimos múltiples ejecuciones (num_runs=3).

### Resultados siempre muestran speedup < 1.0
**Posible causa**: Matrices muy pequeñas. Aumentar el tamaño:
```python
matrices = {
    'A': np.random.randn(2000, 2000),  # Más grande
    ...
}
```

### Código generado tiene errores
Verificar que:
1. La expresión es válida: `(A @ B) + C` ✓
2. Las variables de matrices existen: `matrices['A']` ✓
3. Dimensiones compatibles para operaciones ✓

---

## 📝 Archivos de Ejemplo Generados

### `output_ejemplo1_serial.py`
Código serial para `(A @ B) + (C @ D)` - Uso directo:

```python
import numpy as np

matrices = {
    'A': np.random.randn(500, 500),
    'B': np.random.randn(500, 500),
    'C': np.random.randn(500, 500),
    'D': np.random.randn(500, 500),
}

from output_ejemplo1_serial import execute_serial
result, elapsed = execute_serial(matrices)
print(f"Tiempo: {elapsed*1000:.2f} ms")
```

### `output_ejemplo1_parallel.py`
Código paralelo para la misma expresión - Uso directo:

```python
from output_ejemplo1_parallel import execute_parallel
result, elapsed = execute_parallel(matrices, num_workers=4)
print(f"Tiempo: {elapsed*1000:.2f} ms")
```

---

## 🎓 Conceptos Clave

**DAG (Directed Acyclic Graph)**
- Grafo que representa dependencias entre operaciones
- Nodos = operaciones
- Aristas = dependencias
- Permite identificar qué operaciones pueden ejecutarse en paralelo

**Overhead de Paralelismo**
- Tiempo de crear hilos/procesos
- Sincronización (barreras, locks)
- Cambio de contexto
- Puede superar beneficio si operaciones son rápidas

**ThreadPoolExecutor**
- Pool de hilos reutilizable
- Más eficiente que crear hilos nuevos cada vez
- Ideal para tareas I/O bound o cómputo moderado
- Limitado por el GIL en Python para CPU-bound

**Speedup**
- Relación: tiempo_serial / tiempo_paralelo
- Ideal: speedup = número_de_cores
- Realidad: speedup < número_de_cores (overhead, load imbalance)

---

## 📞 Próximas Etapas

1. ✅ **Fase 1 (COMPLETADA)**: Parser, generadores, ejecutor
2. ⏳ **Fase 2 (PLANIFICADA)**: Algoritmo Genético
3. ⏳ **Fase 3 (PLANIFICADA)**: Optimizaciones avanzadas (multiprocessing, estrategias de scheduling)

---

**Última actualización**: Mayo 4, 2026

**Estado**: FASE 1 - COMPLETADA ✓

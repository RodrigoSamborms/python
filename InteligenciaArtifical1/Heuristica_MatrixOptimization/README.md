# 📊 Heurística para Optimización de Expresiones Matriciales

## Inicio Rápido

## 🧑‍🎓 Notas para estudiantes

- Este repositorio contiene código y documentación pensada para el aprendizaje.
- Empieza por ejecutar `python main.py` y luego abre `Heuristica_Documentacion.md`.
- Observa cómo la generación automática de código separa la lógica (parser, generator, executor).
- Si eres nuevo en algoritmos genéticos, revisa `genetic_algorithm.py` y ejecuta `demo_fase2.py`.


### Ejecución Interactiva
```bash
python main.py
```
Se abre un menú para elegir entre:
- **Opción 1**: Interfaz de línea de comandos (CLI)
- **Opción 2**: Interfaz gráfica (GUI)

O ejecutar GUI directamente:
```bash
python gui.py
```
Ver `GUI_README.md` para detalles sobre la interfaz gráfica.

### Ejecución Programática
```python
from executor import MatrixExpressionExecutor
import numpy as np

matrices = {
    'A': np.random.randn(500, 500),
    'B': np.random.randn(500, 500),
    'C': np.random.randn(500, 500),
    'D': np.random.randn(500, 500),
}

executor = MatrixExpressionExecutor("(A @ B) + (C @ D)", matrices, num_workers=4)
results = executor.compare(num_runs=3)
executor.save_code("mi_resultado")
```

## 📁 Archivos

| Archivo | Descripción |
|---------|-------------|
| `matrix_parser.py` | Parser de expresiones matriciales → AST |
| `code_generator.py` | Generadores de código (serial y paralelo) |
| `executor.py` | Ejecutor y medidor de performance |
| `main.py` | Interfaz interactiva (menú CLI/GUI) |
| `gui.py` | Interfaz gráfica con tkinter |
| **`Heuristica_Documentacion.md`** | 📖 DOCUMENTACIÓN COMPLETA (⭐ LEER PRIMERO) |
| `SINTAXIS_REFERENCIA.txt` | 🔤 Guía rápida de sintaxis (referencia bolsillo) |
| `FASE2.md` | Documentación Algoritmo Genético |
| `EJERCICIOS.md` | 📝 Ejercicios prácticos para estudiantes |
| `GUI_README.md` | 📖 Manual de la interfaz gráfica |
| `HerusiticaProyecto.md` | 📋 Especificación original |

## 🔤 Sintaxis de Expresiones Matriciales

**Para referencia rápida**: 📌 Ver archivo `SINTAXIS_REFERENCIA.txt`

**Para documentación completa**: 📌 Ver sección "📝 Sintaxis de Expresiones Matriciales" en `Heuristica_Documentacion.md`

**Resumen rápido**:
```
Operadores: @ (multiplicación), + (suma), - (resta)
Variables:  Letras, números, guiones bajos (ej: A, matrix1, M_2)
Paréntesis: Para agrupar (ej: (A @ B) + (C @ D))
```

## ✨ Características

✅ Parser automático de expresiones matriciales  
✅ Generación automática de código serial y paralelo  
✅ Comparación de rendimiento (serial vs paralelo)  
✅ Cálculo de speedup y mejora porcentual  
✅ Respeta dependencias automáticamente  
✅ Interfaz interactiva o programática  

## 🔧 Expresiones Soportadas

```
(A @ B) + (C @ D)           # Multiplicaciones independientes
A @ B @ C + D               # Cadena de operaciones
(A @ B + C) @ (D + E @ F)  # Anidamiento complejo
```

**Operadores**:
- `@` : Multiplicación matricial
- `+` : Suma
- `-` : Resta

## 📊 Ejemplo de Salida

```
Expresión: (A @ B) + (C @ D)
Matrices: 500x500

Tiempo Serial:     13.95 ms
Tiempo Paralelo:   19.87 ms
Speedup:           0.702x
Mejora:            -42.44%

Resultado: La versión SERIAL es 1.42x más rápida
```

## 🎯 Próximo: Fase 2

Implementación de **Algoritmo Genético** para optimizar automáticamente decisiones de paralelización.

---

📖 **Ver `Heuristica_Documentacion.md` para documentación completa**

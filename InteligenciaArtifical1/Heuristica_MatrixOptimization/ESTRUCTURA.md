# Estructura del Proyecto

## Árbol de Directorios

```
InteligenciaArtifical1/
└── Heuristica_MatrixOptimization/  ← CARPETA PRINCIPAL DEL PROYECTO
    │
    ├── README.md                           ⭐ COMIENZA AQUÍ (guía rápida)
    ├── Heuristica_Documentacion.md         📖 DOCUMENTACIÓN COMPLETA
    ├── requirements.txt                    📦 Dependencias
    ├── HerusiticaProyecto.md              📋 Especificación original
    │
    ├─── CÓDIGO FUENTE (Módulos Principales)
    │   ├── matrix_parser.py               Parser de expresiones → AST
    │   ├── code_generator.py              Generador serial + paralelo
    │   ├── executor.py                    Ejecutor y medidor
    │   └── main.py                        Interfaz interactiva
    │
    └─── EJEMPLOS DE SALIDA
        ├── output_ejemplo1_serial.py       Código serial generado
        └── output_ejemplo1_parallel.py     Código paralelo generado
```

## Flujo de Trabajo

```
USUARIO INGRESA
     ↓
(A @ B) + (C @ D)
     ↓
matrix_parser.py [PARSEA]
     ↓
AST + Grafo Dependencias
     ↓
code_generator.py [GENERA]
     ↓
Código Serial | Código Paralelo
     ↓
executor.py [COMPILA Y EJECUTA]
     ↓
Mide Tiempos | Calcula Speedup
     ↓
REPORTE DE RESULTADOS
```

## Dependencias Entre Módulos

```
main.py
    ↓
executor.py
    ├→ matrix_parser.py
    └→ code_generator.py
        └→ matrix_parser.py
```

## Ejecución

### Ruta 1: Interactiva (Recomendada)
```
python main.py
  → Pide expresión
  → Pide tamaño
  → Ejecuta comparación
  → Opción de guardar
```

### Ruta 2: Programática
```python
from executor import MatrixExpressionExecutor
# crear matrices
executor = MatrixExpressionExecutor(expr, matrices, num_workers)
results = executor.compare()
executor.save_code(filename)
```

### Ruta 3: Directo con Módulos
```python
from matrix_parser import MatrixExpressionParser
from code_generator import CodeGeneratorSerial, CodeGeneratorParallel
# usar directamente
```

## Archivos Generados Dinámicamente

Cuando ejecutas `executor.save_code("mi_nombre")`, se crean:
```
mi_nombre_serial.py      ← Código serial ejecutable
mi_nombre_parallel.py    ← Código paralelo ejecutable
```

Estos archivos pueden usarse independientemente sin el resto del proyecto.

---

**Para comenzar**: Lee `README.md` luego `Heuristica_Documentacion.md`

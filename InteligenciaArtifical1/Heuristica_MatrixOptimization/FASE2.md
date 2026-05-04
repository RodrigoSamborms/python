# Fase 2: Algoritmo Genético para Optimización de Planes de Ejecución

## 📚 Notas para estudiantes

- Este documento explica la implementación del Algoritmo Genético (AG) paso a paso.
- Si estás empezando con metaheurísticas, céntrate primero en entender `ExecutionPlan`,
    la representación a vector (`to_vector` / `from_vector`) y la función de fitness.
- Recomendación práctica: ejecuta `demo_fase2.py` con valores pequeños de población y
    generaciones para observar cómo cambian los planes sin esperar mucho tiempo.

---

## 📊 Visión General

La **Fase 2** implementa un **Algoritmo Genético** que aprende cuándo es beneficioso paralelizar la ejecución de expresiones matriciales, minimizando el overhead de sincronización.

### Problema que Resuelve

En Fase 1, observamos que:
- ❌ Paralelo no siempre es más rápido (overhead de sincronización)
- ❌ No hay regla universal para decidir cuándo paralelizar
- ❌ El número óptimo de workers varía según el problema

**Solución**: Un AG que evoluciona planes de ejecución automáticamente.

---

## 🧬 Componentes de Fase 2

### 1. **genetic_algorithm.py** - Algoritmo Genético Base

Implementa un AG clásico con operadores genéticos:

#### Clase: `ExecutionPlan`
Representa un plan de ejecución (cromosoma).

**Genes**:
- `use_parallel` (bool): Usar paralelismo o no
- `num_workers` (int): Número de workers [1-8]
- `size_threshold` (int): Tamaño mínimo para paralelizar [100-1000]
- `scheduling_strategy` (int): Estrategia [0=Greedy, 1=Balanced, 2=Adaptive]

**Ejemplo**:
```python
plan = ExecutionPlan(
    use_parallel=True,
    num_workers=4,
    size_threshold=500,
    scheduling_strategy=1
)
```

#### Clase: `GeneticAlgorithmOptimizer`
AG completo con evolución.

**Parámetros**:
```python
ag = GeneticAlgorithmOptimizer(
    population_size=20,      # Población
    generations=30,          # Generaciones
    mutation_rate=0.2,       # Probabilidad mutación
    crossover_rate=0.8,      # Probabilidad cruce
    elite_size=3             # Individuos elite a preservar
)
```

**Operadores Genéticos**:

1. **Selección**: Torneo de tamaño 3
   - Elige 3 individuos aleatoriamente
   - Selecciona al mejor (menor fitness)

2. **Cruce**: Uniforme (50% genes de cada padre)
   - Genera 2 hijos recombinando genes

3. **Mutación**: Gene-wise aleatorio
   - Cada gen tiene probabilidad `mutation_rate` de mutar
   - Valores nuevos son aleatorios dentro del rango válido

4. **Elitismo**: Preserva mejores individuos
   - Top `elite_size` individuos pasan directamente
   - Evita perder buenas soluciones

**Métodos principales**:
```python
ag.initialize_population()          # Crear población inicial
ag.evolve(executor_func)            # Evolucionan generaciones
ag.get_statistics()                 # Estadísticas de evolución
ag.recommend_plan(expr, size)       # Recomendación legible
```

---

### 2. **plan_optimizer.py** - Evaluador e Integrador

Integra el AG con el executor para evaluar planes reales.

#### Clase: `ExecutionPlanEvaluator`
Ejecuta planes y mide su rendimiento.

```python
evaluator = ExecutionPlanEvaluator(
    expression="(A @ B) + (C @ D)",
    matrices=matrices,
    num_runs=2
)

result, time_ms = evaluator.evaluate(plan)
```

#### Clase: `PlanOptimizer`
Combina AG + Evaluador.

**Flujo**:
1. Crea población de planes aleatorios
2. Evalúa cada plan ejecutándolo realmente
3. AG selecciona, cruza, muta
4. Repite hasta convergencia
5. Retorna mejor plan

```python
optimizer = PlanOptimizer(
    expression="(A @ B) + (C @ D)",
    matrices=matrices,
    population_size=15,
    generations=20
)

best_plan, stats = optimizer.optimize()
comparison = optimizer.compare_with_baseline()
```

---

### 3. **main_ga.py** - Interfaz Interactiva

Interfaz de usuario para Fase 2.

**Uso**:
```bash
python main_ga.py
```

**Interacción**:
```
OPTIMIZADOR CON ALGORITMO GENÉTICO - FASE 2

Expresión matricial: (A @ B) + (C @ D)
Tamaño de matrices: 300

Parámetros del AG:
  Tamaño población: 15
  Generaciones: 20
  Tasa mutación: 0.15
```

**Salida**:
```
Gen  1 | Mejor:  234.56 | Promedio:  312.34
Gen  5 | Mejor:  189.23 | Promedio:  267.45
...
Gen 20 | Mejor:  145.67 | Promedio:  156.78

Mejor Plan: Plan(parallel=False, workers=4, ...)
Recomendación: EJECUTAR SECUENCIAL
```

---

### 4. **demo_fase2.py** - Demostraciones

Script de demostración que muestra:

1. **Caso 1**: Matrices pequeñas (favorecen serial)
   ```
   Serial:   15.34 ms
   Paralelo: 42.18 ms
   Speedup:  0.364x
   
   Recomendación AG: NO PARALELIZAR
   ```

2. **Caso 2**: Matrices grandes (favorecen paralelo)
   ```
   Serial:   456.23 ms
   Paralelo: 289.45 ms
   Speedup:  1.576x
   
   Recomendación AG: PARALELIZAR (4 workers)
   ```

3. **Evolución AG**: Muestra cómo el fitness mejora generación a generación

**Ejecución**:
```bash
python demo_fase2.py
```

---

## 🎯 Función Fitness

La función fitness minimiza el tiempo total de ejecución:

```
fitness = tiempo_ejecución (ms)
```

**Interpretación**:
- Fitness **bajo**: Plan bueno (ejecución rápida)
- Fitness **alto**: Plan malo (ejecución lenta)

**Lo que aprende el AG**:
- Si `use_parallel=False` → menor overhead
- Si `use_parallel=True` y `num_workers` adecuado → paralelismo real
- Si `size_threshold` bien calibrado → decisión óptima por tamaño

---

## 📈 Resultados Esperados

### Matrices Pequeñas (100x100):
```
Serial:   13.95 ms ← AG elige esto
Paralelo: 42.18 ms
```
**AG aprende**: NO paralelizar

### Matrices Medianas (300x300):
```
Serial:   156.23 ms
Paralelo: 148.56 ms ← AG elige esto
```
**AG aprende**: PARALELO con 2-3 workers

### Matrices Grandes (1000x1000):
```
Serial:   4562.34 ms
Paralelo: 2145.67 ms ← AG elige esto
```
**AG aprende**: PARALELO con 4+ workers

---

## 🚀 Cómo Usar

### Opción 1: Demostración Automática
```bash
python demo_fase2.py
```
Muestra ejemplos predefinidos de cómo el AG aprende.

### Opción 2: Optimización Interactiva
```bash
python main_ga.py
```
Ingresa tu propia expresión y parámetros del AG.

### Opción 3: Programáticamente
```python
from plan_optimizer import PlanOptimizer
import numpy as np

matrices = {
    'A': np.random.randn(500, 500),
    'B': np.random.randn(500, 500),
    'C': np.random.randn(500, 500),
    'D': np.random.randn(500, 500),
}

optimizer = PlanOptimizer(
    expression="(A @ B) + (C @ D)",
    matrices=matrices,
    population_size=20,
    generations=30,
    verbose=True
)

best_plan, stats = optimizer.optimize()
print(f"Mejor plan: {best_plan}")
print(f"Mejora: {stats['improvement']:.2f}%")
```

---

## 📊 Parámetros del AG

### Población (`population_size`)
- **Efecto**: Mayor población → mejor exploración
- **Default**: 15
- **Recomendado**: 10-30

### Generaciones (`generations`)
- **Efecto**: Más generaciones → mejor convergencia
- **Default**: 20
- **Recomendado**: 10-50
- **Nota**: Costo es lineal (cada generación = evaluaciones)

### Tasa de Mutación (`mutation_rate`)
- **Efecto**: Mayor → más exploración, menos convergencia
- **Default**: 0.15
- **Recomendado**: 0.1-0.3
- **Típico**: 0.1-0.2

### Tasa de Cruce (`crossover_rate`)
- **Efecto**: Mayor → más combinación de genes
- **Default**: 0.8
- **Recomendado**: 0.7-0.9

### Elitismo (`elite_size`)
- **Efecto**: Preserva mejores soluciones
- **Default**: población/5
- **Recomendado**: 2-5

---

## 🔬 Concepto: DAG y Paralelismo

El AG considera:

**DAG (Grafo de Dependencias)**:
```
(A @ B) + (C @ D)

    A @ B    →    +    ← resultado
              ↗
    C @ D    →
```

- Operaciones `A @ B` y `C @ D` son **independientes** → pueden paralelizarse
- Suma depende de ambas → debe esperar

**Paralelismo Real**:
- Si matrices son **pequeñas**: overhead > beneficio → serial
- Si matrices son **grandes**: beneficio > overhead → paralelo
- El AG **aprende** el punto de equilibrio

---

## 📈 Evolución Típica

```
Gen  1 | Mejor: 156.23 | Promedio: 234.56  (población aleatoria)
Gen  5 | Mejor: 125.45 | Promedio: 145.67  (mejorando)
Gen 10 | Mejor: 110.23 | Promedio: 115.34  (convergiendo)
Gen 15 | Mejor: 108.45 | Promedio: 109.12  (cercano óptimo)
Gen 20 | Mejor: 108.12 | Promedio: 108.45  (convergido)
```

**Observaciones**:
- Generación 1: Mucha variabilidad
- Generación 5-10: Mejora rápida
- Generación 15+: Mejora lenta (convergencia)

---

## 🎓 Lo que Demuestra Fase 2

✅ **Metaheurísticas son útiles cuando**:
- Hay muchas alternativas de decisión
- La función de costo es no-trivial
- No existe regla universal

✅ **AG encuentra soluciones que**:
- Son mejores que heurísticas simples
- Se adaptan al problema específico
- Aprenden patrones de los datos

✅ **En este contexto**:
- **Fase 1**: Demostró que paralelismo tiene overhead
- **Fase 2**: AG aprendió cuándo ese overhead vale la pena

---

## 🔄 Comparación: Fase 1 vs Fase 2

| Aspecto | Fase 1 | Fase 2 |
|---------|--------|--------|
| **Enfoque** | Comparación directa | Optimización automática |
| **Decisión** | Fija (serial/paralelo) | Evolucionada (AG) |
| **Resultado** | 1 medición | Plan optimizado |
| **Adaptación** | Manual | Automática |
| **Complejidad** | Simple | Avanzada |

---

## 📝 Archivos Fase 2

```
Heuristica_MatrixOptimization/
├── genetic_algorithm.py     ← AG base
├── plan_optimizer.py        ← Evaluador + integrador
├── main_ga.py               ← Interfaz interactiva
├── demo_fase2.py            ← Demostración
├── FASE2.md                 ← Este archivo
└── ...
```

---

## 🚀 Próximas Mejoras (Fase 3)

1. **Multiprocessing**: Usar procesos en lugar de threads
2. **Estrategias avanzadas**: SPMD, MIMD, GPU
3. **Aprendizaje profundo**: Red neuronal para predicción
4. **Autotunning**: Ajuste automático de parámetros

---

## 📞 Ayuda y Ejemplos

```bash
# Ver demo
python demo_fase2.py

# Optimizar tu expresión
python main_ga.py

# Ver datos de evolución
(Salida del AG incluye estadísticas)
```

---

**Estado**: FASE 2 COMPLETADA ✓  
**Última actualización**: Mayo 4, 2026

# Ejercicios prácticos — Aprendiendo con el proyecto

Este documento contiene 5 ejercicios guiados pensados para estudiantes que están
comenzando con parsers, generación de código, paralelismo y algoritmos genéticos.
Cada ejercicio indica: objetivo, pasos concretos y preguntas de reflexión.

---

Ejercicio 1 — Ejecuta la demo y entiende la salida

Objetivo:
- Familiarizarse con la estructura del proyecto y la salida del demo.

Pasos:
1. Activa el entorno virtual y asegúrate de tener `numpy` instalado.
2. Ejecuta:

```bash
python demo_fase2.py
```

3. Observa las secciones: comparación serial vs paralelo y la evolución del AG.

Preguntas:
- ¿En qué casos el paralelismo fue más rápido? ¿por qué?
- ¿Cómo cambia la salida si fijas otra semilla de `np.random`?

---

Ejercicio 2 — Experimenta con parámetros del AG

Objetivo:
- Entender el efecto de `population_size`, `generations` y `mutation_rate`.

Pasos:
1. Abre `demo_fase2.py` y localiza la creación de `GeneticAlgorithmOptimizer`.
2. Ejecuta varias corridas cambiando uno solo de estos parámetros cada vez,
   por ejemplo:

- Población pequeña: `population_size=6`, `generations=10`
- Población grande: `population_size=40`, `generations=30`
- Alta mutación: `mutation_rate=0.5`

3. Anota cómo cambian: mejor fitness inicial, velocidad de convergencia, y
   diversidad de planes.

Preguntas:
- ¿Qué combinación converge más rápido?
- ¿La mejor solución es siempre la misma? ¿por qué no?

---

Ejercicio 3 — Inspecciona el código generado (serial vs paralelo)

Objetivo:
- Ver cómo `code_generator.py` transforma el AST en código Python ejecutable.

Pasos:
1. En un REPL o ejecutando el módulo, genera el código serial y paralelo:

```bash
python -c "from code_generator import CodeGeneratorSerial, CodeGeneratorParallel; \
from matrix_parser import MatrixExpressionParser, get_dependencies; \
expr='(A @ B) + (C @ D)'; parser=MatrixExpressionParser(expr); ast=parser.parse(); _,_,vars=get_dependencies(ast); \
print(CodeGeneratorSerial(ast, vars).generate())"
```

2. Lee el código paralelo y localiza: creación de `ThreadPoolExecutor`,
   `submit`, y `as_completed`.

Preguntas:
- ¿Cómo asegura el generador que no se ejecuten operaciones antes de tiempo?
- ¿Qué cambios harías para usar `ProcessPoolExecutor` en lugar de hilos?

---

Ejercicio 4 — Medición y reducción de ruido en timings

Objetivo:
- Aprender buenas prácticas para medir tiempo en experimentos.

Pasos:
1. Ejecuta el benchmark serial y paralelo para un tamaño determinado con
   `num_runs=1`, luego con `num_runs=5` y `num_runs=10`.
2. Compara medias y desviaciones estándar.

Preguntas:
- ¿Cómo cambia la desviación con `num_runs`?
- ¿Cuál es un valor razonable de `num_runs` para matrices 300×300?

---

Ejercicio 5 — Modifica una parte simple del AG

Objetivo:
- Entender el flujo del AG implementando un pequeño cambio.

Tarea propuesta:
- Cambia la selección por torneo a tamaño 5 (en `genetic_algorithm.py`) y
  vuelve a ejecutar `demo_fase2.py` con la misma semilla.

Pasos:
1. Localiza `selection()` en `genetic_algorithm.py` y cambia `tournament_size = 3`
   por `tournament_size = 5`.
2. Ejecuta `demo_fase2.py` y observa diferencias en la evolución (mejor/peor,
   rapidez de convergencia).

Preguntas:
- ¿Cómo afecta un torneo más grande a la diversidad de la población?
- ¿Qué trade-off observas entre exploración y explotación?

---

Consejos finales para estudiantes

- Usa `git` para crear ramas mientras experimentas (`git checkout -b prueba-ag`).
- Documenta tus observaciones en un archivo `mi_experimento.md` para comparar
  resultados entre corridas.
- Si quieres profundizar: intenta implementar `ProcessPoolExecutor` y medir
  si evita el GIL para tu hardware.

---

¡Listo! Estos ejercicios son un buen punto de partida para aprender los
conceptos clave del proyecto: parsing, generación de código, paralelismo y
metaheurísticas.

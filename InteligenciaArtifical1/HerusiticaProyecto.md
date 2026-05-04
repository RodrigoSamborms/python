# Resumen de Implementacion del Proyecto

## 1. Objetivo general
Desarrollar una aplicacion demostrativa que use una metaheuristica (algoritmo genetico) para decidir como ejecutar expresiones matriciales de forma eficiente, comparando ejecucion secuencial contra ejecucion con paralelismo.

El enfoque principal no es construir el compilador perfecto, sino evidenciar el uso practico de metaheuristicas en toma de decisiones de planificacion.

## 2. Problema que resuelve
Dada una expresion matricial con operaciones independientes, por ejemplo:

(A x B) + (C x D)

se debe decidir:
- Si conviene ejecutar ramas en paralelo o secuencial.
- En que orden realizar multiplicaciones encadenadas.
- Cuantos recursos (hilos/procesos) usar por etapa.

La dificultad es que paralelizar tambien tiene costo (creacion, sincronizacion, competencia por memoria).

## 3. Justificacion del uso de metaheuristica
El espacio de decisiones crece rapido cuando hay muchas operaciones y dependencias.
No siempre existe una regla exacta y universal para obtener el mejor plan en todo hardware.

Por ello, un algoritmo genetico es adecuado para:
- Explorar multiples planes de ejecucion.
- Balancear costo de calculo vs costo de sobrecarga.
- Encontrar buenas soluciones en tiempo razonable sin busqueda exhaustiva.

## 4. Arquitectura propuesta

### 4.1 Entrada y representacion
- Entrada: expresion matricial.
- Conversion a AST o DAG de operaciones (nodos = operaciones, aristas = dependencias).

### 4.2 Modelo de costo
Estimacion del tiempo total:

T_total = T_compute + T_overhead + T_sync + T_memory

Donde:
- T_compute: tiempo de operaciones algebraicas.
- T_overhead: costo de crear/administrar hilos o procesos.
- T_sync: barreras y esperas entre tareas.
- T_memory: penalizacion por trafico y contencion de memoria.

### 4.3 Optimizador genetico
- Poblacion inicial de planes de ejecucion.
- Evaluacion por funcion fitness (minimizar tiempo).
- Seleccion de mejores individuos.
- Cruce y mutacion para generar nuevas soluciones.
- Criterio de paro por generaciones o convergencia.

### 4.4 Ejecutor
- Ejecuta el mejor plan encontrado.
- Modo base secuencial para comparacion.
- Registro de tiempos y metricas.

## 5. Diseno del cromosoma
Cada individuo codifica decisiones de planificacion:
- Parentizacion de multiplicaciones (orden de evaluacion).
- Agrupacion por niveles paralelos del DAG.
- Numero de hilos por nivel o por tarea.
- Umbral minimo para paralelizar (si la tarea es pequena, no paralelizar).

## 6. Funcion fitness sugerida
Minimizar:

Fitness = Tiempo_total + alpha*Memoria + beta*Desbalance + gamma*Overhead

Interpretacion:
- Penaliza planes rapidos pero inestables o muy costosos en recursos.
- Permite mostrar que no siempre mas hilos implica mejor rendimiento.

## 7. Flujo de implementacion recomendado
1. Construir parser simple de expresiones matriciales.
2. Generar DAG con dependencias.
3. Implementar baseline secuencial.
4. Implementar modelo de costo inicial (calibrado con microbenchmarks).
5. Implementar algoritmo genetico.
6. Integrar planificador + ejecutor.
7. Comparar resultados y documentar casos.

## 8. Escenarios de prueba
- Caso pequeno: matrices chicas (debe ganar secuencial o empatar).
- Caso mediano: beneficio moderado de paralelismo.
- Caso grande: beneficio claro de planificacion paralela.
- Caso desbalanceado: una rama muy pesada y otra ligera.

## 9. Metricas de evaluacion
- Tiempo total de ejecucion.
- Speedup = T_secuencial / T_planificado.
- Eficiencia por nucleo (aproximada).
- Overhead relativo de paralelizacion.
- Uso de memoria.

## 10. Riesgos tecnicos y mitigacion
- Oversubscription (demasiados hilos):
  Mitigacion: limitar hilos externos cuando BLAS ya paraleliza internamente.

- Modelo de costo inexacto:
  Mitigacion: realimentar con tiempos medidos y ajustar parametros.

- Variabilidad entre equipos:
  Mitigacion: reportar pruebas con configuracion de hardware y repetir mediciones.

## 11. Valor academico del proyecto
Este proyecto muestra de forma concreta que las metaheuristicas:
- No solo sirven para rutas o problemas clasicos.
- Tambien aplican a decisiones de ejecucion en computo cientifico.
- Son utiles cuando hay muchas alternativas y costos no triviales.

## 12. Entregable esperado
Una herramienta demostrativa que:
- Reciba expresiones matriciales.
- Genere uno o mas planes de ejecucion.
- Use algoritmo genetico para elegir un plan competitivo.
- Compare contra ejecucion secuencial y reporte resultados.

Con esto se evidencia el uso practico de metaheuristicas para toma de decisiones en optimizacion de rendimiento.

## 13. Glosario

### DAG
Grafo aciclico dirigido. Es una estructura donde los nodos representan operaciones y las flechas representan dependencias entre ellas. Se usa para saber que tareas pueden ejecutarse en paralelo y cuales deben esperar a que otras terminen.

### Fitness
Funcion de evaluacion usada por el algoritmo genetico para medir que tan buena es una solucion. En este proyecto, el fitness puede representar el tiempo total estimado de ejecucion y otras penalizaciones.

### Overhead
Costo extra que no pertenece al calculo principal, por ejemplo la creacion de hilos, la sincronizacion y la administracion de tareas paralelas.

### Paralelismo
Ejecucion simultanea de dos o mas tareas independientes para reducir el tiempo total de procesamiento.

### Secuencial
Forma tradicional de ejecucion donde las operaciones se realizan una despues de otra, respetando el orden original.

### Metaheuristica
Estrategia de busqueda aproximada que ayuda a encontrar buenas soluciones en problemas complejos donde probar todas las combinaciones seria muy costoso.

### Parentizacion
Forma en que se agrupan las operaciones en una expresion. Cambiar la parentizacion puede modificar el costo de calculo.

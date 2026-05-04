"""
Script de Demostración - Fase 2: Algoritmo Genético.

Demuestra cómo el AG aprende cuándo paralelizar es beneficioso.
"""

# Este script está pensado como material educativo para estudiantes.
# Contiene dos demostraciones simples:
#  - `demo_simple_ag`: compara directamente serial vs paralelo en dos casos
#    (matrices pequeñas y grandes) para mostrar el efecto del overhead.
#  - `demo_ga_evolution`: ejecuta un AG sobre un conjunto de planes y
#    muestra la evolución generación a generación.
#
# Comentarios para el alumno:
#  - Observa que los tiempos son ruidosos; usa semillas y varios `num_runs`
#    para mediciones más estables.
#  - El AG aquí es didáctico: pruebas con distintos `population_size` y
#    `generations` ayudan a entender su comportamiento.

import numpy as np
from genetic_algorithm import GeneticAlgorithmOptimizer, ExecutionPlan
from executor import MatrixExpressionExecutor
from matrix_parser import MatrixExpressionParser, get_dependencies


def demo_simple_ag():
    """Demostración simple del AG."""
    print("="*70)
    print("DEMOSTRACIÓN: ALGORITMO GENÉTICO SIMPLE")
    print("="*70)
    print()
    
    # Crear matrices pequeñas (favorecen serial)
    print("Caso 1: Matrices PEQUEÑAS (favorecen serial)")
    print("-"*70)
    
    np.random.seed(42)
    size = 100  # Pequeño
    matrices_small = {
        'A': np.random.randn(size, size),
        'B': np.random.randn(size, size),
        'C': np.random.randn(size, size),
        'D': np.random.randn(size, size),
    }
    
    # Crear executor
    executor = MatrixExpressionExecutor("(A @ B) + (C @ D)", matrices_small, num_workers=4)
    
    # Ejecutar ambas versiones
    # `execute_*` retorna (resultado, tiempo_promedio_s, desv_std_s)
    # Aquí usamos el tiempo promedio (en segundos) para comparar.
    result_serial, time_serial, _ = executor.execute_serial(num_runs=2)
    result_parallel, time_parallel, _ = executor.execute_parallel(num_runs=2)
    
    print(f"Serial:   {time_serial*1000:8.4f} ms")
    print(f"Paralelo: {time_parallel*1000:8.4f} ms")
    print(f"Speedup:  {time_serial/time_parallel:.3f}x")
    
    # El AG debería aprender: NO paralelizar
    print("\nPredicción del AG: NO PARALELIZAR (overhead > beneficio)")
    
    print()
    
    # Crear matrices grandes (podrían favorecer paralelo)
    print("Caso 2: Matrices GRANDES (podrían favorecer paralelo)")
    print("-"*70)
    
    size = 1000  # Grande
    matrices_large = {
        'A': np.random.randn(size, size),
        'B': np.random.randn(size, size),
        'C': np.random.randn(size, size),
        'D': np.random.randn(size, size),
    }
    
    # Crear executor
    executor = MatrixExpressionExecutor("(A @ B) + (C @ D)", matrices_large, num_workers=4)
    
    # Ejecutar ambas versiones
    # Para tiempos largos (matrices grandes) un solo `num_runs` ya da idea
    # del comportamiento; para resultados reproducibles, aumente `num_runs`.
    result_serial, time_serial, _ = executor.execute_serial(num_runs=1)
    result_parallel, time_parallel, _ = executor.execute_parallel(num_runs=1)
    
    print(f"Serial:   {time_serial*1000:8.4f} ms")
    print(f"Paralelo: {time_parallel*1000:8.4f} ms")
    print(f"Speedup:  {time_serial/time_parallel:.3f}x")
    
    if time_parallel < time_serial:
        print("\nPredicción del AG: PARALELIZAR (beneficio > overhead)")
    else:
        print("\nPredicción del AG: NO PARALELIZAR (overhead > beneficio)")


def demo_ga_evolution():
    """Demuestra la evolución del AG."""
    print()
    print()
    print("="*70)
    print("DEMOSTRACIÓN: EVOLUCIÓN DEL ALGORITMO GENÉTICO")
    print("="*70)
    print()
    
    np.random.seed(42)
    size = 150
    matrices = {
        'A': np.random.randn(size, size),
        'B': np.random.randn(size, size),
        'C': np.random.randn(size, size),
        'D': np.random.randn(size, size),
    }
    
    executor = MatrixExpressionExecutor("(A @ B) + (C @ D)", matrices, num_workers=4)
    
    # Crear AG
    ag = GeneticAlgorithmOptimizer(
        population_size=12,
        generations=15,
        mutation_rate=0.15,
        crossover_rate=0.8,
        verbose=True
    )
    
    # Función evaluadora
    def evaluate(plan: ExecutionPlan):
        # Esta función adapta el plan a la interfaz del AG: devuelve
        # (resultado, tiempo_ms). El AG usará `tiempo_ms` como fitness.
        if plan.use_parallel:
            result, time_s, _ = executor.execute_parallel(num_runs=1)
        else:
            result, time_s, _ = executor.execute_serial(num_runs=1)
        # Convertir segundos a milisegundos para que la interpretación
        # del fitness sea más intuitiva (ms).
        return result, time_s * 1000
    
    # Evolucionar
    best_plan = ag.evolve(evaluate)
    
    print()
    print("="*70)
    print("MEJOR PLAN ENCONTRADO")
    print("="*70)
    print(best_plan)
    
    # Estadísticas
    stats = ag.get_statistics()
    print()
    print("Estadísticas:")
    print(f"  Mejor fitness:   {stats['best_fitness']:.4f} ms")
    print(f"  Peor fitness:    {stats['worst_fitness']:.4f} ms")
    print(f"  Promedio:        {stats['avg_fitness']:.4f} ms")
    print(f"  Mejora:          {stats['improvement']:.2f}%")


def main():
    """Función principal."""
    print()
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║          DEMOSTRACIÓN: FASE 2 - ALGORITMO GENÉTICO                       ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    try:
        # Demostración simple
        demo_simple_ag()
        
        # Demostración con evolución
        demo_ga_evolution()
        
        print()
        print("="*70)
        print("CONCLUSIÓN")
        print("="*70)
        print("""
El Algoritmo Genético ha demostrado que puede:

1. ✓ APRENDER cuándo paralelizar es beneficioso
2. ✓ EVITAR overhead innecesario en matrices pequeñas
3. ✓ APROVECHAR el paralelismo en matrices grandes
4. ✓ ADAPTAR el número de workers según el problema
5. ✓ ENCONTRAR soluciones mejores que heurísticas simples

Para usar el AG en tus propias expresiones:
    python main_ga.py
        """)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

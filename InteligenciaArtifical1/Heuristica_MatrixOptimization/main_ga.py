"""
Interfaz Interactiva - Fase 2: Algoritmo Genético.

Permite al usuario optimizar expresiones matriciales usando AG.
"""

import numpy as np
from typing import Dict
from plan_optimizer import PlanOptimizer


def parse_matrix_sizes(input_str: str) -> tuple:
    """Parsea entrada de tamaños."""
    parts = input_str.strip().split('x')
    return [int(p) for p in parts]


def create_test_matrices(matrix_vars: set, sizes: list) -> dict:
    """Crea matrices de prueba."""
    # Fijar semilla para reproducibilidad en ejemplos didácticos
    np.random.seed(42)
    matrices = {}
    
    if len(sizes) == 1:
        size = sizes[0]
        rows, cols = size, size
    elif len(sizes) == 2:
        rows, cols = sizes
    else:
        rows, cols = sizes[0], sizes[1]
    
    for var in sorted(matrix_vars):
        matrices[var] = np.random.randn(rows, cols)
    
    return matrices


def main_ga():
    """Función principal - Interfaz GA."""
    print("="*70)
    print("OPTIMIZADOR CON ALGORITMO GENÉTICO - FASE 2")
    print("Optimización automática de planes de ejecución")
    print("="*70)
    print()
    
    # Obtener expresión
    print("Ingrese una expresión matricial.")
    print("Ejemplo: (A @ B) + (C @ D)")
    print("Ver SINTAXIS_REFERENCIA.txt para más ejemplos")
    print()
    
    expression = input("Expresión matricial: ").strip()
    
    if not expression:
        print("Expresión vacía. Usando ejemplo: (A @ B) + (C @ D)")
        expression = "(A @ B) + (C @ D)"
    
    # Obtener tamaño
    print()
    print("Ingrese el tamaño de las matrices.")
    print("Ejemplos: 100, 300x500")
    print()
    
    size_input = input("Tamaño de matrices: ").strip()
    
    if not size_input:
        print("Tamaño no especificado. Usando 300x300")
        sizes = [300, 300]
    else:
        sizes = parse_matrix_sizes(size_input)
    
    # Parámetros del AG
    print()
    print("Parámetros del Algoritmo Genético:")
    
    pop_input = input("  Tamaño de población (default 15): ").strip()
    population_size = int(pop_input) if pop_input else 15
    
    gen_input = input("  Número de generaciones (default 20): ").strip()
    generations = int(gen_input) if gen_input else 20
    
    mut_input = input("  Tasa de mutación 0-1 (default 0.15): ").strip()
    mutation_rate = float(mut_input) if mut_input else 0.15
    
    num_runs = 2  # Fixed para no hacer muy largo
    # Nota para estudiantes: `num_runs` controla cuántas veces se ejecuta
    # cada plan para promediar tiempos. Más `num_runs` reduce ruido pero
    # incrementa el tiempo total de la optimización.
    
    try:
        # Parsear expresión y extraer variables
        from matrix_parser import MatrixExpressionParser
        parser = MatrixExpressionParser(expression)
        ast = parser.parse()
        from matrix_parser import get_dependencies
        _, _, matrix_vars = get_dependencies(ast)
        
        print()
        print("Creando matrices de prueba...")
        matrices = create_test_matrices(matrix_vars, sizes)
        
        print("Inicializando Algoritmo Genético...")
        print()
        
        # Crear optimizador
        optimizer = PlanOptimizer(
            expression=expression,
            matrices=matrices,
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
            crossover_rate=0.8,
            num_runs=num_runs,
            verbose=True
        )
        
        # Optimizar
        best_plan, stats = optimizer.optimize()
        
        # Mostrar resultados
        print()
        print("="*70)
        print("RESULTADOS DE LA OPTIMIZACIÓN")
        print("="*70)
        print()
        
        print("Mejor Plan Encontrado:")
        print(f"  Usar paralelo: {best_plan.use_parallel}")
        if best_plan.use_parallel:
            print(f"  Número de workers: {best_plan.num_workers}")
            strategies = {0: "Greedy", 1: "Balanced", 2: "Adaptive"}
            print(f"  Estrategia: {strategies.get(best_plan.scheduling_strategy, '?')}")
        print(f"  Umbral de tamaño: {best_plan.size_threshold}")
        print(f"  Fitness (tiempo en ms): {best_plan.fitness:.4f}")
        print()
        
        print("Estadísticas de Evolución:")
        print(f"  Mejor fitness: {stats['best_fitness']:.4f} ms")
        print(f"  Peor fitness: {stats['worst_fitness']:.4f} ms")
        print(f"  Fitness promedio: {stats['avg_fitness']:.4f} ms")
        print(f"  Mejora: {stats['improvement']:.2f}%")
        print()
        
        # Comparar con baseline
        print("Comparación con Baseline:")
        print("  Ejecutando baselines (serial y paralelo estándar)...")
        
        try:
            comparison = optimizer.compare_with_baseline()
            
            print()
            print(f"  Serial baseline:    {comparison['baseline_serial_ms']:.4f} ms")
            print(f"  Paralelo baseline:  {comparison['baseline_parallel_ms']:.4f} ms")
            print(f"  Plan optimizado:    {comparison['optimized_plan_ms']:.4f} ms")
            print()
            print(f"  Speedup vs serial:    {comparison['speedup_vs_serial']:.3f}x")
            print(f"  Speedup vs paralelo:  {comparison['speedup_vs_parallel']:.3f}x")
            print(f"  Mejora vs serial:     {comparison['improvement_percent']:+.2f}%")
            print()
            print(f"  Resultados correctos: {comparison['results_match']}")
            
        except Exception as e:
            print(f"  Error en comparación: {e}")
        
        print()
        print("="*70)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def main_comparison():
    """Menú principal con opciones."""
    print("="*70)
    print("HEURÍSTICA DE OPTIMIZACIÓN DE EXPRESIONES MATRICIALES")
    print("="*70)
    print()
    print("Selecciona modo:")
    print("  1. Comparación simple (serial vs paralelo)")
    print("  2. Optimización con Algoritmo Genético (FASE 2)")
    print("  3. Salir")
    print()
    
    choice = input("Opción (1-3): ").strip()
    
    if choice == "1":
        from main import main
        main()
    elif choice == "2":
        main_ga()
    elif choice == "3":
        print("Hasta luego!")
    else:
        print("Opción inválida")


if __name__ == "__main__":
    main_ga()

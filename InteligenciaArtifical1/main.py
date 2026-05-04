"""
Script principal: Comparador de expresiones matriciales.

Uso:
    python main.py

El script permite:
1. Ingresar una expresión matricial
2. Definir tamaños de matrices
3. Generar código serial y paralelo automáticamente
4. Medir y comparar rendimiento
5. Guardar código generado
"""

import numpy as np
from executor import MatrixExpressionExecutor


def parse_matrix_sizes(input_str: str) -> tuple:
    """
    Parsea entrada como "500" o "100x200x300" para tamaños de matrices.
    
    Args:
        input_str: String con tamaño(s)
        
    Returns:
        Tupla de tamaños
    """
    parts = input_str.strip().split('x')
    return [int(p) for p in parts]


def create_test_matrices(matrix_vars: set, sizes: list) -> dict:
    """
    Crea matrices de prueba.
    
    Args:
        matrix_vars: Conjunto de nombres de variables
        sizes: Lista de tamaños [rows, cols, ...]
        
    Returns:
        Diccionario {nombre -> matriz numpy}
    """
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


def main():
    """Función principal."""
    print("="*70)
    print("COMPARADOR DE EXPRESIONES MATRICIALES")
    print("Serial vs Paralelo")
    print("="*70)
    print()
    
    # Obtener expresión
    print("Ingrese una expresión matricial.")
    print("Ejemplo: (A @ B) + (C @ D)")
    print("Operadores: @ (multiplicación matricial), + (suma), - (resta)")
    print()
    
    expression = input("Expresión matricial: ").strip()
    
    if not expression:
        print("Expresión vacía. Usando ejemplo: (A @ B) + (C @ D)")
        expression = "(A @ B) + (C @ D)"
    
    # Obtener tamaño de matrices
    print()
    print("Ingrese el tamaño de las matrices.")
    print("Ejemplos: 100 (100x100), 200x300 (200 filas, 300 columnas)")
    print()
    
    size_input = input("Tamaño de matrices: ").strip()
    
    if not size_input:
        print("Tamaño no especificado. Usando 200x200")
        sizes = [200, 200]
    else:
        sizes = parse_matrix_sizes(size_input)
    
    try:
        # Crear executor
        print()
        print("Parseando expresión...")
        executor = MatrixExpressionExecutor(expression, {}, num_workers=4)
        
        print("Creando matrices de prueba...")
        matrices = create_test_matrices(executor.matrix_vars, sizes)
        
        # Actualizar executor con matrices
        executor.matrices = matrices
        
        print("Compilando código...")
        executor._compile_code()
        
        # Ejecutar comparación
        results = executor.compare(num_runs=3)
        
        # Guardar código
        print()
        save = input("¿Desea guardar el código generado? (s/n): ").strip().lower()
        
        if save == 's':
            filename = input("Nombre del archivo (sin extensión): ").strip()
            if filename:
                executor.save_code(filename)
        
        # Mostrar resumen
        print()
        print("="*70)
        print("RESUMEN")
        print("="*70)
        print(f"Expresión: {results['expression']}")
        print(f"Tamaño de matrices: {sizes[0]}x{sizes[1] if len(sizes) > 1 else sizes[0]}")
        print(f"Tiempo serial: {results['time_serial_avg']*1000:.4f} ms")
        print(f"Tiempo paralelo: {results['time_parallel_avg']*1000:.4f} ms")
        print(f"Speedup: {results['speedup']:.3f}x")
        print(f"Mejora: {results['improvement_percent']:+.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

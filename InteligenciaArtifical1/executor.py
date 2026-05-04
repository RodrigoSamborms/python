"""
Ejecutor de expresiones matriciales.

Ejecuta versiones serial y paralela, midiendo tiempos.
"""

import numpy as np
from typing import Dict, Tuple
import time
import sys

from matrix_parser import MatrixExpressionParser, get_dependencies
from code_generator import CodeGeneratorSerial, CodeGeneratorParallel


class MatrixExpressionExecutor:
    """Ejecuta expresiones matriciales en versión serial y paralela."""
    
    def __init__(self, expression: str, matrices: Dict[str, np.ndarray], 
                 num_workers: int = 4):
        """
        Inicializa el ejecutor.
        
        Args:
            expression: Expresión matricial como string
            matrices: Diccionario {nombre -> matriz numpy}
            num_workers: Número de workers para paralelismo
        """
        self.expression = expression
        self.matrices = matrices
        self.num_workers = num_workers
        
        # Parsear expresión
        parser = MatrixExpressionParser(expression)
        self.ast = parser.parse()
        self.ops_list, self.graph, self.matrix_vars = get_dependencies(self.ast)
        
        # Generar código
        self.gen_serial = CodeGeneratorSerial(self.ast, self.matrix_vars)
        self.gen_parallel = CodeGeneratorParallel(self.ast, self.matrix_vars, num_workers)
        
        self.code_serial = self.gen_serial.generate()
        self.code_parallel = self.gen_parallel.generate()
        
        # Ejecutables compilados
        self.serial_namespace = {}
        self.parallel_namespace = {}
        
        self._compile_code()
    
    def _compile_code(self):
        """Compila el código Python."""
        # Compilar código serial
        exec(self.code_serial, self.serial_namespace)
        
        # Compilar código paralelo
        exec(self.code_parallel, self.parallel_namespace)
    
    def execute_serial(self, num_runs: int = 3) -> Tuple[np.ndarray, float, float]:
        """
        Ejecuta la versión serial.
        
        Args:
            num_runs: Número de ejecuciones para promediar
            
        Returns:
            Tupla (resultado, tiempo_promedio, tiempo_desv_est)
        """
        times = []
        result = None
        
        execute_func = self.serial_namespace['execute_serial']
        
        for _ in range(num_runs):
            result, elapsed = execute_func(self.matrices)
            times.append(elapsed)
        
        avg_time = np.mean(times)
        std_time = np.std(times)
        
        return result, avg_time, std_time
    
    def execute_parallel(self, num_runs: int = 3) -> Tuple[np.ndarray, float, float]:
        """
        Ejecuta la versión paralela.
        
        Args:
            num_runs: Número de ejecuciones para promediar
            
        Returns:
            Tupla (resultado, tiempo_promedio, tiempo_desv_est)
        """
        times = []
        result = None
        
        execute_func = self.parallel_namespace['execute_parallel']
        
        for _ in range(num_runs):
            result, elapsed = execute_func(self.matrices, self.num_workers)
            times.append(elapsed)
        
        avg_time = np.mean(times)
        std_time = np.std(times)
        
        return result, avg_time, std_time
    
    def compare(self, num_runs: int = 3, verbose: bool = True) -> Dict:
        """
        Ejecuta ambas versiones y compara resultados.
        
        Args:
            num_runs: Número de ejecuciones para promediar
            verbose: Si imprimir resultados
            
        Returns:
            Diccionario con resultados de comparación
        """
        print(f"\n{'='*70}")
        print(f"EXPRESIÓN: {self.expression}")
        print(f"{'='*70}\n")
        
        # Matrices info
        print("Matrices de entrada:")
        for name, matrix in self.matrices.items():
            print(f"  {name}: shape={matrix.shape}, dtype={matrix.dtype}")
        print()
        
        # Ejecutar serial
        print(f"Ejecutando versión SERIAL ({num_runs} ejecuciones)...")
        result_serial, time_serial_avg, time_serial_std = self.execute_serial(num_runs)
        print(f"  Tiempo promedio: {time_serial_avg*1000:.4f} ms (±{time_serial_std*1000:.4f} ms)")
        print()
        
        # Ejecutar paralelo
        print(f"Ejecutando versión PARALELA ({num_runs} ejecuciones, {self.num_workers} workers)...")
        result_parallel, time_parallel_avg, time_parallel_std = self.execute_parallel(num_runs)
        print(f"  Tiempo promedio: {time_parallel_avg*1000:.4f} ms (±{time_parallel_std*1000:.4f} ms)")
        print()
        
        # Comparar resultados
        results_match = np.allclose(result_serial, result_parallel)
        
        # Calcular métricas
        speedup = time_serial_avg / time_parallel_avg
        improvement = ((time_serial_avg - time_parallel_avg) / time_serial_avg) * 100
        
        print(f"{'='*70}")
        print("RESULTADOS:")
        print(f"{'='*70}")
        print(f"Resultados coinciden: {results_match}")
        if not results_match:
            print(f"  Diferencia máxima: {np.max(np.abs(result_serial - result_parallel))}")
        print()
        print(f"Speedup (serial/paralelo): {speedup:.3f}x")
        print(f"Mejora: {improvement:+.2f}%")
        
        if speedup > 1.0:
            print(f"  ✓ La versión PARALELA es {speedup:.2f}x más rápida")
        elif speedup < 1.0:
            print(f"  ✗ La versión SERIAL es {1/speedup:.2f}x más rápida")
        else:
            print(f"  ≈ Rendimiento similar")
        print()
        
        return {
            'expression': self.expression,
            'time_serial_avg': time_serial_avg,
            'time_serial_std': time_serial_std,
            'time_parallel_avg': time_parallel_avg,
            'time_parallel_std': time_parallel_std,
            'speedup': speedup,
            'improvement_percent': improvement,
            'results_match': results_match,
            'result_serial': result_serial,
            'result_parallel': result_parallel
        }
    
    def save_code(self, base_filename: str):
        """
        Guarda el código generado en archivos.
        
        Args:
            base_filename: Nombre base (sin extensión)
        """
        # Guardar código serial
        with open(f"{base_filename}_serial.py", 'w') as f:
            f.write("# CÓDIGO GENERADO AUTOMÁTICAMENTE - VERSIÓN SERIAL\n")
            f.write(f"# Expresión: {self.expression}\n\n")
            f.write(self.code_serial)
        
        # Guardar código paralelo
        with open(f"{base_filename}_parallel.py", 'w') as f:
            f.write("# CÓDIGO GENERADO AUTOMÁTICAMENTE - VERSIÓN PARALELA\n")
            f.write(f"# Expresión: {self.expression}\n\n")
            f.write(self.code_parallel)
        
        print(f"Código guardado:")
        print(f"  - {base_filename}_serial.py")
        print(f"  - {base_filename}_parallel.py")


# Ejemplos de uso
if __name__ == "__main__":
    # Crear matrices de prueba
    print("Creando matrices de prueba...")
    np.random.seed(42)
    
    size = 500
    matrices = {
        'A': np.random.randn(size, size),
        'B': np.random.randn(size, size),
        'C': np.random.randn(size, size),
        'D': np.random.randn(size, size),
    }
    
    # Ejemplo 1: Expresión simple
    expr1 = "(A @ B) + (C @ D)"
    executor1 = MatrixExpressionExecutor(expr1, matrices, num_workers=4)
    results1 = executor1.compare(num_runs=3)
    
    # Guardar código generado
    executor1.save_code("output_ejemplo1")
    
    print("\n" + "="*70)
    print("ARCHIVOS GENERADOS:")
    print("="*70)
    print("Puedes revisar los archivos:")
    print("  - output_ejemplo1_serial.py")
    print("  - output_ejemplo1_parallel.py")

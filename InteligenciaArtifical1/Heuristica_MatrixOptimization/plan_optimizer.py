"""
Evaluador de Planes de Ejecución.

Integra el Algoritmo Genético con el executor para evaluar planes reales.
"""

# Notas educativas:
# - `ExecutionPlanEvaluator` conecta el AG con el ejecutor real.
# - Para estudiantes: esta clase encapsula la medición real del tiempo
#   de ejecución por plan. Se utiliza en el AG como "función objetivo".
# - La función `evaluate` devuelve `(resultado, tiempo_ms)` donde `tiempo_ms`
#   es el tiempo promedio medido para el plan; el AG usa este valor como fitness.

import numpy as np
from typing import Tuple, Dict
from genetic_algorithm import ExecutionPlan
from executor import MatrixExpressionExecutor


class ExecutionPlanEvaluator:
    """
    Evaluador que ejecuta planes de forma real y mide su rendimiento.
    
    Integra:
    - Executor: Ejecuta código generado
    - ExecutionPlan: Planes candidatos del AG
    """
    
    def __init__(self,
                 expression: str,
                 matrices: Dict,
                 num_runs: int = 2,
                 verbose: bool = False):
        """
        Inicializa el evaluador.
        
        Args:
            expression: Expresión matricial
            matrices: Diccionario de matrices
            num_runs: Ejecuciones por plan (para promediar)
            verbose: Mostrar detalles
        """
        self.expression = expression
        self.matrices = matrices
        self.num_runs = num_runs
        self.verbose = verbose
        
        # Cache de resultados para evitar re-evaluar planes idénticos
        self.cache: Dict[Tuple, Tuple] = {}
    
    def evaluate(self, plan: ExecutionPlan) -> Tuple:
        """
        Evalúa un plan ejecutándolo realmente.
        
        Args:
            plan: Plan a evaluar
        
        Returns:
            Tupla (resultado, tiempo_promedio_ms)
        """
        # Crear clave de caché (basada en la expresión y nombres de matrices)
        cache_key = (self.expression, tuple(sorted(self.matrices.keys())))
        
        try:
            # Si el plan es serial, usar executor directo
            # Nota: `execute_serial` retorna (resultado, tiempo_promedio_s, std_s)
            # por eso desempaquetamos correctamente y convertimos a ms.
            if not plan.use_parallel:
                executor = MatrixExpressionExecutor(
                    self.expression,
                    self.matrices,
                    num_workers=1  # No importa, no se usa
                )
                
                # Ejecutar serial
                # `time_ms` viene en segundos, convertimos a ms al retornar
                result, time_ms, _ = executor.execute_serial(num_runs=self.num_runs)
                
                if self.verbose:
                    print(f"  Plan SERIAL: {time_ms*1000:.2f} ms")
                
                return result, time_ms * 1000  # Convertir a ms
            
            # Si el plan es paralelo, usar executor con num_workers del plan
            else:
                executor = MatrixExpressionExecutor(
                    self.expression,
                    self.matrices,
                    num_workers=plan.num_workers
                )
                
                # Ejecutar paralelo
                # `execute_parallel` también retorna (result, avg_s, std_s)
                result, time_ms, _ = executor.execute_parallel(num_runs=self.num_runs)
                
                if self.verbose:
                    print(f"  Plan PARALELO ({plan.num_workers} workers): {time_ms*1000:.2f} ms")
                
                return result, time_ms * 1000  # Convertir a ms
        
        except Exception as e:
            if self.verbose:
                print(f"  Error evaluando plan: {e}")
            raise


class PlanOptimizer:
    """
    Optimizador que combina AG con evaluación real.
    
    Flujo:
    1. AG genera planes candidatos
    2. Evaluador ejecuta cada plan y mide rendimiento
    3. AG evoluciona basándose en resultados reales
    4. Repite hasta convergencia
    """
    
    def __init__(self,
                 expression: str,
                 matrices: Dict,
                 population_size: int = 15,
                 generations: int = 20,
                 mutation_rate: float = 0.15,
                 crossover_rate: float = 0.8,
                 num_runs: int = 2,
                 verbose: bool = True):
        """
        Inicializa el optimizador.
        
        Args:
            expression: Expresión matricial
            matrices: Diccionario de matrices
            population_size: Tamaño de población AG
            generations: Generaciones AG
            mutation_rate: Tasa de mutación
            crossover_rate: Tasa de cruce
            num_runs: Ejecuciones por plan
            verbose: Mostrar progreso
        """
        from genetic_algorithm import GeneticAlgorithmOptimizer
        
        self.expression = expression
        self.matrices = matrices
        self.num_runs = num_runs
        self.verbose = verbose
        
        # Crear evaluador
        self.evaluator = ExecutionPlanEvaluator(
            expression=expression,
            matrices=matrices,
            num_runs=num_runs,
            verbose=False  # El AG maneja verbose
        )
        
        # Crear AG
        self.ag = GeneticAlgorithmOptimizer(
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            elite_size=max(2, population_size // 5),
            verbose=verbose
        )
    
    def optimize(self) -> Tuple[ExecutionPlan, Dict]:
        """
        Ejecuta la optimización completa.
        
        Returns:
            Tupla (mejor_plan, estadísticas)
        """
        # Función evaluadora para el AG
        def evaluate_plan(plan: ExecutionPlan) -> Tuple:
            return self.evaluator.evaluate(plan)
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("OPTIMIZACIÓN DE PLAN DE EJECUCIÓN")
            print(f"{'='*70}")
            print(f"Expresión: {self.expression}")
            print(f"Tamaño de matrices: {list(self.matrices.values())[0].shape if self.matrices else 'N/A'}")
            print(f"{'='*70}\n")
        
        # Evolucionar AG
        best_plan = self.ag.evolve(evaluate_plan)
        
        # Obtener estadísticas
        stats = self.ag.get_statistics()
        stats['best_plan'] = best_plan
        stats['recommendation'] = self.ag.recommend_plan(self.expression, 0)
        
        return best_plan, stats
    
    def compare_with_baseline(self) -> Dict:
        """
        Compara el plan optimizado contra la ejecución serial y paralela base.
        
        Returns:
            Diccionario con comparación
        """
        if not self.ag.best_individuals:
            return {"error": "No optimization completed"}
        
        best_plan = self.ag.best_individuals[-1]
        
        # Ejecutar baseline serial
        executor = MatrixExpressionExecutor(
            self.expression,
            self.matrices,
            num_workers=4  # Parámetro ignorado para serial
        )
        
        result_serial, time_serial = executor.execute_serial(num_runs=self.num_runs)
        result_parallel, time_parallel = executor.execute_parallel(num_runs=self.num_runs)
        
        # Ejecutar plan optimizado
        result_opt, time_opt = self.evaluator.evaluate(best_plan)
        
        # Calcular mejoras
        speedup_vs_serial = time_serial / time_opt if time_opt > 0 else 0
        speedup_vs_parallel = time_parallel / time_opt if time_opt > 0 else 0
        improvement = ((time_serial - time_opt) / time_serial * 100) if time_serial > 0 else 0
        
        comparison = {
            'expression': self.expression,
            'baseline_serial_ms': time_serial * 1000,
            'baseline_parallel_ms': time_parallel * 1000,
            'optimized_plan_ms': time_opt,
            'optimized_plan': best_plan,
            'speedup_vs_serial': speedup_vs_serial,
            'speedup_vs_parallel': speedup_vs_parallel,
            'improvement_percent': improvement,
            'results_match': (
                np.allclose(result_serial, result_opt) and
                np.allclose(result_parallel, result_opt)
            )
        }
        
        return comparison


# Ejemplo de uso
if __name__ == "__main__":
    import numpy as np
    
    print("Evaluador de Planes de Ejecución")
    print("="*70)
    
    # Crear matrices de prueba
    np.random.seed(42)
    size = 200
    matrices = {
        'A': np.random.randn(size, size),
        'B': np.random.randn(size, size),
        'C': np.random.randn(size, size),
        'D': np.random.randn(size, size),
    }
    
    # Crear optimizador
    optimizer = PlanOptimizer(
        expression="(A @ B) + (C @ D)",
        matrices=matrices,
        population_size=10,
        generations=10,
        num_runs=1,
        verbose=True
    )
    
    # Optimizar
    best_plan, stats = optimizer.optimize()
    
    print(f"\nMejor plan encontrado:")
    print(f"  {best_plan}")
    
    print(f"\nEstadísticas:")
    for key, value in stats.items():
        if key != 'best_plan' and key != 'recommendation':
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")

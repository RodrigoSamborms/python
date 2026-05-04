"""
Algoritmo Genético para Optimización de Planes de Ejecución.

Este módulo implementa un AG que aprende cuándo paralelizar es beneficioso
para ejecutar expresiones matriciales de forma eficiente.
"""
"""
Genetic Algorithm implementation for execution plan optimization.

This module defines an ExecutionPlan (chromosome) and a GeneticAlgorithmOptimizer
that evolves plans to minimize execution time of matrix expressions.

Notes for students:
- A chromosome (`ExecutionPlan`) encodes configuration choices that affect
    performance (e.g., whether to parallelize, number of workers).
- The GA operators implemented here are intentionally simple (tournament
    selection, uniform crossover, single-gene mutation, elitism). They are
    easy to understand and reason about, which makes this module suitable for
    educational purposes.

Key concepts to look at while reading the code:
1. Representation: how a solution (plan) is converted into a vector
     (`to_vector` / `from_vector`). This is crucial for implementing
     crossover and mutation.
2. Fitness evaluation: the GA treats execution time as the fitness to minimize.
3. Selection / Crossover / Mutation: simple operators that balance exploration
     and exploitation. Students can experiment by changing tournament size,
     mutation rate, or crossover strategy.

Practical notes:
- Fitness evaluation may be noisy (timing variability). In real experiments
    increase `num_runs` when measuring each plan to obtain stable averages.
- Parallel evaluation of population is possible (not implemented here) and
    can speed up GA runs when many cores are available.
"""

import numpy as np
from typing import List, Tuple, Dict, Callable
from dataclasses import dataclass
import random


@dataclass
class ExecutionPlan:
    """Representa un plan de ejecución (cromosoma)."""
    
    # Decisión principal: paralelizar o no
    use_parallel: bool
    
    # Si se paraleliza, cuántos workers usar
    num_workers: int
    
    # Umbral de tamaño: si matriz > umbral, paralelizar
    size_threshold: int
    
    # Estrategia de scheduling (0=greedy, 1=balanced, 2=adaptive)
    scheduling_strategy: int
    
    # Fitness score (calculado después)
    fitness: float = float('inf')
    
    def __repr__(self):
        return (f"Plan(parallel={self.use_parallel}, workers={self.num_workers}, "
                f"threshold={self.size_threshold}, strategy={self.scheduling_strategy}, "
                f"fitness={self.fitness:.4f})")
    
    def to_vector(self) -> List[int]:
        """Convierte el plan a un vector de genes."""
        return [
            int(self.use_parallel),
            self.num_workers,
            self.size_threshold,
            self.scheduling_strategy
        ]
    
    @staticmethod
    def from_vector(vector: List[int]) -> 'ExecutionPlan':
        """Crea un plan desde un vector de genes."""
        return ExecutionPlan(
            use_parallel=bool(vector[0]),
            num_workers=vector[1],
            size_threshold=vector[2],
            scheduling_strategy=vector[3]
        )


class GeneticAlgorithmOptimizer:
    """
    Algoritmo Genético para optimizar planes de ejecución de expresiones matriciales.
    
    El AG busca encontrar el mejor plan que minimice:
        fitness = tiempo_total + alpha*overhead + beta*desbalance
    """
    
    def __init__(self, 
                 population_size: int = 20,
                 generations: int = 30,
                 mutation_rate: float = 0.2,
                 crossover_rate: float = 0.8,
                 elite_size: int = 3,
                 verbose: bool = True):
        """
        Inicializa el AG.
        
        Args:
            population_size: Tamaño de la población
            generations: Número de generaciones a evolucionar
            mutation_rate: Probabilidad de mutación (0-1)
            crossover_rate: Probabilidad de cruce (0-1)
            elite_size: Número de mejores individuos a preservar
            verbose: Mostrar progreso
        """
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.verbose = verbose
        
        self.population: List[ExecutionPlan] = []
        self.best_individuals: List[ExecutionPlan] = []
        self.fitness_history: List[float] = []
    
    def initialize_population(self) -> List[ExecutionPlan]:
        """Crea una población inicial aleatoria."""
        population = []
        
        for _ in range(self.population_size):
            plan = ExecutionPlan(
                use_parallel=random.choice([True, False]),
                num_workers=random.randint(1, 8),
                size_threshold=random.randint(100, 1000),
                scheduling_strategy=random.randint(0, 2)
            )
            population.append(plan)
        
        self.population = population
        return population
    
    def evaluate_fitness(self, 
                        plan: ExecutionPlan,
                        executor_func: Callable) -> float:
        """
        Evalúa el fitness de un plan.
        
        Args:
            plan: Plan a evaluar
            executor_func: Función que ejecuta el plan y retorna (resultado, tiempo)
                          Expected: executor_func(plan) -> (result, time_ms)
        
        Returns:
            Fitness score (menor es mejor)
        """
        try:
            result, time_ms = executor_func(plan)
            
            # Fitness = tiempo + penalizaciones
            # Si paralelismo es benéfico, el tiempo será bajo
            # Si no, será alto (incluyendo overhead)
            fitness = time_ms
            
            # Penalizar planes que usan muchos recursos innecesarios
            if plan.use_parallel:
                # Penalizar por overhead si paralelo no es necesario
                overhead_penalty = 0  # Se ajusta según contexto
                fitness += overhead_penalty
            
            return fitness
            
        except Exception as e:
            # Plan inválido: asignar penalización alta
            print(f"Error evaluando plan {plan}: {e}")
            return float('inf')
    
    def selection(self, 
                 population: List[ExecutionPlan],
                 fitness_scores: List[float]) -> Tuple[ExecutionPlan, ExecutionPlan]:
        """
        Selección por torneo (elige 2 padres).
        
        Args:
            population: Población actual
            fitness_scores: Scores de fitness
        
        Returns:
            Tupla (padre1, padre2)
        """
        tournament_size = 3
        
        def tournament():
            indices = random.sample(range(len(population)), tournament_size)
            best_idx = min(indices, key=lambda i: fitness_scores[i])
            return population[best_idx]
        
        parent1 = tournament()
        parent2 = tournament()
        
        return parent1, parent2
    
    def crossover(self, parent1: ExecutionPlan, parent2: ExecutionPlan) -> Tuple[ExecutionPlan, ExecutionPlan]:
        """
        Cruce uniforme: cada gen tiene 50% chance de venir de cada padre.
        
        Args:
            parent1, parent2: Padres
        
        Returns:
            Tupla (hijo1, hijo2)
        """
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        vector1 = parent1.to_vector()
        vector2 = parent2.to_vector()
        
        child_vector1 = [vector1[i] if random.random() < 0.5 else vector2[i] 
                        for i in range(len(vector1))]
        child_vector2 = [vector2[i] if random.random() < 0.5 else vector1[i] 
                        for i in range(len(vector2))]
        
        return ExecutionPlan.from_vector(child_vector1), ExecutionPlan.from_vector(child_vector2)
    
    def mutate(self, plan: ExecutionPlan) -> ExecutionPlan:
        """
        Mutación: modifica genes aleatoriamente.
        
        Args:
            plan: Plan a mutar
        
        Returns:
            Plan mutado
        """
        if random.random() > self.mutation_rate:
            return plan
        
        vector = plan.to_vector()
        gene_idx = random.randint(0, len(vector) - 1)
        
        if gene_idx == 0:  # use_parallel
            vector[0] = 1 - vector[0]  # Flip
        elif gene_idx == 1:  # num_workers
            vector[1] = random.randint(1, 8)
        elif gene_idx == 2:  # size_threshold
            vector[2] = random.randint(100, 1000)
        elif gene_idx == 3:  # scheduling_strategy
            vector[3] = random.randint(0, 2)
        
        return ExecutionPlan.from_vector(vector)
    
    def evolve(self, executor_func: Callable) -> ExecutionPlan:
        """
        Evoluciona la población a través de generaciones.
        
        Args:
            executor_func: Función evaluadora que ejecuta y mide planes
        
        Returns:
            Mejor plan encontrado
        """
        # Inicializar población
        self.initialize_population()
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("ALGORITMO GENÉTICO - FASE 2")
            print(f"{'='*70}")
            print(f"Población: {self.population_size}")
            print(f"Generaciones: {self.generations}")
            print(f"Mutation rate: {self.mutation_rate}")
            print(f"Crossover rate: {self.crossover_rate}")
            print(f"{'='*70}\n")
        
        for generation in range(self.generations):
            # Evaluar fitness de toda la población
            fitness_scores = [
                self.evaluate_fitness(plan, executor_func)
                for plan in self.population
            ]
            
            # Actualizar fitness en los planes
            for plan, fitness in zip(self.population, fitness_scores):
                plan.fitness = fitness
            
            # Encontrar mejor individuo
            best_idx = np.argmin(fitness_scores)
            best_plan = self.population[best_idx]
            best_fitness = fitness_scores[best_idx]
            
            self.fitness_history.append(best_fitness)
            self.best_individuals.append(best_plan)
            
            if self.verbose and (generation % 5 == 0 or generation == self.generations - 1):
                avg_fitness = np.mean(fitness_scores)
                print(f"Gen {generation+1:3d} | Mejor: {best_fitness:8.2f} | "
                      f"Promedio: {avg_fitness:8.2f} | "
                      f"Plan: {best_plan}")
            
            # Seleccionar élite (mejores individuos se preservan)
            elite_indices = np.argsort(fitness_scores)[:self.elite_size]
            elite = [self.population[i] for i in elite_indices]
            
            # Crear nueva población
            new_population = elite.copy()
            
            while len(new_population) < self.population_size:
                # Selección y reproducción
                parent1, parent2 = self.selection(self.population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                
                # Mutación
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Truncar a tamaño original
            self.population = new_population[:self.population_size]
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("EVOLUCIÓN COMPLETADA")
            print(f"{'='*70}\n")
        
        return self.best_individuals[-1]
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas de la evolución."""
        if not self.fitness_history:
            return {}
        
        return {
            'best_fitness': min(self.fitness_history),
            'worst_fitness': max(self.fitness_history),
            'avg_fitness': np.mean(self.fitness_history),
            'std_fitness': np.std(self.fitness_history),
            'improvement': (self.fitness_history[0] - self.fitness_history[-1]) / self.fitness_history[0] * 100,
            'generations': len(self.fitness_history)
        }
    
    def recommend_plan(self, 
                      expression: str,
                      matrix_size: int) -> Dict:
        """
        Recomienda un plan de ejecución para una expresión y tamaño dado.
        
        Args:
            expression: Expresión matricial
            matrix_size: Tamaño de matrices
        
        Returns:
            Diccionario con recomendación
        """
        best_plan = self.best_individuals[-1] if self.best_individuals else None
        
        if best_plan is None:
            return {"recommendation": "No evolution completed yet"}
        
        recommendation = {
            'expression': expression,
            'matrix_size': matrix_size,
            'use_parallel': best_plan.use_parallel,
            'num_workers': best_plan.num_workers if best_plan.use_parallel else 1,
            'size_threshold': best_plan.size_threshold,
            'scheduling_strategy': best_plan.scheduling_strategy,
            'fitness': best_plan.fitness,
        }
        
        # Generar consejo legible
        if best_plan.use_parallel:
            strategy_names = {0: "Greedy", 1: "Balanced", 2: "Adaptive"}
            strategy = strategy_names.get(best_plan.scheduling_strategy, "Unknown")
            advice = (f"PARALELIZAR con {best_plan.num_workers} workers. "
                     f"Estrategia: {strategy}. "
                     f"Paralelizar si tamaño > {best_plan.size_threshold}.")
        else:
            advice = "EJECUTAR SECUENCIAL. El overhead de paralelismo no compensa."
        
        recommendation['advice'] = advice
        
        return recommendation


# Ejemplo de uso
if __name__ == "__main__":
    print("Módulo de Algoritmo Genético cargado correctamente")
    
    # Crear un AG simple para demostración
    ag = GeneticAlgorithmOptimizer(
        population_size=10,
        generations=5,
        mutation_rate=0.2,
        crossover_rate=0.8
    )
    
    # Función evaluadora de prueba
    def dummy_evaluator(plan: ExecutionPlan) -> Tuple:
        # Fitness simulado basado en el plan
        if plan.use_parallel:
            time = 20 + random.random() * 10  # Paralelo puede ser más lento en matrices pequeñas
        else:
            time = 15 + random.random() * 5  # Serial es más rápido para matrices pequeñas
        
        return (None, time)
    
    # Evolucionar
    best = ag.evolve(dummy_evaluator)
    
    print(f"\nMejor plan encontrado:")
    print(best)
    
    print(f"\nEstadísticas:")
    stats = ag.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    print(f"\nRecomendación:")
    rec = ag.recommend_plan("(A @ B) + (C @ D)", 500)
    for key, value in rec.items():
        print(f"  {key}: {value}")

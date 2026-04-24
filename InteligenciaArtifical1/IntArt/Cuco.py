"""
Implementacion didactica de Cuckoo Search (Algoritmo del Cuco) para optimizacion.

Objetivo:
- Minimizar una funcion f(x), con x = (x1, ..., xd).
- Seguir paso a paso el pseudocodigo clasico:
  1) Generar cuco aleatorio con vuelo de Levy.
  2) Evaluar fitness.
  3) Elegir nido j aleatorio.
  4) Reemplazar j si el nuevo cuco es mejor.
  5) Abandonar fraccion pa de peores nidos y regenerarlos.
  6) Mantener las mejores soluciones.
  7) Ordenar y actualizar G-Best.
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple


Vector = List[float]


def sphere(x: Vector) -> float:
	"""Funcion objetivo de ejemplo (minimizacion): f(x) = sum(x_i^2)."""
	return sum(value * value for value in x)


def rastrigin(x: Vector) -> float:
	"""Funcion Rastrigin (minimo global en x=0, f=0)."""
	n = len(x)
	return 10 * n + sum((value * value - 10 * math.cos(2 * math.pi * value)) for value in x)


def rosenbrock(x: Vector) -> float:
	"""Funcion Rosenbrock (minimo global en x=[1,...,1], f=0)."""
	return sum(
		100 * ((x[i + 1] - x[i] ** 2) ** 2) + (1 - x[i]) ** 2
		for i in range(len(x) - 1)
	)


def ackley(x: Vector) -> float:
	"""Funcion Ackley (minimo global en x=0, f=0)."""
	n = len(x)
	sum_sq = sum(value * value for value in x)
	sum_cos = sum(math.cos(2 * math.pi * value) for value in x)
	term1 = -20 * math.exp(-0.2 * math.sqrt(sum_sq / n))
	term2 = -math.exp(sum_cos / n)
	return term1 + term2 + 20 + math.e


def get_objective_functions() -> Dict[str, Callable[[Vector], float]]:
	"""Mapa de funciones objetivo disponibles para el usuario."""
	return {
		"sphere": sphere,
		"rastrigin": rastrigin,
		"rosenbrock": rosenbrock,
		"ackley": ackley,
	}


def clamp_vector(x: Vector, lower: float, upper: float) -> Vector:
	"""Recorta un vector para mantenerlo dentro de los limites."""
	return [max(lower, min(upper, value)) for value in x]


def levy_step(beta: float = 1.5) -> float:
	"""
	Genera un paso de Levy usando el metodo de Mantegna.

	Valores tipicos:
	- beta en (1, 2], comunmente 1.5.
	"""
	sigma_u_numerator = math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
	sigma_u_denominator = math.gamma((1 + beta) / 2) * beta * (2 ** ((beta - 1) / 2))
	sigma_u = (sigma_u_numerator / sigma_u_denominator) ** (1 / beta)

	u = random.gauss(0, sigma_u)
	v = random.gauss(0, 1)

	# Evita division por cero en casos extremadamente raros.
	if abs(v) < 1e-12:
		v = 1e-12

	return u / (abs(v) ** (1 / beta))


@dataclass
class CuckooSearch:
	"""Implementacion sencilla y didactica del algoritmo Cuckoo Search."""

	objective: Callable[[Vector], float]
	n_nests: int = 20
	dimension: int = 2
	lower_bound: float = -5.0
	upper_bound: float = 5.0
	max_iterations: int = 100
	alpha: float = 0.01
	beta: float = 1.5
	pa: float = 0.25
	seed: int | None = 42
	verbose: bool = True

	def __post_init__(self) -> None:
		if self.seed is not None:
			random.seed(self.seed)

		self.nests: List[Vector] = [self._random_nest() for _ in range(self.n_nests)]
		self.fitness: List[float] = [self.objective(nest) for nest in self.nests]

		best_index = min(range(self.n_nests), key=lambda i: self.fitness[i])
		self.g_best: Vector = self.nests[best_index][:]
		self.g_best_fitness: float = self.fitness[best_index]

	def _random_nest(self) -> Vector:
		"""Construye un nido aleatorio dentro de los limites de busqueda."""
		return [
			random.uniform(self.lower_bound, self.upper_bound)
			for _ in range(self.dimension)
		]

	def _new_solution_from_levy(self, base_nest: Vector) -> Vector:
		"""
		Paso 1 del pseudocodigo:
		x_nuevo = x_i + alpha * L(s, lambda)
		"""
		new_nest = [
			base_nest[d] + self.alpha * levy_step(self.beta)
			for d in range(self.dimension)
		]
		return clamp_vector(new_nest, self.lower_bound, self.upper_bound)

	def _abandon_worst_nests(self) -> None:
		"""Paso 5: abandonar una fraccion pa de peores nidos y regenerarlos."""
		n_abandon = max(1, int(self.pa * self.n_nests))

		# Orden ascendente de fitness (menor es mejor).
		sorted_indices = sorted(range(self.n_nests), key=lambda i: self.fitness[i])
		worst_indices = sorted_indices[-n_abandon:]

		for idx in worst_indices:
			# Regeneramos alrededor de la mejor solucion actual usando Levy.
			self.nests[idx] = self._new_solution_from_levy(self.g_best)
			self.fitness[idx] = self.objective(self.nests[idx])

	def optimize(self) -> Tuple[Vector, float]:
		"""Ejecuta Cuckoo Search y retorna (mejor_solucion, mejor_fitness)."""
		for t in range(1, self.max_iterations + 1):
			# 1) Elegir un nido i al azar y generar un cuco con vuelo de Levy.
			i = random.randrange(self.n_nests)
			x_new = self._new_solution_from_levy(self.nests[i])

			# 2) Evaluar la calidad de la nueva solucion.
			f_new = self.objective(x_new)

			# 3) Elegir un nido j al azar.
			j = random.randrange(self.n_nests)

			# 4) En minimizacion, "mejor" significa menor fitness.
			if f_new < self.fitness[j]:
				self.nests[j] = x_new
				self.fitness[j] = f_new

			# 5) Abandono de nidos peores y regeneracion.
			self._abandon_worst_nests()

			# 6 y 7) Mantener mejores, ordenar y actualizar G-Best.
			sorted_indices = sorted(range(self.n_nests), key=lambda idx: self.fitness[idx])
			best_idx = sorted_indices[0]
			if self.fitness[best_idx] < self.g_best_fitness:
				self.g_best = self.nests[best_idx][:]
				self.g_best_fitness = self.fitness[best_idx]

			if self.verbose and (t == 1 or t % 10 == 0 or t == self.max_iterations):
				print(f"Iteracion {t:03d} | Mejor fitness actual: {self.g_best_fitness:.8f}")

		return self.g_best, self.g_best_fitness


def parse_args() -> argparse.Namespace:
	"""Argumentos para elegir funciones objetivo y parametros del algoritmo."""
	parser = argparse.ArgumentParser(description="Cuckoo Search didactico")
	parser.add_argument(
		"--objective",
		default="all",
		help="Funcion objetivo: sphere, rastrigin, rosenbrock, ackley o all",
	)
	parser.add_argument("--iterations", type=int, default=120, help="Iteraciones maximas")
	parser.add_argument("--nests", type=int, default=25, help="Numero de nidos")
	parser.add_argument("--dimension", type=int, default=5, help="Dimension de la solucion")
	parser.add_argument("--seed", type=int, default=42, help="Semilla aleatoria")
	parser.add_argument("--quiet", action="store_true", help="Oculta progreso por iteracion")
	return parser.parse_args()


def run_experiment(
	objective_name: str,
	objective_fn: Callable[[Vector], float],
	iterations: int,
	nests: int,
	dimension: int,
	seed: int,
	verbose: bool,
) -> None:
	"""Ejecuta una corrida de Cuckoo Search para una funcion objetivo."""
	print(f"\nFuncion objetivo: {objective_name}")
	print("-" * 40)

	model = CuckooSearch(
		objective=objective_fn,
		n_nests=nests,
		dimension=dimension,
		lower_bound=-10,
		upper_bound=10,
		max_iterations=iterations,
		alpha=0.08,
		beta=1.5,
		pa=0.25,
		seed=seed,
		verbose=verbose,
	)

	best_solution, best_fitness = model.optimize()

	print("Resultado final")
	print(f"Mejor nido (x*): {[round(value, 6) for value in best_solution]}")
	print(f"Mejor valor f(x*): {best_fitness:.10f}")


def demo() -> None:
	"""Demostracion lista para ejecutar desde terminal."""
	args = parse_args()
	objectives = get_objective_functions()

	if args.objective == "all":
		selected = ["sphere", "rastrigin", "rosenbrock", "ackley"]
	else:
		selected = [args.objective.lower()]

	invalid = [name for name in selected if name not in objectives]
	if invalid:
		print("Funcion objetivo invalida.")
		print(f"Opciones disponibles: {', '.join(objectives.keys())}, all")
		return

	print("Cuckoo Search - Ejemplo didactico")
	print(f"Nidos={args.nests}, Dimension={args.dimension}, Iteraciones={args.iterations}")
	print(f"Funciones a evaluar: {', '.join(selected)}")

	for objective_name in selected:
		run_experiment(
			objective_name=objective_name,
			objective_fn=objectives[objective_name],
			iterations=args.iterations,
			nests=args.nests,
			dimension=args.dimension,
			seed=args.seed,
			verbose=not args.quiet,
		)


if __name__ == "__main__":
	demo()

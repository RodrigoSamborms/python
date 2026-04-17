"""
Implementacion del algoritmo Harmony Search (Busqueda Armonica).

Incluye:
- Clase reusable para problemas de minimizacion o maximizacion.
- Parametros clasicos: HMS, HMCR, PAR y BW.
- Ejemplo de uso con la funcion esfera.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple
import random


ObjectiveFunction = Callable[[Sequence[float]], float]


@dataclass
class Harmony:
	"""Representa una armonia (solucion candidata) y su fitness."""

	values: List[float]
	fitness: float


class HarmonySearch:
	"""Implementacion general de Harmony Search."""

	def __init__(
		self,
		objective_function: ObjectiveFunction,
		bounds: Sequence[Tuple[float, float]],
		harmony_memory_size: int = 20,
		harmony_memory_consideration_rate: float = 0.9,
		pitch_adjustment_rate: float = 0.3,
		bandwidth: float = 0.05,
		maximize: bool = False,
		seed: int | None = None,
	) -> None:
		self.objective_function = objective_function
		self.bounds = list(bounds)
		self.dimension = len(self.bounds)

		self.hms = harmony_memory_size
		self.hmcr = harmony_memory_consideration_rate
		self.par = pitch_adjustment_rate
		self.bw = bandwidth
		self.maximize = maximize

		self.rng = random.Random(seed)
		self.harmony_memory: List[Harmony] = []

		self._validate_params()

	def _validate_params(self) -> None:
		if self.dimension == 0:
			raise ValueError("'bounds' no puede estar vacio.")

		for i, (low, high) in enumerate(self.bounds):
			if low >= high:
				raise ValueError(f"Limites invalidos en dimension {i}: ({low}, {high}).")

		if self.hms < 2:
			raise ValueError("'harmony_memory_size' debe ser >= 2.")
		if not 0.0 <= self.hmcr <= 1.0:
			raise ValueError("'harmony_memory_consideration_rate' debe estar en [0, 1].")
		if not 0.0 <= self.par <= 1.0:
			raise ValueError("'pitch_adjustment_rate' debe estar en [0, 1].")
		if self.bw < 0.0:
			raise ValueError("'bandwidth' no puede ser negativo.")

	def _evaluate(self, values: Sequence[float]) -> float:
		score = self.objective_function(values)
		return -score if self.maximize else score

	@staticmethod
	def _clip(value: float, low: float, high: float) -> float:
		return min(max(value, low), high)

	def _create_random_harmony(self) -> Harmony:
		values = [self.rng.uniform(low, high) for low, high in self.bounds]
		return Harmony(values=values, fitness=self._evaluate(values))

	def _initialize_memory(self) -> None:
		self.harmony_memory = [self._create_random_harmony() for _ in range(self.hms)]
		self.harmony_memory.sort(key=lambda h: h.fitness)

	def _select_from_memory(self, dimension_idx: int) -> float:
		return self.rng.choice(self.harmony_memory).values[dimension_idx]

	def _pitch_adjust(self, value: float, dimension_idx: int) -> float:
		low, high = self.bounds[dimension_idx]
		range_size = high - low
		delta = self.rng.uniform(-self.bw * range_size, self.bw * range_size)
		return self._clip(value + delta, low, high)

	def _improvise_new_harmony(self) -> Harmony:
		new_values: List[float] = []

		for i, (low, high) in enumerate(self.bounds):
			if self.rng.random() < self.hmcr:
				value = self._select_from_memory(i)
				if self.rng.random() < self.par:
					value = self._pitch_adjust(value, i)
			else:
				value = self.rng.uniform(low, high)

			new_values.append(self._clip(value, low, high))

		return Harmony(values=new_values, fitness=self._evaluate(new_values))

	def _update_memory(self, candidate: Harmony) -> bool:
		worst = self.harmony_memory[-1]
		if candidate.fitness < worst.fitness:
			self.harmony_memory[-1] = candidate
			self.harmony_memory.sort(key=lambda h: h.fitness)
			return True
		return False

	def optimize(self, iterations: int = 1000, verbose: bool = False) -> Tuple[List[float], float]:
		if iterations <= 0:
			raise ValueError("'iterations' debe ser > 0.")

		self._initialize_memory()
		report_step = max(1, iterations // 10)

		for it in range(1, iterations + 1):
			candidate = self._improvise_new_harmony()
			self._update_memory(candidate)

			if verbose and (it % report_step == 0 or it == 1 or it == iterations):
				best = self.harmony_memory[0]
				display_fitness = -best.fitness if self.maximize else best.fitness
				print(f"Iteracion {it:5d} | Mejor fitness: {display_fitness:.8f}")

		best = self.harmony_memory[0]
		best_fitness = -best.fitness if self.maximize else best.fitness
		return best.values, best_fitness


def sphere_function(x: Sequence[float]) -> float:
	"""Funcion esfera de prueba: minimo global en x=0 con f(x)=0."""
	return sum(v * v for v in x)


if __name__ == "__main__":
	# Ejemplo de uso: minimizar esfera en 5 dimensiones.
	search_bounds = [(-5.0, 5.0)] * 5

	hs = HarmonySearch(
		objective_function=sphere_function,
		bounds=search_bounds,
		harmony_memory_size=30,
		harmony_memory_consideration_rate=0.9,
		pitch_adjustment_rate=0.35,
		bandwidth=0.02,
		maximize=False,
		seed=42,
	)

	best_x, best_f = hs.optimize(iterations=2000, verbose=True)

	print("\nResultado final:")
	print("Mejor solucion encontrada:", best_x)
	print("Mejor valor de la funcion objetivo:", best_f)

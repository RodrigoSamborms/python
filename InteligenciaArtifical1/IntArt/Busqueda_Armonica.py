"""
Implementacion academica del algoritmo Harmony Search (Busqueda Armonica).

Este modulo implementa una version general del algoritmo metaheuristico
inspirado en el proceso de improvisacion musical. El objetivo es optimizar
una funcion (por defecto, minimizacion) dentro de limites definidos para cada
variable de decision.

Componentes clave modelados en esta implementacion:
1. Harmony Memory (HM):
   Conjunto de soluciones candidatas de tamano fijo.
2. Harmony Memory Consideration Rate (HMCR):
   Probabilidad de elegir valores existentes en HM para construir una nueva
   armonia.
3. Pitch Adjustment Rate (PAR):
   Probabilidad de ajustar localmente un valor tomado de HM.
4. Randomize Rate (RR):
   Probabilidad de generar una armonia totalmente aleatoria en una iteracion,
   reforzando exploracion global.
5. Harmony Memory Update:
   Regla de reemplazo del peor elemento de HM cuando la nueva armonia es
   superior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple
import random


# Tipo para representar una funcion objetivo:
# recibe un vector de decision y retorna su costo/fitness.
ObjectiveFunction = Callable[[Sequence[float]], float]


@dataclass
class Harmony:
	"""Estructura para almacenar una armonia y su valor objetivo asociado."""

	values: List[float]
	fitness: float


class BusquedaArmonica:
	"""
	Implementacion del algoritmo Harmony Search (HS).

	Parametros
	----------
	objective_function : Callable[[Sequence[float]], float]
		Funcion a optimizar. Por convencion, un valor menor es mejor en
		minimizacion.
	bounds : Sequence[Tuple[float, float]]
		Limites (minimo, maximo) por variable de decision.
	harmony_memory_size : int
		Cantidad de armonias almacenadas en la memoria (HMS).
	harmony_memory_consideration_rate : float
		HMCR en [0, 1]. Controla uso de valores de la memoria.
	pitch_adjustment_rate : float
		PAR en [0, 1]. Controla ajuste local de valores tomados de memoria.
	bandwidth : float
		Magnitud maxima de ajuste local (analogia al "desplazamiento de tono").
	randomize_rate : float
		RR en [0, 1]. Probabilidad de generar armonia completamente aleatoria.
	maximize : bool
		Si True, transforma el problema en maximizacion.
	seed : int | None
		Semilla para reproducibilidad experimental.
	"""

	def __init__(
		self,
		objective_function: ObjectiveFunction,
		bounds: Sequence[Tuple[float, float]],
		harmony_memory_size: int = 20,
		harmony_memory_consideration_rate: float = 0.9,
		pitch_adjustment_rate: float = 0.3,
		bandwidth: float = 0.05,
		randomize_rate: float = 0.05,
		maximize: bool = False,
		seed: int | None = None,
	) -> None:
		self.objective_function = objective_function
		self.bounds = list(bounds)
		self.dimension = len(self.bounds)

		self.harmony_memory_size = harmony_memory_size
		self.hmcr = harmony_memory_consideration_rate
		self.par = pitch_adjustment_rate
		self.bandwidth = bandwidth
		self.randomize_rate = randomize_rate
		self.maximize = maximize

		# Generador pseudoaleatorio encapsulado para control experimental.
		self.rng = random.Random(seed)

		self._validar_parametros()
		self.harmony_memory: List[Harmony] = []

	def _validar_parametros(self) -> None:
		"""Valida coherencia de parametros para evitar estados inconsistentes."""
		if self.dimension == 0:
			raise ValueError("'bounds' no puede estar vacio.")

		for i, (low, high) in enumerate(self.bounds):
			if low >= high:
				raise ValueError(
					f"Limites invalidos en dimension {i}: ({low}, {high})."
				)

		if self.harmony_memory_size < 2:
			raise ValueError("'harmony_memory_size' debe ser >= 2.")
		if not 0.0 <= self.hmcr <= 1.0:
			raise ValueError("'harmony_memory_consideration_rate' debe estar en [0, 1].")
		if not 0.0 <= self.par <= 1.0:
			raise ValueError("'pitch_adjustment_rate' debe estar en [0, 1].")
		if self.bandwidth < 0.0:
			raise ValueError("'bandwidth' no puede ser negativo.")
		if not 0.0 <= self.randomize_rate <= 1.0:
			raise ValueError("'randomize_rate' debe estar en [0, 1].")

	def _evaluar(self, values: Sequence[float]) -> float:
		"""
		Evalua la funcion objetivo.

		Para soportar maximizacion sin duplicar logica, se usa la transformacion:
		minimizar f(x)              si maximize = False
		minimizar -f(x)             si maximize = True
		"""
		score = self.objective_function(values)
		return -score if self.maximize else score

	def _clip(self, value: float, low: float, high: float) -> float:
		"""Recorta un valor al intervalo permitido [low, high]."""
		return min(max(value, low), high)

	def _crear_armonia_aleatoria(self) -> Harmony:
		"""Crea una armonia completamente aleatoria dentro de los limites."""
		values = [self.rng.uniform(low, high) for low, high in self.bounds]
		fitness = self._evaluar(values)
		return Harmony(values=values, fitness=fitness)

	def _inicializar_harmony_memory(self) -> None:
		"""
		Inicializa la Harmony Memory (HM) con soluciones aleatorias.

		Esta fase provee diversidad inicial para evitar sesgo prematuro hacia
		regiones reducidas del espacio de busqueda.
		"""
		self.harmony_memory = [
			self._crear_armonia_aleatoria() for _ in range(self.harmony_memory_size)
		]
		self.harmony_memory.sort(key=lambda h: h.fitness)

	def _seleccionar_valor_desde_memoria(self, idx_dimension: int) -> float:
		"""Selecciona un valor existente en HM para una dimension especifica."""
		harmony = self.rng.choice(self.harmony_memory)
		return harmony.values[idx_dimension]

	def _ajustar_pitch(self, value: float, idx_dimension: int) -> float:
		"""
		Realiza ajuste local (pitch adjustment) sobre una variable.

		El ajuste se modela como:
			x' = x + delta
		donde delta ~ U(-bandwidth * rango, +bandwidth * rango).

		Escalar por el rango de la variable evita que el ajuste sea demasiado
		pequeno o demasiado agresivo entre dimensiones con diferentes escalas.
		"""
		low, high = self.bounds[idx_dimension]
		value_range = high - low
		delta = self.rng.uniform(-self.bandwidth * value_range, self.bandwidth * value_range)
		adjusted = value + delta
		return self._clip(adjusted, low, high)

	def _improvisar_nueva_armonia(self) -> Harmony:
		"""
		Crea una nueva armonia mediante las reglas HS.

		Mecanismo de generacion:
		1. Con probabilidad randomize_rate, se crea una armonia totalmente
		   aleatoria (exploracion global fuerte).
		2. En caso contrario, para cada dimension:
		   2.1 Con probabilidad HMCR, tomar valor desde HM.
		   2.2 Si se tomo de HM, con probabilidad PAR aplicar pitch adjustment.
		   2.3 Con probabilidad (1 - HMCR), generar valor aleatorio dentro del
			   dominio (exploracion puntual por dimension).
		"""
		if self.rng.random() < self.randomize_rate:
			return self._crear_armonia_aleatoria()

		new_values: List[float] = []

		for i, (low, high) in enumerate(self.bounds):
			if self.rng.random() < self.hmcr:
				# Harmony Memory Consideration (HMC): reutiliza experiencia previa.
				value = self._seleccionar_valor_desde_memoria(i)

				# Pitch Adjustment Rate (PAR): refinamiento local alrededor
				# de soluciones ya prometedoras.
				if self.rng.random() < self.par:
					value = self._ajustar_pitch(value, i)
			else:
				# Randomization por dimension: inyecta diversidad para escapar
				# de optimos locales y regiones sobreexplotadas.
				value = self.rng.uniform(low, high)

			new_values.append(self._clip(value, low, high))

		new_fitness = self._evaluar(new_values)
		return Harmony(values=new_values, fitness=new_fitness)

	def _actualizar_harmony_memory(self, candidate: Harmony) -> bool:
		"""
		Aplica la regla de reemplazo (Harmony Memory Update).

		Estrategia:
		- La HM se mantiene ordenada ascendentemente por fitness.
		- Si el candidato es mejor que la peor armonia de la HM, reemplaza a
		  la peor y se reordena.

		Retorna
		-------
		bool
			True si hubo actualizacion, False en caso contrario.
		"""
		worst = self.harmony_memory[-1]
		if candidate.fitness < worst.fitness:
			self.harmony_memory[-1] = candidate
			self.harmony_memory.sort(key=lambda h: h.fitness)
			return True
		return False

	def optimizar(self, iterations: int = 1000, verbose: bool = False) -> Tuple[List[float], float]:
		"""
		Ejecuta el proceso iterativo de Harmony Search.

		Parametros
		----------
		iterations : int
			Numero de improvisaciones/iteraciones del algoritmo.
		verbose : bool
			Si True, imprime progreso periodico.

		Retorna
		-------
		(best_values, best_fitness_original)
			Mejor solucion encontrada y su valor en escala original de la
			funcion objetivo (sin signo invertido).
		"""
		if iterations <= 0:
			raise ValueError("'iterations' debe ser > 0.")

		self._inicializar_harmony_memory()
		report_step = max(1, iterations // 10)

		for it in range(1, iterations + 1):
			candidate = self._improvisar_nueva_armonia()
			self._actualizar_harmony_memory(candidate)

			if verbose and (it % report_step == 0 or it == 1 or it == iterations):
				best = self.harmony_memory[0]
				display_fitness = -best.fitness if self.maximize else best.fitness
				print(f"Iteracion {it:5d} | Mejor fitness: {display_fitness:.8f}")

		best = self.harmony_memory[0]
		best_fitness_original = -best.fitness if self.maximize else best.fitness
		return best.values, best_fitness_original

#Funcion Objetivo de prueba: Funcion Esfera (Sphere Function)
def funcion_esfera(x: Sequence[float]) -> float:
	"""
	Funcion de prueba clasica (Sphere Function).

	Minimo global en x = 0 con f(x) = 0.
	"""
	return sum(v * v for v in x)


if __name__ == "__main__":
	# Ejemplo de uso orientado a practica academica.
	# Problema: minimizar funcion esfera en 5 dimensiones.
	limites = [(-5.0, 5.0)] * 5

	hs = BusquedaArmonica(
		objective_function=funcion_esfera,
		bounds=limites,
		harmony_memory_size=30,
		harmony_memory_consideration_rate=0.90,
		pitch_adjustment_rate=0.35,
		bandwidth=0.02,
		randomize_rate=0.08,
		maximize=False,
		seed=42,
	)

	mejor_x, mejor_f = hs.optimizar(iterations=2000, verbose=True)

	print("\nResultado final:")
	print("Mejor solucion encontrada:", mejor_x)
	print("Mejor valor de la funcion objetivo:", mejor_f)

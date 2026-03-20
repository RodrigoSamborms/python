"""Algoritmo de Colonia de Hormigas (ACO) para un problema tipo TSP.

Este módulo implementa, de forma explícita y comentada, las fórmulas:

1) Búsqueda de alimento (probabilidad de transición):
   Pij_k(t) = [tau(i,j)^alpha * eta(i,j)^beta] /
			  sum_{l en Ni_k}[tau(i,l)^alpha * eta(i,l)^beta]

2) Heurística de arista:
   eta(i,j) = 1 / d(i,j)

3) Actualización de feromonas:
   tau(i,j) <- (1 - rho) * tau(i,j) + sum_k delta_tau(i,j,k)

4) Depósito por hormiga:
   delta_tau(i,j,k) = Q / L[k]  si la hormiga k usó el arco (i,j), en otro caso 0
"""

from __future__ import annotations

import random
from typing import List, Sequence, Tuple


Matriz = List[List[float]]
Camino = List[int]


def construir_eta(distancias: Sequence[Sequence[float]]) -> Matriz:
	"""Construye la matriz heurística eta usando la fórmula eta(i,j) = 1 / d(i,j)."""
	n = len(distancias)
	eta: Matriz = [[0.0 for _ in range(n)] for _ in range(n)]

	for i in range(n):
		for j in range(n):
			if i != j and distancias[i][j] > 0:
				# --- Fórmula solicitada: Heurística de la arista ---
				# eta(i,j) := 1 / d[i,j]
				eta[i][j] = 1.0 / distancias[i][j]
			else:
				eta[i][j] = 0.0

	return eta


def calcular_probabilidades_transicion(
	nodo_actual: int,
	no_visitados: Sequence[int],
	feromonas: Sequence[Sequence[float]],
	eta: Sequence[Sequence[float]],
	alpha: float,
	beta: float,
) -> List[float]:
	"""Calcula las probabilidades de ir desde i a cada j en N_i^k."""
	pesos = []
	for j in no_visitados:
		# --- Fórmula solicitada: numerador de Pij_k(t) ---
		# tau[i,j](t)^alpha * eta[i,j]^beta
		w = (feromonas[nodo_actual][j] ** alpha) * (eta[nodo_actual][j] ** beta)
		pesos.append(w)

	suma_pesos = sum(pesos)

	if suma_pesos == 0:
		# Si no hay información útil, usar distribución uniforme
		return [1.0 / len(no_visitados)] * len(no_visitados)

	# --- Fórmula solicitada: Pij_k(t) completa ---
	# Pij_k(t) = (tau[i,j]^alpha * eta[i,j]^beta) /
	#            sum_{l en Ni_k}(tau[i,l]^alpha * eta[i,l]^beta)
	return [w / suma_pesos for w in pesos]


def seleccionar_siguiente_nodo(
	nodo_actual: int,
	no_visitados: Sequence[int],
	feromonas: Sequence[Sequence[float]],
	eta: Sequence[Sequence[float]],
	alpha: float,
	beta: float,
) -> int:
	"""Selecciona el siguiente nodo con ruleta probabilística."""
	probabilidades = calcular_probabilidades_transicion(
		nodo_actual, no_visitados, feromonas, eta, alpha, beta
	)
	return random.choices(list(no_visitados), weights=probabilidades, k=1)[0]


def longitud_camino(camino: Sequence[int], distancias: Sequence[Sequence[float]]) -> float:
	"""Longitud total de un camino cerrado (ciclo)."""
	total = 0.0
	for i in range(len(camino) - 1):
		total += distancias[camino[i]][camino[i + 1]]
	return total


def arcos_usados(camino: Sequence[int]) -> set[Tuple[int, int]]:
	"""Regresa el conjunto de arcos dirigidos usados en el camino."""
	usados: set[Tuple[int, int]] = set()
	for i in range(len(camino) - 1):
		a, b = camino[i], camino[i + 1]
		usados.add((a, b))
		usados.add((b, a))  # Se considera grafo no dirigido
	return usados


def actualizar_feromonas(
	feromonas: Matriz,
	caminos: Sequence[Camino],
	longitudes: Sequence[float],
	rho: float,
	q: float,
) -> None:
	"""Actualiza la matriz de feromonas según evaporación + depósitos."""
	n = len(feromonas)

	# Precalcular arcos usados por cada hormiga para evaluar used_arc(i,j,k)
	arcos_por_hormiga = [arcos_usados(camino) for camino in caminos]

	nueva_feromona: Matriz = [[0.0 for _ in range(n)] for _ in range(n)]

	for i in range(n):
		for j in range(n):
			if i == j:
				continue

			# --- Fórmula solicitada: sum_k delta_tau(i,j,k) ---
			suma_delta = 0.0
			for k in range(len(caminos)):
				# --- Fórmula solicitada: delta_tau(i,j,k) ---
				# delta_tau(i,j,k) = Q / L[k]  si used_arc(i,j,k), si no 0
				if (i, j) in arcos_por_hormiga[k]:
					suma_delta += q / longitudes[k]

			# --- Fórmula solicitada: tau_update(i,j,t) ---
			# tau(i,j) <- (1 - rho) * tau(i,j) + sum_k delta_tau(i,j,k)
			nueva_feromona[i][j] = (1.0 - rho) * feromonas[i][j] + suma_delta

	# Reemplazar matriz de feromonas
	for i in range(n):
		for j in range(n):
			if i != j:
				feromonas[i][j] = nueva_feromona[i][j]


def construir_camino_hormiga(
	distancias: Sequence[Sequence[float]],
	feromonas: Sequence[Sequence[float]],
	eta: Sequence[Sequence[float]],
	alpha: float,
	beta: float,
) -> Camino:
	"""Construye un camino para una hormiga, iniciando en nodo aleatorio."""
	n = len(distancias)
	inicio = random.randrange(n)
	camino: Camino = [inicio]
	no_visitados = set(range(n))
	no_visitados.remove(inicio)

	actual = inicio
	while no_visitados:
		siguiente = seleccionar_siguiente_nodo(
			actual,
			list(no_visitados),
			feromonas,
			eta,
			alpha,
			beta,
		)
		camino.append(siguiente)
		no_visitados.remove(siguiente)
		actual = siguiente

	# Cerrar ciclo regresando al origen
	camino.append(inicio)
	return camino


def aco_tsp(
	distancias: Sequence[Sequence[float]],
	n_hormigas: int = 20,
	iteraciones: int = 100,
	alpha: float = 1.0,
	beta: float = 2.0,
	rho: float = 0.5,
	q: float = 100.0,
	tau_inicial: float = 1.0,
	semilla: int | None = 42,
	mostrar_iteraciones: bool = False,
) -> Tuple[Camino, float]:
	"""Ejecuta ACO y devuelve (mejor_camino, mejor_longitud)."""
	if semilla is not None:
		random.seed(semilla)

	n = len(distancias)
	feromonas: Matriz = [[0.0 if i == j else tau_inicial for j in range(n)] for i in range(n)]
	eta = construir_eta(distancias)

	mejor_camino: Camino | None = None
	mejor_longitud = float("inf")

	for iteracion in range(1, iteraciones + 1):
		caminos_iteracion: List[Camino] = []
		longitudes_iteracion: List[float] = []

		for _ in range(n_hormigas):
			camino = construir_camino_hormiga(distancias, feromonas, eta, alpha, beta)
			longitud = longitud_camino(camino, distancias)
			caminos_iteracion.append(camino)
			longitudes_iteracion.append(longitud)

			if longitud < mejor_longitud:
				mejor_longitud = longitud
				mejor_camino = camino

		if mostrar_iteraciones and longitudes_iteracion:
			mejor_iteracion = min(longitudes_iteracion)
			promedio_iteracion = sum(longitudes_iteracion) / len(longitudes_iteracion)
			print(
				f"Iteración {iteracion:03d} | "
				f"Mejor iteración: {mejor_iteracion:.4f} | "
				f"Promedio iteración: {promedio_iteracion:.4f} | "
				f"Mejor global: {mejor_longitud:.4f}"
			)

		actualizar_feromonas(feromonas, caminos_iteracion, longitudes_iteracion, rho, q)

	# Por construcción siempre habrá un mejor camino
	return mejor_camino if mejor_camino is not None else [], mejor_longitud


if __name__ == "__main__":
	# Matriz de distancias de ejemplo (simétrica, diagonal en 0)
	distancias_ejemplo = [
		[0, 2, 2, 5, 7],
		[2, 0, 4, 8, 2],
		[2, 4, 0, 1, 3],
		[5, 8, 1, 0, 2],
		[7, 2, 3, 2, 0],
	]

	mejor_camino, mejor_longitud = aco_tsp(
		distancias_ejemplo,
		n_hormigas=15,
		iteraciones=120,
		alpha=1.0,
		beta=3.0,
		rho=0.4,
		q=100.0,
		tau_inicial=1.0,
		semilla=7,
		mostrar_iteraciones=True,
	)

	print("Mejor camino encontrado:", mejor_camino)
	print("Longitud del mejor camino:", round(mejor_longitud, 4))

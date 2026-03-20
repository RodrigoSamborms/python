"""Segmentación de imagen multinivel con ACO + entropía de Shannon (Kapur).

Este archivo usa el programa de hormigas `AOC.py` para reutilizar partes del ACO:
- `calcular_probabilidades_transicion` para Pij_k(t)
- `actualizar_feromonas` para tau_update y delta_tau

Objetivo: encontrar umbrales óptimos que maximicen la entropía total de Shannon
en una imagen en escala de grises, y generar una imagen segmentada.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np
from PIL import Image

import AOC


def histograma_probabilidad(imagen_gris: np.ndarray) -> np.ndarray:
	"""Devuelve el histograma normalizado (probabilidades) para 256 niveles."""
	hist = np.bincount(imagen_gris.ravel(), minlength=256).astype(np.float64)
	total = hist.sum()
	if total == 0:
		raise ValueError("La imagen no contiene píxeles válidos.")
	return hist / total


def entropia_shannon_multinivel(prob: np.ndarray, umbrales: Sequence[int]) -> float:
	"""Calcula la suma de entropías de Shannon por clase (método de Kapur)."""
	limites = [0] + sorted(int(t) for t in umbrales) + [255]
	entropia_total = 0.0
	eps = 1e-12

	for c in range(len(limites) - 1):
		inicio = limites[c]
		fin = limites[c + 1]

		if c == 0:
			segmento = prob[inicio : fin + 1]
		else:
			segmento = prob[inicio + 1 : fin + 1]

		w = float(np.sum(segmento))
		if w <= eps:
			continue

		p_norm = segmento / w
		p_norm = p_norm[p_norm > 0]
		entropia_total += -float(np.sum(p_norm * np.log(p_norm + eps)))

	return entropia_total


def construir_eta_umbral(prob: np.ndarray) -> List[List[float]]:
	"""Matriz heurística eta para transiciones entre niveles de gris.

	eta(i,j) favorece intervalos con mayor masa de probabilidad.
	"""
	n = 256
	eta = [[0.0 for _ in range(n)] for _ in range(n)]

	acum = np.cumsum(prob)
	eps = 1e-12
	for i in range(n):
		for j in range(i + 1, n):
			masa = acum[j] - (acum[i] if i >= 0 else 0.0)
			eta[i][j] = float(masa + eps)

	return eta


def construir_solucion_hormiga(
	feromonas: Sequence[Sequence[float]],
	eta: Sequence[Sequence[float]],
	n_umbral: int,
	alpha: float,
	beta: float,
) -> Tuple[List[int], List[int]]:
	"""Construye umbrales crecientes para una hormiga y retorna (umbrales, camino)."""
	camino = [0]
	actual = 0
	umbrales: List[int] = []

	for paso in range(n_umbral):
		restantes = n_umbral - paso - 1
		maximo = 254 - restantes
		candidatos = list(range(actual + 1, maximo + 1))

		if not candidatos:
			break

		# Reutilizamos directamente la fórmula Pij_k(t) implementada en AOC.py
		probabilidades = AOC.calcular_probabilidades_transicion(
			actual,
			candidatos,
			feromonas,
			eta,
			alpha,
			beta,
		)
		siguiente = random.choices(candidatos, weights=probabilidades, k=1)[0]

		umbrales.append(siguiente)
		camino.append(siguiente)
		actual = siguiente

	camino.append(255)
	return umbrales, camino


def aplicar_segmentacion_multinivel(imagen_gris: np.ndarray, umbrales: Sequence[int]) -> np.ndarray:
	"""Aplica cuantización por umbrales y devuelve la imagen segmentada."""
	umbrales_ordenados = sorted(int(t) for t in umbrales)
	clases = len(umbrales_ordenados) + 1

	valores_salida = np.linspace(0, 255, clases, dtype=np.uint8)
	salida = np.zeros_like(imagen_gris, dtype=np.uint8)

	limites = [0] + umbrales_ordenados + [255]
	for idx in range(clases):
		inf = limites[idx]
		sup = limites[idx + 1]
		if idx == 0:
			mascara = (imagen_gris >= inf) & (imagen_gris <= sup)
		else:
			mascara = (imagen_gris > inf) & (imagen_gris <= sup)
		salida[mascara] = valores_salida[idx]

	return salida


def aco_segmentacion_shannon(
	imagen_gris: np.ndarray,
	n_umbral: int = 2,
	n_hormigas: int = 20,
	iteraciones: int = 80,
	alpha: float = 1.0,
	beta: float = 2.0,
	rho: float = 0.4,
	q: float = 50.0,
	tau_inicial: float = 1.0,
	semilla: int | None = 42,
	mostrar_iteraciones: bool = True,
) -> Tuple[List[int], float, np.ndarray]:
	"""Optimiza umbrales multinivel con ACO maximizando entropía de Shannon."""
	if semilla is not None:
		random.seed(semilla)
		np.random.seed(semilla)

	prob = histograma_probabilidad(imagen_gris)
	eta = construir_eta_umbral(prob)

	n = 256
	feromonas = [[0.0 if i == j else tau_inicial for j in range(n)] for i in range(n)]

	mejores_umbrales: List[int] = []
	mejor_entropia = -float("inf")

	for it in range(1, iteraciones + 1):
		caminos: List[List[int]] = []
		longitudes_coste: List[float] = []
		entropias: List[float] = []

		for _ in range(n_hormigas):
			umbrales, camino = construir_solucion_hormiga(
				feromonas,
				eta,
				n_umbral=n_umbral,
				alpha=alpha,
				beta=beta,
			)

			if len(umbrales) != n_umbral:
				continue

			entropia = entropia_shannon_multinivel(prob, umbrales)
			entropias.append(entropia)
			caminos.append(camino)

			# AOC.update usa minimización mediante L[k].
			# Convertimos maximización de entropía a coste: L = 1 / (entropia + eps)
			longitudes_coste.append(1.0 / (entropia + 1e-12))

			if entropia > mejor_entropia:
				mejor_entropia = entropia
				mejores_umbrales = sorted(umbrales)

		if caminos:
			# Reutilizamos la actualización de feromonas de AOC.py
			AOC.actualizar_feromonas(
				feromonas=feromonas,
				caminos=caminos,
				longitudes=longitudes_coste,
				rho=rho,
				q=q,
			)

		if mostrar_iteraciones and entropias:
			print(
				f"Iteración {it:03d} | "
				f"Mejor iteración (H): {max(entropias):.6f} | "
				f"Promedio (H): {float(np.mean(entropias)):.6f} | "
				f"Mejor global (H): {mejor_entropia:.6f} | "
				f"Umbrales globales: {mejores_umbrales}"
			)

	segmentada = aplicar_segmentacion_multinivel(imagen_gris, mejores_umbrales)
	return mejores_umbrales, mejor_entropia, segmentada


def cargar_grises(path: str) -> np.ndarray:
	"""Carga una imagen y la convierte a escala de grises (uint8)."""
	img = Image.open(path).convert("L")
	return np.array(img, dtype=np.uint8)


def guardar_imagen(path: str, imagen_gris: np.ndarray) -> None:
	"""Guarda una imagen en escala de grises."""
	Image.fromarray(imagen_gris, mode="L").save(path)


def construir_ruta_salida_automatica(ruta_entrada: str) -> str:
	"""Construye: NombreArchivo_Output_Segmentada.Extension en la misma carpeta."""
	ruta = Path(ruta_entrada)
	extension = ruta.suffix

	if not extension:
		extension = ".png"

	nombre_salida = f"{ruta.stem}_Output_Segmentada{extension}"
	ruta_salida = ruta.with_name(nombre_salida)
	return str(ruta_salida)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Segmentación multinivel con ACO usando entropía de Shannon."
	)
	parser.add_argument("entrada", help="Ruta de imagen de entrada")
	parser.add_argument("--umbrales", type=int, default=2, help="Número de umbrales")
	parser.add_argument("--hormigas", type=int, default=20, help="Número de hormigas")
	parser.add_argument("--iteraciones", type=int, default=80, help="Número de iteraciones")
	parser.add_argument("--alpha", type=float, default=1.0, help="Peso de feromona")
	parser.add_argument("--beta", type=float, default=2.0, help="Peso heurístico")
	parser.add_argument("--rho", type=float, default=0.4, help="Evaporación")
	parser.add_argument("--q", type=float, default=50.0, help="Constante de depósito")
	parser.add_argument("--semilla", type=int, default=42, help="Semilla aleatoria")
	parser.add_argument(
		"--silencioso",
		action="store_true",
		help="No imprimir resultados por iteración",
	)

	args = parser.parse_args()

	imagen = cargar_grises(args.entrada)
	umbrales, entropia, seg = aco_segmentacion_shannon(
		imagen_gris=imagen,
		n_umbral=args.umbrales,
		n_hormigas=args.hormigas,
		iteraciones=args.iteraciones,
		alpha=args.alpha,
		beta=args.beta,
		rho=args.rho,
		q=args.q,
		semilla=args.semilla,
		mostrar_iteraciones=not args.silencioso,
	)
	ruta_salida = construir_ruta_salida_automatica(args.entrada)

	guardar_imagen(ruta_salida, seg)

	print("\nResultado final")
	print("Umbrales óptimos:", umbrales)
	print("Entropía de Shannon (Kapur):", round(entropia, 6))
	print("Imagen segmentada guardada en:", ruta_salida)


if __name__ == "__main__":
	main()

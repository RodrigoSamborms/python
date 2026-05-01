"""Mejora de contraste con CLAHE + Cuckoo Search por linea de comandos.

Flujo:
1) Cargar imagen y convertir a escala de grises.
2) Optimizar parametros de CLAHE con algoritmo del cuco.
3) Aplicar CLAHE con parametros optimos.
4) Evaluar antes/despues con metricas (entropia y, si existen, MSE/PSNR/SSIM).
"""

from __future__ import annotations

import argparse
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
from PIL import Image, ImageFilter


Array = np.ndarray


def entropy_8bit(image: Array) -> float:
	hist = np.bincount(image.ravel(), minlength=256).astype(np.float64)
	prob = hist / np.sum(hist)
	prob = prob[prob > 0]
	return float(-np.sum(prob * np.log2(prob)))


def sobel_energy(image: Array) -> float:
	img = image.astype(np.float32)
	p = np.pad(img, pad_width=1, mode="edge")

	gx = (
		-1 * p[:-2, :-2] + 1 * p[:-2, 2:]
		- 2 * p[1:-1, :-2] + 2 * p[1:-1, 2:]
		- 1 * p[2:, :-2] + 1 * p[2:, 2:]
	)
	gy = (
		-1 * p[:-2, :-2] - 2 * p[:-2, 1:-1] - 1 * p[:-2, 2:]
		+ 1 * p[2:, :-2] + 2 * p[2:, 1:-1] + 1 * p[2:, 2:]
	)
	magnitude = np.hypot(gx, gy)
	return float(np.mean(magnitude))


def noise_estimate(image: Array) -> float:
	pil_img = Image.fromarray(image)
	blurred = np.array(pil_img.filter(ImageFilter.GaussianBlur(radius=1.0)), dtype=np.float32)
	residual = image.astype(np.float32) - blurred
	return float(np.var(residual))


def normalize_metrics(
	enhanced: Array,
	original: Array,
) -> tuple[float, float, float, float, float]:
	h_hat = entropy_8bit(enhanced) / 8.0
	sigma_hat = float(np.std(enhanced)) / 127.5
	e_hat = sobel_energy(enhanced) / 255.0
	n_hat = noise_estimate(enhanced) / (255.0 * 255.0)
	delta_mu_hat = abs(float(np.mean(enhanced)) - float(np.mean(original))) / 255.0

	h_hat = min(max(h_hat, 0.0), 1.0)
	sigma_hat = min(max(sigma_hat, 0.0), 1.0)
	e_hat = min(max(e_hat, 0.0), 1.0)
	n_hat = min(max(n_hat, 0.0), 1.0)
	delta_mu_hat = min(max(delta_mu_hat, 0.0), 1.0)
	return h_hat, sigma_hat, e_hat, n_hat, delta_mu_hat


def clahe_numpy(
	image: Array,
	clip_limit: float,
	grid_x: int,
	grid_y: int,
) -> Array:
	"""Implementacion simplificada de CLAHE por bloques (didactica)."""
	if image.dtype != np.uint8:
		raise ValueError("La imagen debe ser uint8")

	h, w = image.shape
	grid_x = max(2, int(grid_x))
	grid_y = max(2, int(grid_y))

	tile_h = math.ceil(h / grid_y)
	tile_w = math.ceil(w / grid_x)
	out = np.zeros_like(image)

	for ty in range(grid_y):
		for tx in range(grid_x):
			y0 = ty * tile_h
			y1 = min((ty + 1) * tile_h, h)
			x0 = tx * tile_w
			x1 = min((tx + 1) * tile_w, w)
			if y0 >= y1 or x0 >= x1:
				continue

			tile = image[y0:y1, x0:x1]
			hist = np.bincount(tile.ravel(), minlength=256).astype(np.int64)

			clip_count = max(1, int(clip_limit * tile.size / 256.0))
			excess = np.maximum(hist - clip_count, 0)
			hist = np.minimum(hist, clip_count)

			total_excess = int(np.sum(excess))
			if total_excess > 0:
				base = total_excess // 256
				rem = total_excess % 256
				hist += base
				if rem > 0:
					hist[:rem] += 1

			cdf = np.cumsum(hist).astype(np.float64)
			cdf_min = cdf[np.nonzero(cdf)][0] if np.any(cdf > 0) else 0
			denom = max(1.0, tile.size - cdf_min)
			lut = np.clip((cdf - cdf_min) * 255.0 / denom, 0, 255).astype(np.uint8)
			out[y0:y1, x0:x1] = lut[tile]

	return out


def levy_step(beta: float = 1.5) -> float:
	sigma_u_numerator = math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
	sigma_u_denominator = math.gamma((1 + beta) / 2) * beta * (2 ** ((beta - 1) / 2))
	sigma_u = (sigma_u_numerator / sigma_u_denominator) ** (1 / beta)
	u = random.gauss(0, sigma_u)
	v = random.gauss(0, 1)
	if abs(v) < 1e-12:
		v = 1e-12
	return u / (abs(v) ** (1 / beta))


@dataclass
class CuckooCLAHE:
	objective: Callable[[np.ndarray], float]
	nests: int = 20
	iterations: int = 40
	alpha: float = 0.35
	beta: float = 1.5
	pa: float = 0.25
	seed: int | None = 42
	clip_min: float = 1.0
	clip_max: float = 10.0
	grid_min: int = 4
	grid_max: int = 16
	verbose: bool = True

	def __post_init__(self) -> None:
		if self.seed is not None:
			random.seed(self.seed)
			np.random.seed(self.seed)

		self.population = np.array([self._random_nest() for _ in range(self.nests)], dtype=np.float64)
		self.fitness = np.array([self.objective(n) for n in self.population], dtype=np.float64)
		best_idx = int(np.argmax(self.fitness))
		self.best_nest = self.population[best_idx].copy()
		self.best_fitness = float(self.fitness[best_idx])

	def _random_nest(self) -> np.ndarray:
		clip = random.uniform(self.clip_min, self.clip_max)
		gx = random.uniform(self.grid_min, self.grid_max)
		gy = random.uniform(self.grid_min, self.grid_max)
		return np.array([clip, gx, gy], dtype=np.float64)

	def _clip_nest(self, nest: np.ndarray) -> np.ndarray:
		nest[0] = np.clip(nest[0], self.clip_min, self.clip_max)
		nest[1] = np.clip(nest[1], self.grid_min, self.grid_max)
		nest[2] = np.clip(nest[2], self.grid_min, self.grid_max)
		return nest

	def _levy_move(self, base: np.ndarray) -> np.ndarray:
		step = np.array([levy_step(self.beta), levy_step(self.beta), levy_step(self.beta)], dtype=np.float64)
		candidate = base + self.alpha * step
		return self._clip_nest(candidate)

	def _abandon_worst(self) -> None:
		n_abandon = max(1, int(self.pa * self.nests))
		worst_indices = np.argsort(self.fitness)[:n_abandon]
		for idx in worst_indices:
			new_nest = self._levy_move(self.best_nest.copy())
			self.population[idx] = new_nest
			self.fitness[idx] = self.objective(new_nest)

	def optimize(self) -> tuple[np.ndarray, float]:
		for t in range(1, self.iterations + 1):
			i = random.randrange(self.nests)
			new_nest = self._levy_move(self.population[i].copy())
			new_fit = self.objective(new_nest)

			j = random.randrange(self.nests)
			if new_fit > self.fitness[j]:
				self.population[j] = new_nest
				self.fitness[j] = new_fit

			self._abandon_worst()

			best_idx = int(np.argmax(self.fitness))
			if self.fitness[best_idx] > self.best_fitness:
				self.best_fitness = float(self.fitness[best_idx])
				self.best_nest = self.population[best_idx].copy()

			if self.verbose and (t == 1 or t % 10 == 0 or t == self.iterations):
				print(f"Iteracion {t:03d} | Mejor J: {self.best_fitness:.6f}")

		return self.best_nest, self.best_fitness


def load_optional_metrics_from_repo() -> tuple[Callable | None, Callable | None, Callable | None]:
	"""Carga funciones de métricas locales (MSE/PSNR/SSIM) si existen."""
	metrics_dir = Path(__file__).resolve().parent / "métricas"
	if not metrics_dir.exists():
		return None, None, None

	sys.path.insert(0, str(metrics_dir))
	try:
		from MSE import calcular_mse  # type: ignore
		from PSNR import calcular_psnr  # type: ignore
		from SSIM import calcular_ssim_global  # type: ignore
		return calcular_mse, calcular_psnr, calcular_ssim_global
	except Exception:
		return None, None, None


def to_matrix_list(image: Array) -> list[list[int]]:
	return image.astype(int).tolist()


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Optimiza CLAHE con Cuckoo Search y evalua metricas antes/despues"
	)
	parser.add_argument("--input", required=True, help="Ruta de la imagen de entrada")
	parser.add_argument("--output", default="imagen_mejorada_cuco_clahe.png", help="Ruta de imagen de salida")
	parser.add_argument("--nests", type=int, default=20, help="Numero de nidos")
	parser.add_argument("--iterations", type=int, default=40, help="Numero de iteraciones")
	parser.add_argument("--pa", type=float, default=0.25, help="Probabilidad de abandono")
	parser.add_argument("--alpha", type=float, default=0.35, help="Paso de vuelo de Levy")
	parser.add_argument("--beta", type=float, default=1.5, help="Parametro beta de Levy")
	parser.add_argument("--seed", type=int, default=42, help="Semilla aleatoria")

	parser.add_argument("--clip-min", type=float, default=1.0, help="clipLimit minimo")
	parser.add_argument("--clip-max", type=float, default=10.0, help="clipLimit maximo")
	parser.add_argument("--tile-min", type=int, default=4, help="tamano minimo de grilla")
	parser.add_argument("--tile-max", type=int, default=16, help="tamano maximo de grilla")

	parser.add_argument("--w1", type=float, default=0.35, help="Peso de entropia")
	parser.add_argument("--w2", type=float, default=0.25, help="Peso de desviacion estandar")
	parser.add_argument("--w3", type=float, default=0.25, help="Peso de energia de bordes")
	parser.add_argument("--w4", type=float, default=0.10, help="Peso de penalizacion de ruido")
	parser.add_argument("--w5", type=float, default=0.05, help="Peso de penalizacion de brillo")
	parser.add_argument("--ssim-window", type=int, default=8, help="Tamano de ventana para SSIM")
	parser.add_argument("--quiet", action="store_true", help="Oculta progreso de iteraciones")
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	input_path = Path(args.input)
	if not input_path.exists():
		raise FileNotFoundError(f"No existe la imagen de entrada: {input_path}")

	original_gray = Image.open(input_path).convert("L")
	original = np.array(original_gray, dtype=np.uint8)

	w1, w2, w3, w4, w5 = args.w1, args.w2, args.w3, args.w4, args.w5

	def objective(params: np.ndarray) -> float:
		clip = float(params[0])
		gx = int(round(params[1]))
		gy = int(round(params[2]))
		enhanced = clahe_numpy(original, clip, gx, gy)
		h_hat, sigma_hat, e_hat, n_hat, delta_mu_hat = normalize_metrics(enhanced, original)
		score = w1 * h_hat + w2 * sigma_hat + w3 * e_hat - w4 * n_hat - w5 * delta_mu_hat
		return float(score)

	model = CuckooCLAHE(
		objective=objective,
		nests=args.nests,
		iterations=args.iterations,
		alpha=args.alpha,
		beta=args.beta,
		pa=args.pa,
		seed=args.seed,
		clip_min=args.clip_min,
		clip_max=args.clip_max,
		grid_min=args.tile_min,
		grid_max=args.tile_max,
		verbose=not args.quiet,
	)

	best_params, best_score = model.optimize()
	best_clip = float(best_params[0])
	best_grid_x = int(round(best_params[1]))
	best_grid_y = int(round(best_params[2]))

	enhanced = clahe_numpy(original, best_clip, best_grid_x, best_grid_y)
	output_path = Path(args.output)
	Image.fromarray(enhanced).save(output_path)

	h0 = entropy_8bit(original)
	h1 = entropy_8bit(enhanced)

	print("\n=== Resultado Cuckoo + CLAHE ===")
	print(f"Imagen entrada: {input_path}")
	print(f"Imagen salida : {output_path}")
	print(f"Mejor J       : {best_score:.6f}")
	print("Parametros optimos de CLAHE:")
	print(f"  clipLimit   : {best_clip:.4f}")
	print(f"  tileGridSize: ({best_grid_x}, {best_grid_y})")

	print("\nEntropia:")
	print(f"  Antes       : {h0:.4f}")
	print(f"  Despues     : {h1:.4f}")

	calcular_mse, calcular_psnr, calcular_ssim = load_optional_metrics_from_repo()
	if calcular_mse and calcular_psnr and calcular_ssim:
		original_list = to_matrix_list(original)
		enhanced_list = to_matrix_list(enhanced)
		alto, ancho = original.shape

		mse, rmse = calcular_mse(original_list, enhanced_list, ancho, alto)
		psnr = calcular_psnr(mse, 255)

		ssim_window = max(2, int(args.ssim_window))
		if ssim_window > min(alto, ancho):
			ssim_window = min(alto, ancho)
		ssim = calcular_ssim(original_list, enhanced_list, ssim_window, 255)

		print("\nMetricas del repositorio (métricas/):")
		print(f"  MSE         : {mse:.6f}")
		print(f"  RMSE        : {rmse:.6f}")
		if psnr == float("inf"):
			print("  PSNR        : Infinito")
		else:
			print(f"  PSNR        : {psnr:.4f} dB")
		print(f"  SSIM        : {ssim:.6f} (ventana={ssim_window})")
	else:
		print("\nNo se pudieron cargar MSE/PSNR/SSIM desde la carpeta métricas.")
		print("Se mantuvieron las metricas internas de entropia y la funcion objetivo.")


if __name__ == "__main__":
	main()

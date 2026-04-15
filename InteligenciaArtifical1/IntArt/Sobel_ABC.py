"""Procesa una imagen en tres etapas separadas:

imagen.png -> imagen_grises.png -> imagen_sobel.png -> imagen_sobel_ABC.png

Primero convierte la imagen a escala de grises y guarda ese archivo.
Despues toma el archivo _grises.png como entrada para aplicar Sobel y
generar el mapa de bordes.
Por ultimo usa ABC para buscar un umbral que refine el mapa de bordes Sobel.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


class ArtificialBeeColony:
	"""Implementacion didactica de ABC para maximizar una funcion objetivo."""

	def __init__(
		self,
		fitness_function,
		lower_bounds,
		upper_bounds,
		num_bees: int = 30,
		max_iter: int = 80,
		seed: int | None = None,
	):
		self.fitness_function = fitness_function
		self.lower_bounds = np.array(lower_bounds, dtype=np.float32)
		self.upper_bounds = np.array(upper_bounds, dtype=np.float32)
		self.num_bees = num_bees
		self.max_iter = max_iter
		self.num_params = len(lower_bounds)

		if seed is not None:
			np.random.seed(seed)

		self.population = np.random.uniform(
			self.lower_bounds,
			self.upper_bounds,
			size=(self.num_bees, self.num_params),
		)
		self.fitness = np.apply_along_axis(self.fitness_function, 1, self.population)
		self.best_bee = self.population[np.argmax(self.fitness)]
		self.best_fitness = float(np.max(self.fitness))

	def optimize(self):
		for iteration in range(self.max_iter):
			for i in range(self.num_bees):
				k = np.random.randint(0, self.num_params)
				phi = np.random.uniform(-1, 1)
				new_solution = np.copy(self.population[i])
				new_solution[k] = self.population[i, k] + phi * (
					self.population[i, k] - self.best_bee[k]
				)
				new_solution = np.clip(new_solution, self.lower_bounds, self.upper_bounds)
				new_fitness = float(self.fitness_function(new_solution))

				if new_fitness > self.fitness[i]:
					self.population[i] = new_solution
					self.fitness[i] = new_fitness

				if new_fitness > self.best_fitness:
					self.best_bee = new_solution
					self.best_fitness = new_fitness

			print(
				f"ABC iteracion {iteration + 1:03d} | "
				f"Mejor fitness: {self.best_fitness:.6f} | "
				f"Mejor umbral: {self.best_bee[0]:.2f}"
			)

		return self.best_bee, self.best_fitness


def construir_ruta_salida_grises(ruta_entrada: str | Path) -> Path:
	"""Genera la ruta de salida con el sufijo _grises."""
	ruta = Path(ruta_entrada)
	extension = ruta.suffix if ruta.suffix else ".png"
	return ruta.with_name(f"{ruta.stem}_grises{extension}")


def convertir_a_grises(ruta_entrada: str | Path, ruta_salida: str | Path) -> None:
	"""Carga una imagen y la guarda en escala de grises."""
	imagen = Image.open(ruta_entrada).convert("L")
	imagen.save(ruta_salida)


def construir_ruta_salida_sobel(ruta_entrada: str | Path) -> Path:
	"""Genera la ruta de salida con el sufijo _sobel."""
	ruta = Path(ruta_entrada)
	extension = ruta.suffix if ruta.suffix else ".png"
	return ruta.with_name(f"{ruta.stem}_sobel{extension}")


def construir_ruta_salida_sobel_abc(ruta_sobel: str | Path) -> Path:
	"""Genera la ruta de salida con el sufijo _ABC sobre la imagen Sobel."""
	ruta = Path(ruta_sobel)
	extension = ruta.suffix if ruta.suffix else ".png"
	return ruta.with_name(f"{ruta.stem}_ABC{extension}")


def cargar_grises_como_array(ruta_entrada: str | Path) -> np.ndarray:
	"""Carga una imagen en escala de grises y la devuelve como arreglo NumPy."""
	imagen = Image.open(ruta_entrada).convert("L")
	return np.array(imagen, dtype=np.float32)


def convolucion2d(imagen: np.ndarray, kernel: np.ndarray) -> np.ndarray:
	"""Aplica una convolucion 2D con relleno por replicacion en los bordes."""
	kernel_alto, kernel_ancho = kernel.shape
	pad_y = kernel_alto // 2
	pad_x = kernel_ancho // 2
	imagen_padded = np.pad(imagen, ((pad_y, pad_y), (pad_x, pad_x)), mode="edge")
	resultado = np.zeros_like(imagen, dtype=np.float32)

	for y in range(imagen.shape[0]):
		for x in range(imagen.shape[1]):
			ventana = imagen_padded[y : y + kernel_alto, x : x + kernel_ancho]
			resultado[y, x] = float(np.sum(ventana * kernel))

	return resultado


def aplicar_sobel(ruta_grises: str | Path, ruta_salida: str | Path) -> None:
	"""Aplica Sobel sobre la imagen en grises y guarda la magnitud del borde."""
	imagen_gris = cargar_grises_como_array(ruta_grises)

	kernel_x = np.array(
		[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
		dtype=np.float32,
	)
	kernel_y = np.array(
		[[1, 2, 1], [0, 0, 0], [-1, -2, -1]],
		dtype=np.float32,
	)

	grad_x = convolucion2d(imagen_gris, kernel_x)
	grad_y = convolucion2d(imagen_gris, kernel_y)
	magnitud = np.hypot(grad_x, grad_y)

	maximo = float(np.max(magnitud))
	if maximo > 0:
		magnitud = (magnitud / maximo) * 255.0

	Image.fromarray(magnitud.astype(np.uint8), mode="L").save(ruta_salida)


def evaluar_umbral_otsu(imagen: np.ndarray, umbral: float) -> float:
	"""Evalua un umbral con la varianza entre clases tipo Otsu."""
	valores = imagen.ravel().astype(np.float32)
	clase_fondo = valores[valores < umbral]
	clase_borde = valores[valores >= umbral]

	if clase_fondo.size == 0 or clase_borde.size == 0:
		return 0.0

	peso_fondo = clase_fondo.size / valores.size
	peso_borde = clase_borde.size / valores.size
	media_fondo = float(np.mean(clase_fondo))
	media_borde = float(np.mean(clase_borde))
	varianza_entre_clases = peso_fondo * peso_borde * (media_fondo - media_borde) ** 2
	return float(varianza_entre_clases)


def refinar_sobel_con_abc(ruta_sobel: str | Path, ruta_salida: str | Path) -> None:
	"""Refina la imagen Sobel buscando con ABC el mejor umbral de binarizacion."""
	imagen_sobel = np.array(Image.open(ruta_sobel).convert("L"), dtype=np.float32)

	def funcion_objetivo(solucion: np.ndarray) -> float:
		umbral = float(solucion[0])
		return evaluar_umbral_otsu(imagen_sobel, umbral)

	abc = ArtificialBeeColony(
		funcion_objetivo,
		lower_bounds=[0.0],
		upper_bounds=[255.0],
		num_bees=24,
		max_iter=40,
		seed=42,
	)
	mejor_solucion, mejor_fitness = abc.optimize()
	umbral_optimo = float(mejor_solucion[0])
	imagen_refinada = np.where(imagen_sobel >= umbral_optimo, 255, 0).astype(np.uint8)
	Image.fromarray(imagen_refinada, mode="L").save(ruta_salida)

	print("Refinamiento ABC completado")
	print(f"Umbral optimo: {umbral_optimo:.2f}")
	print(f"Fitness final: {mejor_fitness:.6f}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Convierte una imagen a escala de grises y luego aplica Sobel."
	)
	parser.add_argument(
		"entrada",
		help="Ruta de la imagen de entrada.",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	ruta_entrada = Path(args.entrada)

	if not ruta_entrada.exists():
		raise FileNotFoundError(f"No se encontro la imagen de entrada: {ruta_entrada}")

	ruta_salida = construir_ruta_salida_grises(ruta_entrada)
	convertir_a_grises(ruta_entrada, ruta_salida)

	ruta_sobel = construir_ruta_salida_sobel(ruta_entrada)
	aplicar_sobel(ruta_salida, ruta_sobel)

	ruta_sobel_abc = construir_ruta_salida_sobel_abc(ruta_sobel)
	refinar_sobel_con_abc(ruta_sobel, ruta_sobel_abc)

	print("Conversión a escala de grises completada")
	print(f"Entrada: {ruta_entrada}")
	print(f"Salida: {ruta_salida}")
	print("Aplicación de Sobel completada")
	print(f"Entrada Sobel: {ruta_salida}")
	print(f"Salida Sobel: {ruta_sobel}")
	print(f"Salida Sobel ABC: {ruta_sobel_abc}")


if __name__ == "__main__":
	main()

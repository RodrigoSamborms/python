"""Procesa una imagen en dos etapas separadas:

imagen.png -> imagen_grises.png -> imagen_sobel.png

Primero convierte la imagen a escala de grises y guarda ese archivo.
Despues toma el archivo _grises.png como entrada para aplicar Sobel y
generar el mapa de bordes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


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

	print("Conversión a escala de grises completada")
	print(f"Entrada: {ruta_entrada}")
	print(f"Salida: {ruta_salida}")
	print("Aplicación de Sobel completada")
	print(f"Entrada Sobel: {ruta_salida}")
	print(f"Salida Sobel: {ruta_sobel}")


if __name__ == "__main__":
	main()

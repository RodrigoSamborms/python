"""
Pipeline inicial de nitidez:
1. Suavizado gaussiano.
2. Afilado laplaciano sobre la imagen suavizada.

Este script carga una imagen, aplica ambos pasos y guarda el resultado final.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def apply_gaussian_smoothing(image: Image.Image, sigma: float) -> Image.Image:
	"""Aplica un suavizado gaussiano con radio (sigma) dado."""
	return image.filter(ImageFilter.GaussianBlur(radius=sigma))


def apply_laplacian_sharpening(image: Image.Image, alpha: float) -> Image.Image:
	"""
	Aplica afilado laplaciano: I_sharp = I + alpha * Laplaciano(I).

	Usa un Laplaciano de 4 vecinos para mantener el proceso estable y simple.
	"""
	image_array = np.asarray(image).astype(np.float32)

	if image_array.ndim == 2:
		padded = np.pad(image_array, ((1, 1), (1, 1)), mode="reflect")
		center = padded[1:-1, 1:-1]
		up = padded[:-2, 1:-1]
		down = padded[2:, 1:-1]
		left = padded[1:-1, :-2]
		right = padded[1:-1, 2:]
		laplacian = 4.0 * center - up - down - left - right
	else:
		padded = np.pad(image_array, ((1, 1), (1, 1), (0, 0)), mode="reflect")
		center = padded[1:-1, 1:-1, :]
		up = padded[:-2, 1:-1, :]
		down = padded[2:, 1:-1, :]
		left = padded[1:-1, :-2, :]
		right = padded[1:-1, 2:, :]
		laplacian = 4.0 * center - up - down - left - right

	sharpened = image_array + alpha * laplacian
	sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
	return Image.fromarray(sharpened)


def build_default_output_path(input_path: Path) -> Path:
	"""Construye una ruta de salida en el mismo directorio con sufijo _gauss_lap."""
	return input_path.with_name(f"{input_path.stem}_gauss_lap{input_path.suffix}")


def build_default_gaussian_output_path(input_path: Path) -> Path:
	"""Construye una ruta para la salida intermedia con sufijo _gauss."""
	return input_path.with_name(f"{input_path.stem}_gauss{input_path.suffix}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Aplica suavizado gaussiano y luego afilado laplaciano."
	)
	parser.add_argument(
		"--input",
		required=True,
		help="Ruta de la imagen de entrada.",
	)
	parser.add_argument(
		"--output",
		default=None,
		help="Ruta de la imagen de salida (opcional).",
	)
	parser.add_argument(
		"--gaussian-output",
		default=None,
		help="Ruta para guardar la imagen intermedia gaussiana (opcional).",
	)
	parser.add_argument(
		"--sigma",
		type=float,
		default=1.5,
		help="Sigma/radio del filtro gaussiano (por defecto 1.5).",
	)
	parser.add_argument(
		"--alpha",
		type=float,
		default=1.0,
		help="Intensidad del afilado laplaciano (por defecto 1.0).",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	if args.sigma < 0:
		raise ValueError("El valor de --sigma debe ser >= 0.")
	if args.alpha < 0:
		raise ValueError("El valor de --alpha debe ser >= 0.")

	input_path = Path(args.input)
	if not input_path.exists():
		raise FileNotFoundError(f"No se encontro la imagen: {input_path}")

	output_path = Path(args.output) if args.output else build_default_output_path(input_path)
	gaussian_output_path = (
		Path(args.gaussian_output)
		if args.gaussian_output
		else build_default_gaussian_output_path(input_path)
	)

	image = Image.open(input_path)
	smoothed = apply_gaussian_smoothing(image, args.sigma)
	smoothed.save(gaussian_output_path)
	sharpened = apply_laplacian_sharpening(smoothed, args.alpha)
	sharpened.save(output_path)

	print("Pipeline aplicado correctamente: suavizado gaussiano + afilado laplaciano.")
	print(f"Entrada: {input_path}")
	print(f"Salida intermedia (gaussiana): {gaussian_output_path}")
	print(f"Salida: {output_path}")
	print(f"Sigma: {args.sigma}")
	print(f"Alpha: {args.alpha}")


if __name__ == "__main__":
	main()

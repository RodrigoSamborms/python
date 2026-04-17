"""
Primera etapa de nitidez: suavizado gaussiano.

Este script carga una imagen, aplica un filtro Gaussiano y guarda el resultado.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter


def apply_gaussian_smoothing(image: Image.Image, sigma: float) -> Image.Image:
	"""Aplica un suavizado gaussiano con radio (sigma) dado."""
	return image.filter(ImageFilter.GaussianBlur(radius=sigma))


def build_default_output_path(input_path: Path) -> Path:
	"""Construye una ruta de salida en el mismo directorio con sufijo _gauss."""
	return input_path.with_name(f"{input_path.stem}_gauss{input_path.suffix}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Carga una imagen y aplica suavizado gaussiano."
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
		"--sigma",
		type=float,
		default=1.5,
		help="Sigma/radio del filtro gaussiano (por defecto 1.5).",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	if args.sigma < 0:
		raise ValueError("El valor de --sigma debe ser >= 0.")

	input_path = Path(args.input)
	if not input_path.exists():
		raise FileNotFoundError(f"No se encontro la imagen: {input_path}")

	output_path = Path(args.output) if args.output else build_default_output_path(input_path)

	image = Image.open(input_path)
	smoothed = apply_gaussian_smoothing(image, args.sigma)
	smoothed.save(output_path)

	print("Suavizado gaussiano aplicado correctamente.")
	print(f"Entrada: {input_path}")
	print(f"Salida: {output_path}")
	print(f"Sigma: {args.sigma}")


if __name__ == "__main__":
	main()

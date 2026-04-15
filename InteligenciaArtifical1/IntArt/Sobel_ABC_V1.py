"""Convierte una imagen de entrada a escala de grises.

Uso:
	python Sobel_ABC.py ruta\a\imagen.png

Salida:
	ruta\a\imagen_grises.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

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


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Convierte una imagen a escala de grises."
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

	print("Conversión a escala de grises completada")
	print(f"Entrada: {ruta_entrada}")
	print(f"Salida: {ruta_salida}")


if __name__ == "__main__":
	main()

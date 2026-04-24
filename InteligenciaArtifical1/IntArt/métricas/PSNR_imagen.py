import argparse
import os

from MSE import calcular_mse
from PSNR import calcular_psnr


def _saltar_espacios_y_comentarios(data, idx):
	longitud = len(data)
	while idx < longitud:
		byte = data[idx]

		# Ignora espacios en blanco
		if byte in b" \t\r\n":
			idx += 1
			continue

		# Ignora comentarios que inician con '#'
		if byte == ord("#"):
			idx += 1
			while idx < longitud and data[idx] not in b"\r\n":
				idx += 1
			continue

		break

	return idx


def _leer_token(data, idx):
	idx = _saltar_espacios_y_comentarios(data, idx)
	longitud = len(data)

	if idx >= longitud:
		return None, idx

	inicio = idx
	while idx < longitud and data[idx] not in b" \t\r\n":
		idx += 1

	token = data[inicio:idx].decode("ascii")
	return token, idx


def cargar_pgm(ruta):
	with open(ruta, "rb") as archivo:
		data = archivo.read()

	idx = 0

	magic, idx = _leer_token(data, idx)
	if magic not in ("P2", "P5"):
		raise ValueError(
			"Formato no soportado. Use imagenes PGM tipo P2 (texto) o P5 (binario)."
		)

	ancho_txt, idx = _leer_token(data, idx)
	alto_txt, idx = _leer_token(data, idx)
	maxval_txt, idx = _leer_token(data, idx)

	if ancho_txt is None or alto_txt is None or maxval_txt is None:
		raise ValueError("Cabecera PGM incompleta")

	ancho = int(ancho_txt)
	alto = int(alto_txt)
	maxval = int(maxval_txt)

	if ancho <= 0 or alto <= 0:
		raise ValueError("Dimensiones invalidas en la imagen")

	if maxval <= 0 or maxval > 65535:
		raise ValueError("Valor maximo de pixel invalido en PGM")

	total_pixeles = ancho * alto

	if magic == "P2":
		pixeles = []
		for _ in range(total_pixeles):
			token, idx = _leer_token(data, idx)
			if token is None:
				raise ValueError("Cantidad de pixeles insuficiente en P2")
			pixeles.append(int(token))
	else:
		idx = _saltar_espacios_y_comentarios(data, idx)

		if maxval < 256:
			necesarios = total_pixeles
			bloque = data[idx:idx + necesarios]
			if len(bloque) != necesarios:
				raise ValueError("Cantidad de pixeles insuficiente en P5")
			pixeles = list(bloque)
		else:
			necesarios = total_pixeles * 2
			bloque = data[idx:idx + necesarios]
			if len(bloque) != necesarios:
				raise ValueError("Cantidad de pixeles insuficiente en P5")

			pixeles = []
			for i in range(0, len(bloque), 2):
				valor = (bloque[i] << 8) + bloque[i + 1]
				pixeles.append(valor)

	matriz = []
	posicion = 0
	for _ in range(alto):
		fila = pixeles[posicion:posicion + ancho]
		matriz.append(fila)
		posicion += ancho

	return matriz, ancho, alto, maxval


def solicitar_ruta(mensaje):
	ruta = input(mensaje).strip().strip('"')
	return ruta


def main():
	parser = argparse.ArgumentParser(
		description="Calcula PSNR (Peak Signal-to-Noise Ratio) entre dos imagenes PGM sin librerias externas."
	)
	parser.add_argument(
		"--original",
		help="Ruta de la imagen original (PGM P2/P5)",
	)
	parser.add_argument(
		"--procesada",
		help="Ruta de la imagen procesada (PGM P2/P5)",
	)

	args = parser.parse_args()

	ruta_original = args.original or solicitar_ruta("Ruta de imagen original (PGM): ")
	ruta_procesada = args.procesada or solicitar_ruta("Ruta de imagen procesada (PGM): ")

	if not os.path.exists(ruta_original):
		raise FileNotFoundError(f"No existe la ruta original: {ruta_original}")
	if not os.path.exists(ruta_procesada):
		raise FileNotFoundError(f"No existe la ruta procesada: {ruta_procesada}")

	imagen_original, ancho_o, alto_o, maxval_o = cargar_pgm(ruta_original)
	imagen_procesada, ancho_p, alto_p, maxval_p = cargar_pgm(ruta_procesada)

	if ancho_o != ancho_p or alto_o != alto_p:
		raise ValueError(
			"Las imagenes no tienen la misma dimension: "
			f"original={ancho_o}x{alto_o}, procesada={ancho_p}x{alto_p}"
		)

	if maxval_o != maxval_p:
		raise ValueError(
			"Las imagenes no tienen el mismo valor maximo de pixel: "
			f"original={maxval_o}, procesada={maxval_p}"
		)

	# Calcular MSE (necesario para PSNR)
	mse, rmse = calcular_mse(imagen_original, imagen_procesada, ancho_o, alto_o)

	# Calcular PSNR
	psnr = calcular_psnr(mse, maxval_o)

	# Mostrar resultados
	print(f"\n=== Resultados de comparación de imágenes ===")
	print(f"Dimension: {ancho_o}x{alto_o}")
	print(f"Valor máximo de pixel: {maxval_o}")
	print(f"\nMétricas de calidad:")
	print(f"  MSE (Error Cuadrático Medio): {mse:.6f}")
	print(f"  RMSE (Raíz del ECM): {rmse:.6f}")

	if psnr == float('inf'):
		print(f"  PSNR (Peak Signal-to-Noise Ratio): Infinito (imágenes idénticas)")
	else:
		print(f"  PSNR (Peak Signal-to-Noise Ratio): {psnr:.2f} dB")

		# Interpretación de la calidad
		if psnr > 50:
			interpretacion = "Excelente"
		elif psnr > 40:
			interpretacion = "Muy buena"
		elif psnr > 30:
			interpretacion = "Buena"
		elif psnr > 20:
			interpretacion = "Aceptable"
		else:
			interpretacion = "Pobre"

		print(f"  Interpretación: {interpretacion}")


if __name__ == "__main__":
	main()

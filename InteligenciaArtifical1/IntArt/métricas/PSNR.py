from math import log10


def calcular_psnr(mse, valor_maximo_pixel=255):
	"""Calcula PSNR (Peak Signal-to-Noise Ratio) entre dos imágenes.

	Peak Signal-to-Noise Ratio es una métrica que mide la calidad de una imagen
	comparándola con una imagen original. Un PSNR más alto indica mejor calidad.

	Parametros:
		mse: Error Cuadrático Medio (Mean Squared Error) entre dos imágenes.
		valor_maximo_pixel: Valor máximo que puede tener un píxel (ej. 255 para 8-bit).
			Por defecto es 255.

	Retorna:
		float: Valor de PSNR en decibelios (dB). Si MSE es 0, retorna infinito
			(las imágenes son idénticas).

	Lanza:
		ValueError: Si MSE es negativo o valor_maximo_pixel es <= 0.
	"""
	if mse < 0:
		raise ValueError("MSE no puede ser negativo")

	if valor_maximo_pixel <= 0:
		raise ValueError("Valor máximo de pixel debe ser mayor que cero")

	# Si MSE es 0, las imágenes son idénticas
	if mse == 0:
		return float('inf')

	# Numerador = Valor_Maximo_Pixel^2
	numerador = valor_maximo_pixel ** 2

	# Relacion = Numerador / MSE
	relacion = numerador / mse

	# PSNR = 10 * Logaritmo10(Relacion)
	psnr = 10 * log10(relacion)

	return psnr


if __name__ == "__main__":
	# Ejemplo de uso
	print("=== Ejemplos de cálculo de PSNR ===\n")

	# Ejemplo 1: Imágenes idénticas (MSE = 0)
	mse_ejemplo1 = 0
	psnr_ejemplo1 = calcular_psnr(mse_ejemplo1)
	print(f"Ejemplo 1 - Imágenes idénticas:")
	print(f"  MSE: {mse_ejemplo1}")
	print(f"  PSNR: {psnr_ejemplo1} dB\n")

	# Ejemplo 2: MSE pequeño (buena calidad)
	mse_ejemplo2 = 10
	psnr_ejemplo2 = calcular_psnr(mse_ejemplo2)
	print(f"Ejemplo 2 - Buena calidad:")
	print(f"  MSE: {mse_ejemplo2}")
	print(f"  PSNR: {psnr_ejemplo2:.2f} dB\n")

	# Ejemplo 3: MSE moderado (calidad media)
	mse_ejemplo3 = 100
	psnr_ejemplo3 = calcular_psnr(mse_ejemplo3)
	print(f"Ejemplo 3 - Calidad media:")
	print(f"  MSE: {mse_ejemplo3}")
	print(f"  PSNR: {psnr_ejemplo3:.2f} dB\n")

	# Ejemplo 4: MSE grande (baja calidad)
	mse_ejemplo4 = 1000
	psnr_ejemplo4 = calcular_psnr(mse_ejemplo4)
	print(f"Ejemplo 4 - Baja calidad:")
	print(f"  MSE: {mse_ejemplo4}")
	print(f"  PSNR: {psnr_ejemplo4:.2f} dB\n")

	# Ejemplo 5: Con valor máximo de píxel diferente (16-bit)
	mse_ejemplo5 = 100
	valor_max_16bit = 65535
	psnr_ejemplo5 = calcular_psnr(mse_ejemplo5, valor_max_16bit)
	print(f"Ejemplo 5 - Imagen 16-bit:")
	print(f"  MSE: {mse_ejemplo5}")
	print(f"  Valor máximo de píxel: {valor_max_16bit}")
	print(f"  PSNR: {psnr_ejemplo5:.2f} dB")

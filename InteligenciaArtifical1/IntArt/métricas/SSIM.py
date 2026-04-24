def calcular_media(bloque):
	"""Calcula la media de los píxeles en un bloque."""
	if not bloque or not bloque[0]:
		return 0
	
	total = sum(sum(fila) for fila in bloque)
	cantidad = len(bloque) * len(bloque[0])
	return total / cantidad


def calcular_varianza(bloque, media=None):
	"""Calcula la varianza de los píxeles en un bloque."""
	if not bloque or not bloque[0]:
		return 0
	
	if media is None:
		media = calcular_media(bloque)
	
	suma_cuadrados = sum(sum((pixel - media) ** 2 for pixel in fila) for fila in bloque)
	cantidad = len(bloque) * len(bloque[0])
	return suma_cuadrados / cantidad


def calcular_covarianza(bloque_x, bloque_y, media_x=None, media_y=None):
	"""Calcula la covarianza entre dos bloques."""
	if not bloque_x or not bloque_x[0]:
		return 0
	
	if media_x is None:
		media_x = calcular_media(bloque_x)
	if media_y is None:
		media_y = calcular_media(bloque_y)
	
	suma_productos = sum(
		sum((bloque_x[i][j] - media_x) * (bloque_y[i][j] - media_y)
			for j in range(len(bloque_x[0])))
		for i in range(len(bloque_x))
	)
	cantidad = len(bloque_x) * len(bloque_x[0])
	return suma_productos / cantidad


def extraer_bloque(imagen, fila_inicio, columna_inicio, tamaño_ventana):
	"""Extrae un bloque de la imagen."""
	bloque = []
	for i in range(fila_inicio, min(fila_inicio + tamaño_ventana, len(imagen))):
		fila = []
		for j in range(columna_inicio, min(columna_inicio + tamaño_ventana, len(imagen[0]))):
			fila.append(imagen[i][j])
		bloque.append(fila)
	return bloque


def calcular_ssim_local(ventana_x, ventana_y, c1, c2):
	"""Calcula el SSIM local entre dos ventanas."""
	media_x = calcular_media(ventana_x)
	media_y = calcular_media(ventana_y)
	varianza_x = calcular_varianza(ventana_x, media_x)
	varianza_y = calcular_varianza(ventana_y, media_y)
	covarianza_xy = calcular_covarianza(ventana_x, ventana_y, media_x, media_y)
	
	# Numerador = (2 * Media_x * Media_y + C1) * (2 * Covarianza_xy + C2)
	numerador = (2 * media_x * media_y + c1) * (2 * covarianza_xy + c2)
	
	# Denominador = (Media_x^2 + Media_y^2 + C1) * (Varianza_x + Varianza_y + C2)
	denominador = (media_x ** 2 + media_y ** 2 + c1) * (varianza_x + varianza_y + c2)
	
	# Evitar división por cero
	if denominador == 0:
		return 1.0 if numerador == 0 else 0.0
	
	ssim_local = numerador / denominador
	return ssim_local


def calcular_ssim_global(imagen_x, imagen_y, tamaño_ventana=8, valor_maximo_pixel=255):
	"""Calcula SSIM (Structural Similarity Index) global entre dos imágenes.

	SSIM es una métrica perceptual de calidad de imagen que mide la similitud
	estructural entre dos imágenes. A diferencia de MSE y PSNR, SSIM tiene en
	cuenta las características visuales humanas.

	Parametros:
		imagen_x: Primera imagen como matriz (lista de listas).
		imagen_y: Segunda imagen como matriz (lista de listas).
		tamaño_ventana: Tamaño de la ventana deslizante (por defecto 8x8).
		valor_maximo_pixel: Valor máximo que puede tener un píxel (ej. 255).

	Retorna:
		float: Valor SSIM entre -1 y 1 (típicamente 0 a 1).
			1 = imágenes idénticas
			0 = imágenes sin correlación
			Valores negativos = correlación negativa

	Lanza:
		ValueError: Si las imágenes tienen dimensiones diferentes o están vacías.
	"""
	# Validaciones
	if not imagen_x or not imagen_y:
		raise ValueError("Las imágenes no pueden estar vacías")
	
	alto_x = len(imagen_x)
	ancho_x = len(imagen_x[0]) if imagen_x else 0
	alto_y = len(imagen_y)
	ancho_y = len(imagen_y[0]) if imagen_y else 0
	
	if alto_x != alto_y or ancho_x != ancho_y:
		raise ValueError(
			f"Las imágenes deben tener las mismas dimensiones: "
			f"imagen_x={ancho_x}x{alto_x}, imagen_y={ancho_y}x{alto_y}"
		)
	
	if ancho_x < tamaño_ventana or alto_x < tamaño_ventana:
		raise ValueError(
			f"El tamaño de la imagen ({ancho_x}x{alto_x}) debe ser al menos "
			f"{tamaño_ventana}x{tamaño_ventana}"
		)
	
	# Constantes de estabilización numérica
	# C1 = (0.01 * L)^2
	# C2 = (0.03 * L)^2
	# donde L es el rango dinámico de los píxeles
	l = valor_maximo_pixel
	c1 = (0.01 * l) ** 2
	c2 = (0.03 * l) ** 2
	
	lista_ssim_locales = []
	
	# Dividir la imagen en bloques (ventanas)
	for fila_inicio in range(0, alto_x - tamaño_ventana + 1, tamaño_ventana):
		for columna_inicio in range(0, ancho_x - tamaño_ventana + 1, tamaño_ventana):
			# Extraer ventanas
			ventana_x = extraer_bloque(imagen_x, fila_inicio, columna_inicio, tamaño_ventana)
			ventana_y = extraer_bloque(imagen_y, fila_inicio, columna_inicio, tamaño_ventana)
			
			# Calcular SSIM local
			ssim_local = calcular_ssim_local(ventana_x, ventana_y, c1, c2)
			lista_ssim_locales.append(ssim_local)
	
	# El SSIM final es el promedio de todos los bloques
	if not lista_ssim_locales:
		return 0.0
	
	ssim_final = sum(lista_ssim_locales) / len(lista_ssim_locales)
	return ssim_final


if __name__ == "__main__":
	# Ejemplo de uso
	print("=== Ejemplos de cálculo de SSIM ===\n")

	# Ejemplo 1: Imágenes idénticas
	imagen_identica = [
		[10, 20, 30, 40],
		[50, 60, 70, 80],
		[90, 100, 110, 120],
		[130, 140, 150, 160],
	]
	ssim_ejemplo1 = calcular_ssim_global(imagen_identica, imagen_identica, tamaño_ventana=2)
	print(f"Ejemplo 1 - Imágenes idénticas:")
	print(f"  SSIM: {ssim_ejemplo1:.4f}\n")

	# Ejemplo 2: Imágenes ligeramente diferentes
	imagen_original = [
		[10, 20, 30, 40],
		[50, 60, 70, 80],
		[90, 100, 110, 120],
		[130, 140, 150, 160],
	]
	imagen_modificada = [
		[11, 21, 31, 41],
		[51, 61, 71, 81],
		[91, 101, 111, 121],
		[131, 141, 151, 161],
	]
	ssim_ejemplo2 = calcular_ssim_global(imagen_original, imagen_modificada, tamaño_ventana=2)
	print(f"Ejemplo 2 - Imágenes ligeramente diferentes (+1 píxel):")
	print(f"  SSIM: {ssim_ejemplo2:.4f}\n")

	# Ejemplo 3: Imágenes bastante diferentes
	imagen_diferente = [
		[100, 110, 120, 130],
		[140, 150, 160, 170],
		[180, 190, 200, 210],
		[220, 230, 240, 250],
	]
	ssim_ejemplo3 = calcular_ssim_global(imagen_original, imagen_diferente, tamaño_ventana=2)
	print(f"Ejemplo 3 - Imágenes bastante diferentes:")
	print(f"  SSIM: {ssim_ejemplo3:.4f}\n")

	# Información sobre SSIM
	print("Escala de SSIM:")
	print("  1.0    = Imágenes idénticas")
	print("  0.8-1.0 = Muy buena similitud")
	print("  0.6-0.8 = Buena similitud")
	print("  0.4-0.6 = Similitud moderada")
	print("  0.0-0.4 = Baja similitud")
	print("  < 0.0  = Correlación negativa")

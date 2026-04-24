from math import sqrt


def calcular_mse(imagen_original, imagen_procesada, ancho, alto):
	"""Calcula MSE y RMSE entre dos imagenes 2D.

	Parametros:
		imagen_original: matriz (lista de listas) de la imagen original.
		imagen_procesada: matriz (lista de listas) de la imagen procesada.
		ancho: numero de columnas a comparar.
		alto: numero de filas a comparar.

	Retorna:
		(mse, rmse)
	"""
	if ancho <= 0 or alto <= 0:
		raise ValueError("ancho y alto deben ser mayores que cero")

	if len(imagen_original) < alto or len(imagen_procesada) < alto:
		raise ValueError("alto mayor al numero de filas disponibles")

	suma_cuadrados = 0.0

	for i in range(alto):
		if len(imagen_original[i]) < ancho or len(imagen_procesada[i]) < ancho:
			raise ValueError("ancho mayor al numero de columnas disponibles")

		for j in range(ancho):
			diferencia = imagen_original[i][j] - imagen_procesada[i][j]
			suma_cuadrados += diferencia * diferencia

	mse = suma_cuadrados / (ancho * alto)
	rmse = sqrt(mse)

	return mse, rmse


if __name__ == "__main__":
	# Ejemplo sencillo de uso
	original = [
		[10, 20, 30],
		[40, 50, 60],
	]
	procesada = [
		[12, 18, 33],
		[39, 49, 62],
	]

	mse_valor, rmse_valor = calcular_mse(original, procesada, ancho=3, alto=2)
	print("MSE:", mse_valor)
	print("RMSE:", rmse_valor)

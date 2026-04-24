import argparse
import os
import sys
from struct import pack

# Intentar importar PIL si está disponible
try:
	from PIL import Image
	PIL_DISPONIBLE = True
except ImportError:
	PIL_DISPONIBLE = False


def guardar_pgm_p5(imagen_array, ancho, alto, valor_maximo, ruta_salida):
	"""Guarda una matriz 2D como imagen PGM en formato binario (P5)."""
	try:
		with open(ruta_salida, 'wb') as archivo:
			# Escribir cabecera
			archivo.write(f"P5\n".encode('ascii'))
			archivo.write(f"# Convertido con PGM_conversion.py\n".encode('ascii'))
			archivo.write(f"{ancho} {alto}\n".encode('ascii'))
			archivo.write(f"{valor_maximo}\n".encode('ascii'))
			
			# Escribir datos
			for fila in imagen_array:
				for pixel in fila:
					if valor_maximo < 256:
						archivo.write(pack('B', pixel))
					else:
						archivo.write(pack('>H', pixel))
		
		return True
	except Exception as e:
		print(f"Error al guardar: {e}")
		return False


def guardar_pgm_p2(imagen_array, ancho, alto, valor_maximo, ruta_salida):
	"""Guarda una matriz 2D como imagen PGM en formato texto (P2)."""
	try:
		with open(ruta_salida, 'w') as archivo:
			# Escribir cabecera
			archivo.write(f"P2\n")
			archivo.write(f"# Convertido con PGM_conversion.py\n")
			archivo.write(f"{ancho} {alto}\n")
			archivo.write(f"{valor_maximo}\n")
			
			# Escribir datos
			for i, fila in enumerate(imagen_array):
				for j, pixel in enumerate(fila):
					archivo.write(f"{pixel}")
					if j < len(fila) - 1:
						archivo.write(" ")
				archivo.write("\n")
		
		return True
	except Exception as e:
		print(f"Error al guardar: {e}")
		return False


def convertir_con_pil(ruta_entrada, ruta_salida, formato_salida='P5'):
	"""Convierte una imagen usando PIL/Pillow."""
	try:
		# Abrir imagen
		imagen = Image.open(ruta_entrada)
		
		# Convertir a escala de grises
		imagen_gris = imagen.convert('L')
		
		# Obtener dimensiones
		ancho, alto = imagen_gris.size
		
		# Obtener datos de píxeles
		datos = list(imagen_gris.getdata())
		matriz = []
		for i in range(alto):
			fila = datos[i * ancho:(i + 1) * ancho]
			matriz.append(list(fila))
		
		# Guardar como PGM
		if formato_salida.upper() == 'P5':
			exito = guardar_pgm_p5(matriz, ancho, alto, 255, ruta_salida)
		else:
			exito = guardar_pgm_p2(matriz, ancho, alto, 255, ruta_salida)
		
		if exito:
			print(f"✓ Imagen convertida exitosamente")
			print(f"  Dimensiones: {ancho}x{alto}")
			print(f"  Formato de salida: {formato_salida}")
			print(f"  Archivo: {ruta_salida}")
		
		return exito
	except Exception as e:
		print(f"Error en la conversión: {e}")
		return False


def crear_imagen_prueba(ruta_salida, ancho=256, alto=256, patron='gradiente'):
	"""Crea una imagen de prueba en formato PGM."""
	try:
		matriz = []
		
		if patron == 'gradiente':
			# Gradiente horizontal
			for i in range(alto):
				fila = []
				for j in range(ancho):
					valor = int((j / ancho) * 255)
					fila.append(valor)
				matriz.append(fila)
		
		elif patron == 'cuadros':
			# Patrón de cuadros
			tamaño_cuadro = 32
			for i in range(alto):
				fila = []
				for j in range(ancho):
					cuadro_i = (i // tamaño_cuadro) % 2
					cuadro_j = (j // tamaño_cuadro) % 2
					valor = 255 if (cuadro_i + cuadro_j) % 2 == 0 else 0
					fila.append(valor)
				matriz.append(fila)
		
		elif patron == 'circulo':
			# Círculo en el centro
			centro_x, centro_y = ancho // 2, alto // 2
			radio = min(ancho, alto) // 3
			for i in range(alto):
				fila = []
				for j in range(ancho):
					distancia = ((j - centro_x) ** 2 + (i - centro_y) ** 2) ** 0.5
					valor = 255 if distancia <= radio else 0
					fila.append(valor)
				matriz.append(fila)
		
		# Guardar imagen
		exito = guardar_pgm_p5(matriz, ancho, alto, 255, ruta_salida)
		
		if exito:
			print(f"✓ Imagen de prueba creada: {patron}")
			print(f"  Dimensiones: {ancho}x{alto}")
			print(f"  Archivo: {ruta_salida}")
		
		return exito
	except Exception as e:
		print(f"Error al crear imagen de prueba: {e}")
		return False


def obtener_informacion_archivo(ruta_archivo):
	"""Obtiene información sobre un archivo de imagen."""
	if not os.path.exists(ruta_archivo):
		print(f"Error: El archivo no existe: {ruta_archivo}")
		return False
	
	nombre = os.path.basename(ruta_archivo)
	extension = os.path.splitext(nombre)[1].lower()
	tamaño_bytes = os.path.getsize(ruta_archivo)
	
	print(f"\n=== Información del archivo ===")
	print(f"Nombre: {nombre}")
	print(f"Extensión: {extension}")
	print(f"Tamaño: {tamaño_bytes} bytes ({tamaño_bytes / 1024 / 1024:.2f} MB)")
	
	if PIL_DISPONIBLE:
		try:
			imagen = Image.open(ruta_archivo)
			print(f"Dimensiones: {imagen.width}x{imagen.height}")
			print(f"Modo de color: {imagen.mode}")
		except:
			print("No se pudo leer información de la imagen")
	
	return True


def main():
	parser = argparse.ArgumentParser(
		description="Convierte imágenes a formato PGM (Portable Graymap) sin librerías externas.",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Ejemplos de uso:

  # Convertir una imagen con PIL (recomendado)
  python PGM_conversion.py -i imagen.jpg -o imagen.pgm

  # Crear una imagen de prueba (gradiente)
  python PGM_conversion.py --crear gradiente -o test_gradiente.pgm

  # Crear una imagen de prueba (cuadros)
  python PGM_conversion.py --crear cuadros -o test_cuadros.pgm

  # Crear una imagen de prueba (círculo)
  python PGM_conversion.py --crear circulo -o test_circulo.pgm

  # Obtener información de una imagen
  python PGM_conversion.py -i imagen.jpg --info

  # Especificar formato de salida PGM
  python PGM_conversion.py -i imagen.jpg -o imagen.pgm --formato P2
		"""
	)

	parser.add_argument(
		"-i", "--entrada",
		help="Ruta del archivo de imagen de entrada",
	)
	parser.add_argument(
		"-o", "--salida",
		help="Ruta del archivo PGM de salida",
	)
	parser.add_argument(
		"--crear",
		choices=['gradiente', 'cuadros', 'circulo'],
		help="Crear una imagen de prueba en lugar de convertir",
	)
	parser.add_argument(
		"--ancho",
		type=int,
		default=256,
		help="Ancho de la imagen de prueba (por defecto 256)",
	)
	parser.add_argument(
		"--alto",
		type=int,
		default=256,
		help="Alto de la imagen de prueba (por defecto 256)",
	)
	parser.add_argument(
		"--formato",
		choices=['P2', 'P5'],
		default='P5',
		help="Formato PGM de salida: P2 (texto) o P5 (binario, por defecto)",
	)
	parser.add_argument(
		"--info",
		action='store_true',
		help="Mostrar información sobre la imagen de entrada",
	)

	args = parser.parse_args()

	# Mostrar estado de PIL
	print(f"Estado de PIL: {'Disponible ✓' if PIL_DISPONIBLE else 'NO disponible ✗'}\n")

	# Crear imagen de prueba
	if args.crear:
		if not args.salida:
			print("Error: Se requiere -o/--salida para crear imagen")
			return
		
		crear_imagen_prueba(args.salida, args.ancho, args.alto, args.crear)
		return

	# Obtener información de la imagen
	if args.info:
		if not args.entrada:
			print("Error: Se requiere -i/--entrada para obtener información")
			return
		
		obtener_informacion_archivo(args.entrada)
		return

	# Convertir imagen
	if args.entrada and args.salida:
		if not os.path.exists(args.entrada):
			print(f"Error: El archivo de entrada no existe: {args.entrada}")
			return

		if not PIL_DISPONIBLE:
			print("Error: PIL/Pillow no está instalado")
			print("\nPara instalar PIL/Pillow:")
			print("  pip install Pillow")
			print("\nAlternativa: Usa --crear para generar imágenes de prueba")
			return

		convertir_con_pil(args.entrada, args.salida, args.formato)
		return

	# Si no hay argumentos válidos
	print("Error: Especifica operación válida")
	print("\nOpciones:")
	print("  1. Convertir imagen: -i entrada.jpg -o salida.pgm")
	print("  2. Crear prueba: --crear gradiente -o salida.pgm")
	print("  3. Ver información: -i imagen.jpg --info")
	print("\nUsa -h para más ayuda")


if __name__ == "__main__":
	main()

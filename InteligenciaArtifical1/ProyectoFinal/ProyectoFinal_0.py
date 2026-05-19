import re

class ValidadorExpresion:
    def __init__(self):
        self.matrices_dimensiones = {}

    def solicitar_datos(self):
        print("--- CAPA 1: INGRESO DE DATOS Y VALIDACIÓN ---")
        # 1. Recibir la expresión
        expresion = input("Ingresa la expresión matricial (ej. A * B + C * D): ")
        # Limpiar espacios en blanco extras
        expresion = "".join(expresion.split())
        
        # 2. Extraer los nombres de las matrices usando Expresiones Regulares (letras mayúsculas)
        nombres_matrices = sorted(list(set(re.findall(r'[A-Z]', expresion))))
        
        if not nombres_matrices:
            print("Error: No se detectaron nombres de matrices válidos (usa letras mayúsculas).")
            return None, None

        print("\nAhora, ingresa las dimensiones de cada matriz:")
        # 3. Solicitar las dimensiones de cada una
        for matriz in nombres_matrices:
            while True:
                try:
                    filas = int(input(f"  Filas de {matriz}: "))
                    columnas = int(input(f"  Columnas de {matriz}: "))
                    if filas <= 0 or columnas <= 0:
                        print("  [Error] Las dimensiones deben ser mayores a 0.")
                        continue
                    # Guardamos como una tupla (filas, columnas)
                    self.matrices_dimensiones[matriz] = (filas, columnas)
                    break
                except ValueError:
                    print("  [Error] Por favor, ingresa números enteros válidos.")
        
        return expresion, self.matrices_dimensiones

# --- PRUEBA DE LA IMPLEMENTACIÓN ---
if __name__ == "__main__":
    validador = ValidadorExpresion()
    expresion, dimensiones = validador.solicitar_datos()
    
    if expresion:
        print("\n--- DATOS CAPTURADOS CON ÉXITO ---")
        print(f"Expresión a procesar: {expresion}")
        print(f"Diccionario de dimensiones: {dimensiones}")
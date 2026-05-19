import re

class ValidadorExpresion:
    def __init__(self):
        self.matrices_dimensiones = {}

    def solicitar_datos(self):
        print("--- CAPA 1: INGRESO DE DATOS Y VALIDACIÓN ---")
        expresion = input("Ingresa la expresión matricial (ej. A * B + C * D): ")
        expresion = "".join(expresion.split())
        
        nombres_matrices = sorted(list(set(re.findall(r'[A-Z]', expresion))))
        
        if not nombres_matrices:
            print("Error: No se detectaron nombres de matrices válidos.")
            return None, None

        print("\nAhora, ingresa las dimensiones de cada matriz:")
        for matriz in nombres_matrices:
            while True:
                try:
                    filas = int(input(f"  Filas de {matriz}: "))
                    columnas = int(input(f"  Columnas de {matriz}: "))
                    if filas <= 0 or columnas <= 0:
                        print("  [Error] Las dimensiones deben ser mayores a 0.")
                        continue
                    self.matrices_dimensiones[matriz] = (filas, columnas)
                    break
                except ValueError:
                    print("  [Error] Por favor, ingresa números enteros.")
        
        return expresion, self.matrices_dimensiones

    def _convertir_a_postfix(self, expresion):
        """Convierte la expresión a notación postfija para respetar la jerarquía (* antes que +)"""
        precedencia = {'+': 1, '*': 2}
        salida = []
        pila_operadores = []
        
        # Tokenizar la expresión (separar letras y operadores)
        tokens = re.findall(r'[A-Z]|\+|\*', expresion)
        
        for token in tokens:
            if token.isupper():  # Es una matriz
                salida.append(token)
            elif token in precedencia:  # Es un operador
                while (pila_operadores and pila_operadores[-1] in precedencia and 
                       precedencia[pila_operadores[-1]] >= precedencia[token]):
                    salida.append(pila_operadores.pop())
                pila_operadores.append(token)
                
        while pila_operadores:
            salida.append(pila_operadores.pop())
            
        return salida

    def validar_dimensiones(self, expresion):
        """Fase 1: Valida si las operaciones de la expresión son matemáticamente posibles"""
        tokens_postfix = self._convertir_a_postfix(expresion)
        pila_evaluacion = []
        
        print("\n--- FASE 1: ANALIZANDO COMPATIBILIDAD MATEMÁTICA ---")
        
        for token in tokens_postfix:
            if token.isupper():
                # Colocamos en la pila las dimensiones de la matriz actual
                pila_evaluacion.append(self.matrices_dimensiones[token])
            else:
                # Si es un operador, necesitamos los dos últimos elementos procesados
                if len(pila_evaluacion) < 2:
                    print("Error: Expresión mal formada.")
                    return False
                
                dim_derecha = pila_evaluacion.pop()   # Matriz 2
                dim_izquierda = pila_evaluacion.pop() # Matriz 1
                
                if token == '*':
                    # Regla: Columnas de la izq == Filas de la der
                    if dim_izquierda[1] != dim_derecha[0]:
                        print(f"[ERROR MATEMÁTICO]: No se puede multiplicar una matriz de "
                              f"{dim_izquierda[0]}x{dim_izquierda[1]} con una de {dim_derecha[0]}x{dim_derecha[1]}.")
                        return False
                    # La matriz resultante tiene las filas de la izq y las columnas de la der
                    dim_resultante = (dim_izquierda[0], dim_derecha[1])
                    pila_evaluacion.append(dim_resultante)
                    print(f"  ✔ Multiplicación válida. Resultado temporal: {dim_resultante[0]}x{dim_resultante[1]}")
                    
                elif token == '+':
                    # Regla: Dimensiones exactamente iguales
                    if dim_izquierda[0] != dim_derecha[0] or dim_izquierda[1] != dim_derecha[1]:
                        print(f"[ERROR MATEMÁTICO]: No se pueden sumar matrices de dimensiones diferentes: "
                              f"{dim_izquierda[0]}x{dim_izquierda[1]} + {dim_derecha[0]}x{dim_derecha[1]}.")
                        return False
                    # La suma mantiene las mismas dimensiones
                    pila_evaluacion.append(dim_izquierda)
                    print(f"  ✔ Suma válida. Resultado temporal: {dim_izquierda[0]}x{dim_izquierda[1]}")
        
        dim_final = pila_evaluacion[0]
        print(f"\n[ÉXITO]: La expresión es matemáticamente válida. Dimensión final: {dim_final[0]}x{dim_final[1]}")
        return True

# --- PRUEBA DEL FLUJO ---
if __name__ == "__main__":
    validador = ValidadorExpresion()
    expresion, dimensiones = validador.solicitar_datos()
    
    if expresion:
        es_valido = validador.validar_dimensiones(expresion)
        if es_valido:
            print("¡Listo para pasar a la Fase de Optimización!")
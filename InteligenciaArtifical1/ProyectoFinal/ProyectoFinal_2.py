import re

class NodoGrafo:
    def __init__(self, nombre, tipo, dimensiones, izquierdo=None, derecho=None):
        self.nombre = nombre          # Ej: 'A', 'Mult_1', 'Suma_1'
        self.tipo = tipo              # 'MATRIZ' o 'OPERACION'
        self.dimensiones = dimensiones  # Tupla (filas, columnas)
        self.izquierdo = izquierdo    # Nodo hijo izquierdo de la operación
        self.derecho = derecho        # Nodo hijo derecho de la operación

class ValidadorExpresion:
    def __init__(self):
        self.matrices_dimensiones = {}
        self.contador_ops = {"*": 1, "+": 1} # Para nombrar las operaciones de forma única

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
        precedencia = {'+': 1, '*': 2}
        salida = []
        pila_operadores = []
        tokens = re.findall(r'[A-Z]|\+|\*', expresion)
        
        for token in tokens:
            if token.isupper():
                salida.append(token)
            elif token in precedencia:
                while (pila_operadores and pila_operadores[-1] in precedencia and 
                       precedencia[pila_operadores[-1]] >= precedencia[token]):
                    salida.append(pila_operadores.pop())
                pila_operadores.append(token)
                
        while pila_operadores:
            salida.append(pila_operadores.pop())
            
        return salida

    def construir_y_validar_grafo(self, expresion):
        """Fase 1 Mejorada: Valida dimensiones y construye el Grafo de Dependencias"""
        tokens_postfix = self._convertir_a_postfix(expresion)
        pila_nodos = []
        
        print("\n--- FASE 1: ANALIZANDO COMPATIBILIDAD Y CONSTRUYENDO GRAFO ---")
        
        for token in tokens_postfix:
            if token.isupper():
                # Crear un nodo hoja para la matriz
                dim = self.matrices_dimensiones[token]
                nodo_matriz = NodoGrafo(token, 'MATRIZ', dim)
                pila_nodos.append(nodo_matriz)
            else:
                if len(pila_nodos) < 2:
                    print("Error: Expresión mal formada.")
                    return None
                
                nodo_derecho = pila_nodos.pop()
                nodo_izquierdo = pila_nodos.pop()
                
                if token == '*':
                    if nodo_izquierdo.dimensiones[1] != nodo_derecho.dimensiones[0]:
                        print(f"[ERROR MATEMÁTICO]: No se puede multiplicar {nodo_izquierdo.nombre} ({nodo_izquierdo.dimensiones[0]}x{nodo_izquierdo.dimensiones[1]}) con {nodo_derecho.nombre} ({nodo_derecho.dimensiones[0]}x{nodo_derecho.dimensiones[1]}).")
                        return None
                    dim_res = (nodo_izquierdo.dimensiones[0], nodo_derecho.dimensiones[1])
                    nombre_op = f"Multiplicacion_{self.contador_ops['*']}"
                    self.contador_ops['*'] += 1
                    
                elif token == '+':
                    if nodo_izquierdo.dimensiones != nodo_derecho.dimensiones:
                        print(f"[ERROR MATEMÁTICO]: No se pueden sumar dimensiones distintas: {nodo_izquierdo.dimensiones} + {nodo_derecho.dimensiones}")
                        return None
                    dim_res = nodo_izquierdo.dimensiones
                    nombre_op = f"Suma_{self.contador_ops['+']}"
                    self.contador_ops['+'] += 1
                
                # Crear el nodo de la operación enlazando sus dependencias (hijos)
                nodo_op = NodoGrafo(nombre_op, 'OPERACION', dim_res, nodo_izquierdo, nodo_derecho)
                pila_nodos.append(nodo_op)
                print(f"  ✔ Conectado nodo: {nombre_op} [{dim_res[0]}x{dim_res[1]}]")
        
        # El último nodo que queda en la pila es la raíz de todo el grafo (la operación final)
        raiz_grafo = pila_nodos[0]
        print("\n[ÉXITO]: Grafo construido correctamente.")
        return raiz_grafo

    def mostrar_grafo(self, nodo, nivel=0, prefijo="Raíz: "):
        """Muestra el grafo de forma visual/textual en la consola mediante recursión"""
        if nodo is not None:
            print(" " * (nivel * 4) + prefijo + f"{nodo.nombre} ({nodo.tipo}) - Dim: {nodo.dimensiones[0]}x{nodo.dimensiones[1]}")
            if nodo.tipo == 'OPERACION':
                self.mostrar_grafo(nodo.izquierdo, nivel + 1, "├── Izq (Depende de): ")
                self.mostrar_grafo(nodo.derecho, nivel + 1, "└── Der (Depende de): ")

# --- PRUEBA DEL FLUJO ---
if __name__ == "__main__":
    validador = ValidadorExpresion()
    expresion, dimensiones = validador.solicitar_datos()
    
    if expresion:
        raiz = validador.construir_y_validar_grafo(expresion)
        if raiz:
            print("\n--- REPRESENTACIÓN DEL GRAFO DE DEPENDENCIAS ---")
            validador.mostrar_grafo(raiz)
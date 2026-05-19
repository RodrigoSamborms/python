import re
import random
import math

class NodoGrafo:
    def __init__(self, nombre, tipo, dimensiones, izquierdo=None, derecho=None):
        self.nombre = nombre
        self.tipo = tipo
        self.dimensiones = dimensiones
        self.izquierdo = izquierdo
        self.derecho = derecho

class ValidadorExpresion:
    def __init__(self):
        self.matrices_dimensiones = {}
        self.contador_ops = {"*": 1, "+": 1}

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
        tokens_postfix = self._convertir_a_postfix(expresion)
        pila_nodos = []
        
        for token in tokens_postfix:
            if token.isupper():
                dim = self.matrices_dimensiones[token]
                nodo_matriz = NodoGrafo(token, 'MATRIZ', dim)
                pila_nodos.append(nodo_matriz)
            else:
                if len(pila_nodos) < 2: return None
                nodo_derecho = pila_nodos.pop()
                nodo_izquierdo = pila_nodos.pop()
                
                if token == '*':
                    if nodo_izquierdo.dimensiones[1] != nodo_derecho.dimensiones[0]:
                        print(f"[ERROR MATEMÁTICO]: No se pueden sumar dimensiones distintas...")
                        return None
                    dim_res = (nodo_izquierdo.dimensiones[0], nodo_derecho.dimensiones[1])
                    nombre_op = f"Multiplicacion_{self.contador_ops['*']}"
                    self.contador_ops['*'] += 1
                elif token == '+':
                    if nodo_izquierdo.dimensiones != nodo_derecho.dimensiones:
                        return None
                    dim_res = nodo_izquierdo.dimensiones
                    nombre_op = f"Suma_{self.contador_ops['+']}"
                    self.contador_ops['+'] += 1
                
                nodo_op = NodoGrafo(nombre_op, 'OPERACION', dim_res, nodo_izquierdo, nodo_derecho)
                pila_nodos.append(nodo_op)
        
        return pila_nodos[0]

class OptimizadorProcesos:
    def __init__(self, raiz_grafo, overhead_hilo=50000):
        self.raiz = raiz_grafo
        self.OVERHEAD = overhead_hilo  # Costo "castigo" por crear hilos en el OS
        self.operaciones_independientes = []
        self._detectar_multiplicaciones_iniciales(self.raiz)

    def _detectar_multiplicaciones_iniciales(self, nodo):
        """Identifica del grafo qué multiplicaciones base pueden paralelizarse"""
        if nodo is not None and nodo.tipo == 'OPERACION':
            if nodo.nombre.startswith("Multiplicacion"):
                self.operaciones_independientes.append(nodo)
            self._detectar_multiplicaciones_iniciales(nodo.izquierdo)
            self._detectar_multiplicaciones_iniciales(nodo.derecho)

    def calcular_costo_operacion(self, nodo):
        """Calcula el costo teórico matemático (M * N * P)"""
        if nodo.nombre.startswith("Multiplicacion"):
            M = nodo.izquierdo.dimensiones[0]
            N = nodo.izquierdo.dimensiones[1]
            P = nodo.derecho.dimensiones[1]
            return M * N * P
        elif nodo.nombre.startswith("Suma"):
            # Una suma toma solo M * N operaciones elementales
            return nodo.izquierdo.dimensiones[0] * nodo.izquierdo.dimensiones[1]
        return 0

    def evaluar_estrategia(self, estrategia):
        """
        Función de aptitud corregida.
        Garantiza que el paralelismo sea real y penaliza la asimetría 
        en tareas del mismo nivel jerárquico.
        """
        tiempo_ramas = []
        
        # 1. Calcular el costo base de cada operación
        for i, nodo in enumerate(self.operaciones_independientes):
            costo_calculo = self.calcular_costo_operacion(nodo)
            usa_hilos = estrategia[i]
            
            if usa_hilos:
                tiempo_ramas.append(costo_calculo + self.OVERHEAD)
            else:
                tiempo_ramas.append(costo_calculo)
        
        # 2. Lógica de ejecución del Sistema Operativo
        if all(estrategia):
            # PARALELISMO PURO: Todos son hilos independientes en núcleos separados.
            # El tiempo es el de la rama más lenta (corren en simultáneo).
            tiempo_multiplicaciones = max(tiempo_ramas) if tiempo_ramas else 0
        elif not any(estrategia):
            # SECUENCIAL PURO: Ninguno usa hilos, corren uno detrás de otro en un solo núcleo.
            tiempo_multiplicaciones = sum(tiempo_ramas)
        else:
            # ESTRATEGIA MIXTA (Inestable en el mundo real): 
            # Una rama crea un hilo y la otra corre en el hilo principal bloqueándolo.
            # Esto genera un retraso por desbalance de carga, lo simulamos sumando un porcentaje de penalización.
            tiempo_multiplicaciones = max(tiempo_ramas) + (self.OVERHEAD * 2)

        # 3. Sumar el costo de la operación final (Suma)
        tiempo_suma = self.calcular_costo_operacion(self.raiz)
        
        return tiempo_multiplicaciones + tiempo_suma

    def optimizar_con_recocido_simulado(self):
        """Algoritmo Metaheurístico para decidir la mejor estrategia de hilos"""
        print("\n--- FASE 2: INICIANDO OPTIMIZACIÓN METAHEURÍSTICA ---")
        
        # Una solución/estrategia inicial aleatoria (ej: [True, False])
        solucion_actual = [random.choice([True, False]) for _ in self.operaciones_independientes]
        costo_actual = self.evaluar_estrategia(solucion_actual)
        
        mejor_solucion = list(solucion_actual)
        mejor_costo = costo_actual
        
        # Parámetros del Recocido Simulado
        temperatura = 1000.0
        factor_enfriamiento = 0.95
        temperatura_minima = 0.01
        
        while temperatura > temperatura_minima:
            # Generar una solución vecina (cambiar una decisión al azar de True a False o viceversa)
            vecino = list(solucion_actual)
            if vecino:
                idx = random.randint(0, len(vecino) - 1)
                vecino[idx] = not vecino[idx]
            
            costo_vecino = self.evaluar_estrategia(vecino)
            
            # ¿Aceptamos al vecino? (Si es mejor, o por probabilidad si la temperatura es alta)
            if costo_vecino < costo_actual:
                solucion_actual = vecino
                costo_actual = costo_vecino
                if costo_vecino < mejor_costo:
                    mejor_solucion = vecino
                    mejor_costo = costo_vecino
            else:
                # Criterio de aceptación de Metrópolis (evita mínimos locales)
                probabilidad = math.exp((costo_actual - costo_vecino) / temperatura)
                if random.random() < probabilidad:
                    solucion_actual = vecino
                    costo_actual = costo_vecino
                    
            temperatura *= factor_enfriamiento
            
        # Presentación de resultados
        print("\n[RESULTADO DE LA OPTIMIZACIÓN]:")
        for i, nodo in enumerate(self.operaciones_independientes):
            decision = "CREAR HILO (Ejecución Paralela)" if mejor_solucion[i] else "NO CREAR HILO (Ejecución Secuencial)"
            print(f"  -> Para {nodo.nombre}: La metaheurística decidió: {decision}")
            
        print(f"\nTiempo estimado óptimo de ejecución: {mejor_costo} ciclos de reloj.")
        return mejor_solucion

# --- PRUEBA DEL SISTEMA COMPLETO ---
if __name__ == "__main__":
    validador = ValidadorExpresion()
    expresion, dimensiones = validador.solicitar_datos()
    
    if expresion:
        raiz = validador.construir_y_validar_grafo(expresion)
        if raiz:
            # Le pasamos el grafo al optimizador. Fijamos un overhead simulado de 50,000 ciclos.
            optimizador = OptimizadorProcesos(raiz, overhead_hilo=50000)
            optimizador.optimizar_con_recocido_simulado()
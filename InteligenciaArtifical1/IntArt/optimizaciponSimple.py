import random
import numpy as np

#definir rango [-3,3]
ValoresX = [random.randint(-3, 3) for _ in range(15)]
#definir una funcion objetivo
Ydex = [x**2 * random.random() for x in ValoresX]

print("=" * 60)
print("OPTIMIZACIÓN SIMPLE")
print("=" * 60)

print("\nValores X:")
print(ValoresX)
print("\nValores Y:")
print(Ydex)

#Inicializar el vector de soluciones con valores random
#==================================================================
# CREAR MATRIZ CON NUMPY
#==================================================================
# Opción 3a: Matriz con dos filas (X, Y)
vector_matriz1 = np.array([ValoresX, Ydex])

# Opción 3b: Matriz con dos columnas (X, Y)
vector_matriz2 = np.column_stack((ValoresX, Ydex))
"""
print("\n" + "=" * 60)
print("\nMatriz con NumPy (2 filas - X y Y):")
print("-" * 60)
print(vector_matriz1)
print(f"Forma: {vector_matriz1.shape}")

print("\n" + "=" * 60)
print("\nMatriz con NumPy (columnas - X y Y):")
print("-" * 60)
print(vector_matriz2)
print(f"Forma: {vector_matriz2.shape}")

print("\n" + "=" * 60)
print("Acceso a elementos:")
print("-" * 60)
print(f"Fila X: {vector_matriz1[0]}")
print(f"Fila Y: {vector_matriz1[1]}")
print(f"Primera columna (X[0], Y[0]): {vector_matriz2[0]}")
print("=" * 60)
"""
#==================================================================
# MOSTRAR CONJUNTO DE VALORES (X, Y)
#==================================================================
print("\n" + "=" * 60)
print("Conjunto de valores (X, Y) del vector solución:")
print("-" * 60)
print(f"{'Índice':<8} {'ValorX':<12} {'ValorY':<20}")
print("-" * 60)

for i in range(len(ValoresX)):
    print(f"{i:<8} {ValoresX[i]:<12} {Ydex[i]:<20.6f}")

print("-" * 60)
print(f"Total de pares: {len(ValoresX)}")
print("=" * 60)

#==================================================================
# ALGORITMO DE ORDENAMIENTO - QUICKSORT
#==================================================================
def quicksort(vector, izq=0, der=None):
    """
    Implementa el algoritmo quicksort para ordenar pares (X, Y).
    Ordena basándose en los valores Y.
    
    Args:
        vector: Matriz de pares (X, Y) a ordenar
        izq: Índice izquierdo (inicio)
        der: Índice derecho (final)
    
    Returns:
        Vector ordenado
    """
    if der is None:
        der = len(vector) - 1
    
    if izq < der:
        # Partición
        pivote = particion(vector, izq, der)
        # Recursividad izquierda y derecha
        quicksort(vector, izq, pivote - 1)
        quicksort(vector, pivote + 1, der)
    
    return vector


def particion(vector, izq, der):
    """
    Particiona el vector usando el último elemento como pivote.
    
    Args:
        vector: Matriz de pares a particionar
        izq: Índice izquierdo
        der: Índice derecho (posición del pivote)
    
    Returns:
        Índice del pivote después de la partición
    """
    pivote = vector[der][1]  # Valor Y del elemento final
    i = izq - 1
    
    for j in range(izq, der):
        if vector[j][1] <= pivote:  # Compara por valor Y
            i += 1
            # Intercambiar
            vector[i], vector[j] = vector[j], vector[i]
    
    # Colocar el pivote en su posición correcta
    vector[i + 1], vector[der] = vector[der], vector[i + 1]
    return i + 1


# Crear copia del vector para ordenar (para no modificar el original)
vector_ordenado = vector_matriz2.copy()

print("\n" + "=" * 60)
print("Realizando ordenamiento con QUICKSORT...")
print("-" * 60)

# Aplicar quicksort
vector_ordenado = quicksort(vector_ordenado)

print("¡Ordenamiento completado!")
print("\n" + "=" * 60)
print("Conjunto de valores (X, Y) ORDENADO por Y:")
print("-" * 60)
print(f"{'Índice':<8} {'ValorX':<12} {'ValorY':<20}")
print("-" * 60)

for i in range(len(vector_ordenado)):
    x_val = int(vector_ordenado[i][0])
    y_val = vector_ordenado[i][1]
    print(f"{i:<8} {x_val:<12} {y_val:<20.6f}")

print("-" * 60)
print(f"Total de pares: {len(vector_ordenado)}")
print("=" * 60)

#==================================================================
# ALGORITMO DE BÚSQUEDA - BÚSQUEDA DEL MÍNIMO
#==================================================================
def buscar_minimo_cercano(vector):
    """
    Busca el valor Y más cercano al mínimo (0) en el vector ordenado.
    Como el vector está ordenado, el primer elemento es el mínimo.
    
    Args:
        vector: Vector ordenado de pares (X, Y)
    
    Returns:
        Tupla con (índice, par_encontrado, valor_Y)
    """
    # El primer elemento tiene el valor Y más pequeño (mínimo)
    indice_minimo = 0
    par_minimo = vector[indice_minimo]
    valor_y_minimo = par_minimo[1]
    
    return indice_minimo, par_minimo, valor_y_minimo


print("\n" + "=" * 60)
print("Búsqueda del punto óptimo (más cercano al mínimo de Y)")
print("-" * 60)

# Encontrar el mínimo
indice_opt, par_opt, valor_y_opt = buscar_minimo_cercano(vector_ordenado)

print(f"\nObjetivo: Encontrar Y más cercano a 0 (función cuadrática)")
print(f"\nResultado de la búsqueda:")
print(f"  Índice en vector ordenado: {indice_opt}")
print(f"  ValorX óptimo: {int(par_opt[0])}")
print(f"  ValorY mínimo: {valor_y_opt:.6f}")
print(f"\n  Par óptimo encontrado: ({int(par_opt[0])}, {valor_y_opt:.6f})")

print("\n" + "=" * 60)
print("Comparación con el objetivo:")
print("-" * 60)
print(f"Objetivo: Y = 0.0 (mínimo teórico de función cuadrática)")
print(f"Encontrado: Y = {valor_y_opt:.6f}")
print(f"Diferencia: {abs(0.0 - valor_y_opt):.6f}")
print(f"\nEl valor X que minimiza la función es: {int(par_opt[0])}")
print("=" * 60)


import random

def heapify(lista, n, i):
    """
    Convierte un árbol binario en un max-heap
    """
    mayor = i
    izq = 2 * i + 1
    der = 2 * i + 2
    
    if izq < n and lista[izq] > lista[mayor]:
        mayor = izq
    
    if der < n and lista[der] > lista[mayor]:
        mayor = der
    
    if mayor != i:
        lista[i], lista[mayor] = lista[mayor], lista[i]
        heapify(lista, n, mayor)


def heap_sort(lista):
    """
    Implementación del algoritmo Heap Sort
    """
    lista_copia = lista.copy()
    n = len(lista_copia)
    
    # Construir el heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(lista_copia, n, i)
    
    # Extraer elementos del heap uno por uno
    for i in range(n - 1, 0, -1):
        lista_copia[0], lista_copia[i] = lista_copia[i], lista_copia[0]
        heapify(lista_copia, i, 0)
    
    return lista_copia


def main():
    # Generar lista de 15 números aleatorios entre 0 y 100
    numeros = [random.randint(0, 100) for _ in range(15)]
    
    print("Lista original:")
    print(numeros)
    print(f"\nTotal de elementos: {len(numeros)}")
    
    # Ordenar usando Heap Sort
    numeros_ordenados = heap_sort(numeros)
    
    print("\nLista ordenada:")
    print(numeros_ordenados)
    
    # Verificar que está ordenada correctamente
    esta_ordenada = all(numeros_ordenados[i] <= numeros_ordenados[i+1] 
                        for i in range(len(numeros_ordenados)-1))
    print(f"\n¿La lista está correctamente ordenada? {esta_ordenada}")


if __name__ == "__main__":
    main()

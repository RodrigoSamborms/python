import random

def quicksort(lista):
    """
    Implementación del algoritmo QuickSort
    """
    if len(lista) <= 1:
        return lista
    
    # Seleccionar el pivote (elemento del medio)
    pivote = lista[len(lista) // 2]
    
    # Dividir la lista en tres partes
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    
    # Recursivamente ordenar y combinar
    return quicksort(menores) + iguales + quicksort(mayores)


def main():
    # Generar lista de 15 números aleatorios entre 0 y 100
    numeros = [random.randint(0, 100) for _ in range(15)]
    
    print("Lista original:")
    print(numeros)
    print(f"\nTotal de elementos: {len(numeros)}")
    
    # Ordenar usando QuickSort
    numeros_ordenados = quicksort(numeros)
    
    print("\nLista ordenada:")
    print(numeros_ordenados)
    
    # Verificar que está ordenada correctamente
    esta_ordenada = all(numeros_ordenados[i] <= numeros_ordenados[i+1] 
                        for i in range(len(numeros_ordenados)-1))
    print(f"\n¿La lista está correctamente ordenada? {esta_ordenada}")


if __name__ == "__main__":
    main()

import random

def selection_sort(lista):
    """
    Implementación del algoritmo Selection Sort
    """
    lista_copia = lista.copy()
    n = len(lista_copia)
    
    for i in range(n):
        # Encontrar el índice del elemento mínimo
        min_idx = i
        for j in range(i + 1, n):
            if lista_copia[j] < lista_copia[min_idx]:
                min_idx = j
        
        # Intercambiar el elemento actual con el mínimo
        lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
    
    return lista_copia


def main():
    # Generar lista de 15 números aleatorios entre 0 y 100
    numeros = [random.randint(0, 100) for _ in range(15)]
    
    print("Lista original:")
    print(numeros)
    print(f"\nTotal de elementos: {len(numeros)}")
    
    # Ordenar usando Selection Sort
    numeros_ordenados = selection_sort(numeros)
    
    print("\nLista ordenada:")
    print(numeros_ordenados)
    
    # Verificar que está ordenada correctamente
    esta_ordenada = all(numeros_ordenados[i] <= numeros_ordenados[i+1] 
                        for i in range(len(numeros_ordenados)-1))
    print(f"\n¿La lista está correctamente ordenada? {esta_ordenada}")


if __name__ == "__main__":
    main()

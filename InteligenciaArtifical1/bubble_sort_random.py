import random

def bubble_sort(lista):
    """
    Implementación del algoritmo Bubble Sort
    """
    lista_copia = lista.copy()
    n = len(lista_copia)
    
    for i in range(n):
        intercambio = False
        for j in range(0, n - i - 1):
            if lista_copia[j] > lista_copia[j + 1]:
                lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
                intercambio = True
        
        # Si no hay intercambios, la lista ya está ordenada
        if not intercambio:
            break
    
    return lista_copia


def main():
    # Generar lista de 15 números aleatorios entre 0 y 100
    numeros = [random.randint(0, 100) for _ in range(15)]
    
    print("Lista original:")
    print(numeros)
    print(f"\nTotal de elementos: {len(numeros)}")
    
    # Ordenar usando Bubble Sort
    numeros_ordenados = bubble_sort(numeros)
    
    print("\nLista ordenada:")
    print(numeros_ordenados)
    
    # Verificar que está ordenada correctamente
    esta_ordenada = all(numeros_ordenados[i] <= numeros_ordenados[i+1] 
                        for i in range(len(numeros_ordenados)-1))
    print(f"\n¿La lista está correctamente ordenada? {esta_ordenada}")


if __name__ == "__main__":
    main()

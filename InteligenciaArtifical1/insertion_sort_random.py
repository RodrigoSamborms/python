import random

def insertion_sort(lista):
    """
    Implementación del algoritmo Insertion Sort
    """
    lista_copia = lista.copy()
    
    for i in range(1, len(lista_copia)):
        clave = lista_copia[i]
        j = i - 1
        
        while j >= 0 and lista_copia[j] > clave:
            lista_copia[j + 1] = lista_copia[j]
            j -= 1
        
        lista_copia[j + 1] = clave
    
    return lista_copia


def main():
    # Generar lista de 15 números aleatorios entre 0 y 100
    numeros = [random.randint(0, 100) for _ in range(15)]
    
    print("Lista original:")
    print(numeros)
    print(f"\nTotal de elementos: {len(numeros)}")
    
    # Ordenar usando Insertion Sort
    numeros_ordenados = insertion_sort(numeros)
    
    print("\nLista ordenada:")
    print(numeros_ordenados)
    
    # Verificar que está ordenada correctamente
    esta_ordenada = all(numeros_ordenados[i] <= numeros_ordenados[i+1] 
                        for i in range(len(numeros_ordenados)-1))
    print(f"\n¿La lista está correctamente ordenada? {esta_ordenada}")


if __name__ == "__main__":
    main()

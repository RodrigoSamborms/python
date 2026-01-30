import random

def merge(izq, der):
    """
    Combina dos listas ordenadas en una sola lista ordenada
    """
    resultado = []
    i = j = 0
    
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    
    # Agregar elementos restantes
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    
    return resultado


def mergesort(lista):
    """
    Implementación del algoritmo MergeSort
    """
    if len(lista) <= 1:
        return lista
    
    # Dividir la lista en dos mitades
    mitad = len(lista) // 2
    izq = lista[:mitad]
    der = lista[mitad:]
    
    # Recursivamente ordenar las dos mitades
    izq_ordenada = mergesort(izq)
    der_ordenada = mergesort(der)
    
    # Combinar las mitades ordenadas
    return merge(izq_ordenada, der_ordenada)


def main():
    # Generar lista de 15 números aleatorios entre 0 y 100
    numeros = [random.randint(0, 100) for _ in range(15)]
    
    print("Lista original:")
    print(numeros)
    print(f"\nTotal de elementos: {len(numeros)}")
    
    # Ordenar usando MergeSort
    numeros_ordenados = mergesort(numeros)
    
    print("\nLista ordenada:")
    print(numeros_ordenados)
    
    # Verificar que está ordenada correctamente
    esta_ordenada = all(numeros_ordenados[i] <= numeros_ordenados[i+1] 
                        for i in range(len(numeros_ordenados)-1))
    print(f"\n¿La lista está correctamente ordenada? {esta_ordenada}")


if __name__ == "__main__":
    main()

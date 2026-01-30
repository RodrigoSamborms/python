"""
Algoritmo de Búsqueda Lineal
Genera 15 valores aleatorios y realiza una búsqueda lineal
"""
import random


def busqueda_lineal(lista, valor_buscado):
    """
    Implementa el algoritmo de búsqueda lineal.
    
    Args:
        lista: Lista de valores donde buscar
        valor_buscado: Valor a buscar en la lista
    
    Returns:
        El índice donde se encuentra el valor, o -1 si no se encuentra
    """
    comparaciones = 0
    for i in range(len(lista)):
        comparaciones += 1
        if lista[i] == valor_buscado:
            print(f"Valor encontrado después de {comparaciones} comparaciones")
            return i
    
    print(f"Valor no encontrado después de {comparaciones} comparaciones")
    return -1


def main():
    # Generar 15 valores aleatorios entre 1 y 100
    print("=" * 50)
    print("BÚSQUEDA LINEAL")
    print("=" * 50)
    
    lista = [random.randint(1, 100) for _ in range(15)]
    
    print("\nValores generados:")
    print("-" * 50)
    for i, valor in enumerate(lista):
        print(f"Posición {i}: {valor}")
    print("-" * 50)
    print(f"\nLista completa: {lista}")
    print("\n" + "=" * 50)
    
    # Solicitar al usuario el valor a buscar
    try:
        valor_buscado = int(input("\nIngrese el valor a buscar de la lista: "))
        
        print("\nRealizando búsqueda lineal...")
        print("-" * 50)
        
        # Realizar la búsqueda
        posicion = busqueda_lineal(lista, valor_buscado)
        
        # Mostrar el resultado
        print("-" * 50)
        if posicion != -1:
            print(f"\n✓ El valor {valor_buscado} fue encontrado en la posición {posicion}")
        else:
            print(f"\n✗ El valor {valor_buscado} no se encuentra en la lista")
        
        print("=" * 50)
        
    except ValueError:
        print("Error: Debe ingresar un número entero válido")


if __name__ == "__main__":
    main()

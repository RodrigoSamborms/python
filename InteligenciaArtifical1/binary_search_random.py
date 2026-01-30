"""
Algoritmo de Búsqueda Binaria
Genera 15 valores aleatorios, los ordena y realiza una búsqueda binaria
"""
import random


#==================================================================
# ALGORITMO DE BÚSQUEDA BINARIA
#==================================================================
def busqueda_binaria(lista, valor_buscado):
    """
    Implementa el algoritmo de búsqueda binaria.
    IMPORTANTE: La lista debe estar ordenada.
    
    Args:
        lista: Lista ordenada de valores donde buscar
        valor_buscado: Valor a buscar en la lista
    
    Returns:
        El índice donde se encuentra el valor, o -1 si no se encuentra
    """
    izquierda = 0
    derecha = len(lista) - 1
    comparaciones = 0
    
    print(f"Buscando el valor {valor_buscado} en la lista ordenada...")
    print(f"Rango inicial: [{izquierda}, {derecha}]\n")
    
    while izquierda <= derecha:
        comparaciones += 1
        medio = (izquierda + derecha) // 2
        
        print(f"Comparación {comparaciones}:")
        print(f"  Rango: [{izquierda}, {derecha}]")
        print(f"  Índice medio: {medio}, Valor: {lista[medio]}")
        
        if lista[medio] == valor_buscado:
            print(f"  ✓ ¡Valor encontrado!")
            print(f"\nValor encontrado después de {comparaciones} comparaciones")
            return medio
        elif lista[medio] < valor_buscado:
            print(f"  {lista[medio]} < {valor_buscado}, buscar en mitad derecha")
            izquierda = medio + 1
        else:
            print(f"  {lista[medio]} > {valor_buscado}, buscar en mitad izquierda")
            derecha = medio - 1
        print()
    
    print(f"Valor no encontrado después de {comparaciones} comparaciones")
    return -1
#==================================================================


def main():
    # Generar 15 valores aleatorios entre 1 y 100
    print("=" * 60)
    print("BÚSQUEDA BINARIA")
    print("=" * 60)
    
    lista = [random.randint(1, 100) for _ in range(15)]
    
    print("\nValores generados (desordenados):")
    print("-" * 60)
    for i, valor in enumerate(lista):
        print(f"Posición {i}: {valor}")
    print("-" * 60)
    print(f"\nLista original: {lista}")
    
    # Ordenar la lista para búsqueda binaria
    lista_ordenada = sorted(lista)
    
    print("\n" + "=" * 60)
    print("\nValores después de ordenar:")
    print("-" * 60)
    for i, valor in enumerate(lista_ordenada):
        print(f"Posición {i}: {valor}")
    print("-" * 60)
    print(f"\nLista ordenada: {lista_ordenada}")
    print("\n" + "=" * 60)
    
    # Solicitar al usuario el valor a buscar
    try:
        valor_buscado = int(input("\nIngrese el valor a buscar de la lista: "))
        
        print("\n" + "=" * 60)
        print("Realizando búsqueda binaria...")
        print("-" * 60)
        
        # Realizar la búsqueda
        posicion = busqueda_binaria(lista_ordenada, valor_buscado)
        
        # Mostrar el resultado
        print("-" * 60)
        if posicion != -1:
            print(f"\n✓ El valor {valor_buscado} fue encontrado en la posición {posicion}")
            print(f"  (en la lista ordenada)")
        else:
            print(f"\n✗ El valor {valor_buscado} no se encuentra en la lista")
        
        print("=" * 60)
        
    except ValueError:
        print("Error: Debe ingresar un número entero válido")


if __name__ == "__main__":
    main()

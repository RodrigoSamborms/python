"""
Algoritmo de Búsqueda por Interpolación
Genera 15 valores aleatorios, los ordena y realiza una búsqueda por interpolación
"""
import random


#==================================================================
# ALGORITMO DE BÚSQUEDA POR INTERPOLACIÓN
#==================================================================
def busqueda_interpolacion(lista, valor_buscado):
    """
    Implementa el algoritmo de búsqueda por interpolación.
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
    print(f"Rango inicial: [{izquierda}, {derecha}]")
    print(f"Valores en extremos: lista[{izquierda}]={lista[izquierda]}, lista[{derecha}]={lista[derecha]}\n")
    
    while izquierda <= derecha and valor_buscado >= lista[izquierda] and valor_buscado <= lista[derecha]:
        comparaciones += 1
        
        # Si los valores en los extremos son iguales, evitar división por cero
        if lista[izquierda] == lista[derecha]:
            if lista[izquierda] == valor_buscado:
                print(f"Comparación {comparaciones}:")
                print(f"  Valores en extremos son iguales")
                print(f"  ✓ ¡Valor encontrado!")
                print(f"\nValor encontrado después de {comparaciones} comparaciones")
                return izquierda
            else:
                break
        
        # Calcular posición estimada usando interpolación
        pos = izquierda + int(((valor_buscado - lista[izquierda]) * (derecha - izquierda)) / (lista[derecha] - lista[izquierda]))
        
        print(f"Comparación {comparaciones}:")
        print(f"  Rango: [{izquierda}, {derecha}]")
        print(f"  Valores: lista[{izquierda}]={lista[izquierda]}, lista[{derecha}]={lista[derecha]}")
        print(f"  Posición estimada: {pos}, Valor: {lista[pos]}")
        
        if lista[pos] == valor_buscado:
            print(f"  ✓ ¡Valor encontrado!")
            print(f"\nValor encontrado después de {comparaciones} comparaciones")
            return pos
        elif lista[pos] < valor_buscado:
            print(f"  {lista[pos]} < {valor_buscado}, buscar en parte derecha")
            izquierda = pos + 1
        else:
            print(f"  {lista[pos]} > {valor_buscado}, buscar en parte izquierda")
            derecha = pos - 1
        print()
    
    print(f"Valor no encontrado después de {comparaciones} comparaciones")
    return -1
#==================================================================


def main():
    # Generar 15 valores aleatorios entre 1 y 100
    print("=" * 60)
    print("BÚSQUEDA POR INTERPOLACIÓN")
    print("=" * 60)
    
    lista = [random.randint(1, 100) for _ in range(15)]
    
    print("\nValores generados (desordenados):")
    print("-" * 60)
    for i, valor in enumerate(lista):
        print(f"Posición {i}: {valor}")
    print("-" * 60)
    print(f"\nLista original: {lista}")
    
    # Ordenar la lista para búsqueda por interpolación
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
        print("Realizando búsqueda por interpolación...")
        print("-" * 60)
        
        # Realizar la búsqueda
        posicion = busqueda_interpolacion(lista_ordenada, valor_buscado)
        
        # Mostrar el resultado
        print("-" * 60)
        if posicion != -1:
            print(f"\n✓ El valor {valor_buscado} fue encontrado en la posición {posicion}")
            print(f"  (en la lista ordenada)")
        else:
            print(f"\n✗ El valor {valor_buscado} no se encuentra en la lista")
        
        print("\n" + "=" * 60)
        print("NOTA: La búsqueda por interpolación estima la posición")
        print("      basándose en la distribución de valores, siendo")
        print("      más eficiente que búsqueda binaria en datos uniformes.")
        print("=" * 60)
        
    except ValueError:
        print("Error: Debe ingresar un número entero válido")


if __name__ == "__main__":
    main()

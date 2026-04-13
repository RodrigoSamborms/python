# 1. Definición de la clase del Nodo
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.deredo = None

# 2. Método para obtener elementos por niveles
def obtener_elementos_por_nivel(raiz):
    if not raiz:
        return []

    resultado = []
    cola = [raiz]  # Cola para BFS usando lista
    inicio = 0

    while inicio < len(cola):
        nivel_actual = []
        elementos_en_nivel = len(cola) - inicio  # Cuántos nodos hay en este nivel

        # Procesar todos los nodos del nivel actual
        for _ in range(elementos_en_nivel):
            nodo = cola[inicio]
            inicio += 1
            nivel_actual.append(nodo.valor)
            
            # Añadir hijos a la cola para el siguiente nivel
            if nodo.izquierdo:
                cola.append(nodo.izquierdo)
            if nodo.deredo:
                cola.append(nodo.deredo)
        
        # Agregar la lista del nivel al resultado final
        resultado.append(nivel_actual)

    return resultado

# 3. Ejemplo de Uso
if __name__ == "__main__":
    # Crear árbol:
    #      1
    #     / \
    #    2   3
    #   / \   \
    #  4   5   6
    
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.deredo = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.deredo = Nodo(5)
    raiz.deredo.deredo = Nodo(6)

    niveles = obtener_elementos_por_nivel(raiz)
    print(niveles) # Salida esperada: [[1], [2, 3], [4, 5, 6]]

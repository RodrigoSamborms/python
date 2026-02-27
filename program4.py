if __name__ == '__main__':
    registros = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        registros.append([name, score]) #construyes la lista de registros con el nombre y el puntaje
    print (registros)#DEBUG vemos como quedo la lista
    
    #ordenar por puntaje de menor a mayor y alfabeticamente por nombre
    registros.sort(key=lambda x: (x[1], x[0]))#note como primero ordena por el puntaje y luego por el nombre, ambos de menor a mayor
    print (registros)#DEBUG vemos como quedo la lista ordenada

    print (10*"-")#separador
    
    # Encontrar el puntaje más bajo
    puntaje_mas_bajo = registros[0][1]
    
    # Encontrar el segundo puntaje más bajo (diferente al primero)
    segundo_puntaje = None
    for nombre, puntaje in registros:
        if puntaje > puntaje_mas_bajo:
            segundo_puntaje = puntaje
            break #encontramos un puntaje mayor al más bajo, entonces no hay necesidad de seguir buscando
    
    # Imprimir todos los nombres con el segundo puntaje más bajo
    for nombre, puntaje in registros:
        if puntaje == segundo_puntaje:
            print(nombre)
    
    
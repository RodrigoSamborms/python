if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())
    conjunto = set(arr) #eliminamos duplicados
    lista = list(conjunto) #convertimos el conjunto a lista
    lista = sorted(lista, reverse=True) #ordenamos la lista de mayor a menor
    print (lista[1]) #imprimimos el segundo elemento de la lista que es el segundo numero mas grande
    '''
    lista = list(arr)
    print (lista)
    print (max(lista))
    conjunto = set(lista)
    lista = list(conjunto)
    lista = sorted(lista, reverse=True)
    print (lista)
    print (lista[1])
    '''

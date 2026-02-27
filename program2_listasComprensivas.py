x=int(input("valor x: "))
y=int(input("valor y: "))
z=int(input("valor z: "))
n=int(input("valor n: "))
#Realizamos el calculo, lo que genera una lista de tuplas
lista=[(i, j, k) \
            for i in range(x+1) \
            for j in range(y+1) \
            for k in range(z+1) \
            if i+j+k !=n]
print(lista)
#Convertimos la lista de tuplas a una lista de listas
lista2=[list(t) for t in lista]
print(lista2)
#note como en la primera lista comprensiva se recorren las listas
#donde x, y, z pasadas por range() se vuelven (0 1 2 .. n-1)
#posteriormente especificamos cual variable guardara el valor del recorrido
#donde i es para x j es para y y k es para z, indicamos que debe ser un valor adicional
#limite para x, y y z porque range() llega hasta n-1.
#especificamos un filtro que incluye a los tres guiones, el cual se tomara para
#creara la salida que se pasara a la tupla (i, j, k) y se guardara en la lista.
#como el resultado nos genera una lista de tuplas, debemos convertir las tuplas a listas
#utilizamos una lista2 donde recorremos la lista de tuplas con "for t in lista"
#y en vez de escrbir lista2=[t for ...], tomamos el valor t y le aplicamos una trasformacion a
#lista usando list(t) si deseamos recorrer la lista comprendida por sus elementos internos
#de la lista de tuplas:
#[(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)]
#usamos lista2 = [num for fila in lista for num in fila]
#lo cual genera:
#[0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1]
#es decir "for fila en lista" recorre cada tupla y nos regresa fila como: (se omitieron los valores por claridad)
#(), (), (), (), ()
#y despues "for num in fila"
#recorre cada tupla internamente por ejemplo la primera:
#(0,0,0) generando 0,0,0
#elementos individuales

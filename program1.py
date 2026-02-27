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



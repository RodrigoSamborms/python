def cadenapar(cadena):
    parcadena = []
    for i in range(0, len(cadena)):
        if i % 2 == 0:
            parcadena.append(cadena[i])
    parcadena = "".join(parcadena) #convertimos la lista de caracteres a una cadena
    return parcadena
def cadenaimpar(cadena):
    imparcadena = []
    for i in range(0, len(cadena)):
        if i % 2 != 0:
            imparcadena.append(cadena[i])
    imparcadena = "".join(imparcadena)#convertimos la lista de caracteres a una cadena
    return imparcadena

t = int(input())
S1 = []
for t in range(0,t):
    S1.append(input())
for i in range(0,t+1):
    print(cadenapar(S1[i]), cadenaimpar(S1[i]))
    
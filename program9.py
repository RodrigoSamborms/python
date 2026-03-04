n = int (input()) #Numero de entradas en el directorio y numero de consultas
Directorio = [] #lista de claves par valor nombre y telefono para crear un lista de diccionario.
for i in range (n): #N Entradas del directorio telefonico
    nombre, telefono = input().split() #Entrada de los dos datos separados por espacio
    Directorio.append({"nombre": nombre, "telefono": telefono}) #agregado un elemento a la lista como un 
        #dato diccionario con clave "nombre" y "telefono" y su respectivo valor.

queries = [] #lista de valores a consultar en la lista de diccionario del directorio telefonico.
for i in range (n): #N Datos a consultar en el directorio telefonico
   queries.append(str(input())) #agregamos cada consulta a la lista de consultas.

for i in range (n): #Realizar N consultas en el directorio telefonico
    consulta = queries[i] #obtenemos la consulta a realizar de la lista de consultas.
    for j in range (n): #Recorrer el directorio telefonico con N entradas para encontrar la consulta
        if consulta == Directorio[j]["nombre"]: #si la consulta coincide con el valor de la clave "nombre" del primer elemento de la lista de diccionario
            print(Directorio[j]["nombre"] + "=" + str(Directorio[j]["telefono"]))#escribimos los valores
            break#, y salimos del ciclo for para realizar la siguiente consulta.
    else: #el recorrido por los valores del diccionario no encontro la consulta
        print("Not found")#, entonces se ejecuta el bloque else del ciclo for.
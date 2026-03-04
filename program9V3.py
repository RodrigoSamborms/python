import sys


def main() -> None:
    #Comenzamos leyendo todas las entradas, en vez de usar input()
    #utilizamos un buffer para leer todas las entradas de una sola vez

    data = sys.stdin.buffer.read().splitlines()
    if not data:
        return

    n = int(data[0].strip()) #separamos el valor del numero de entradas del resto de los datos
    directorio = {}

    idx = 1
    for _ in range(n): #comenzamos a llenar el directorio con los datos de entrada
        nombre, telefono = data[idx].decode().split()
        directorio[nombre] = telefono #asignamos en valores clave:valor para cada clave del diccionario
        idx += 1                        #denotado por la variable directorio, note que idx apunta
                                        #al siguiente elemento de los datos que proporcionamos
    salida = []     #variable del tipo lista para almacenar los resultados de las consultas.
    for raw_query in data[idx:]:#idx ahora apunta a la primera consulta, tras llenar el directorio.
        consulta = raw_query.decode().strip() #extraemos el valor del nombre a consultar.
        telefono = directorio.get(consulta)#utilizamos un metodo especializado para obtener el valor buscado
        if telefono is None: #si no lo encontramos agregamos un mensaje de error a la variable salida
            salida.append("Not found")
        else:
            salida.append(f"{consulta}={telefono}") #Si encontramos el valor agregamos el resultado a la lista

    sys.stdout.write("\n".join(salida)) #le damos formato a la salida tomando cada elemento de la variable
        #salida[] y le agregamos el caracter de salto de linea, para separa cada resultado.


if __name__ == "__main__":
    main() #mandamos llamar a Main solo si el programa se ejecuta directamente. no desde un modulo


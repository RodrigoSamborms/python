#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(input().strip())
    arr = list(map(int, input().rstrip().split()))#toma la entrada como una cadena de caracteres, elimina
        #los espacios en blanco a la derecha y luego divide la cadena en elementos individuales, tomando
        #como delimitador el espacio en blanco. Despues convierte estos elementos en un mapa
        #y este mapa lo convierte al tipo lista.
    arr.reverse()#invierte la lista
    print(' '.join(map(str, arr)))#imprime el resultado de convertir una lista de caracteres
                                #a una cadena de caracteres separando cada elemento por un espacio


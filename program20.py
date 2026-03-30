#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(input().strip())

    a = list(map(int, input().rstrip().split()))

    # Write your code here
    #Algoritmo de la burbuja mejorado
    suma = 0
    for i in range(n):
        contador = 0 #contador de intercambios se reinicia en cada pasada
        for j in range(0, n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                contador += 1 #actualizamos el contador de intercambios para la pasada actual
        suma += contador
        if contador == 0: #si no hubo intercambio, el arreglo ya está ordenado
            break #detemos las iteraciones no se requiren mas pasadas
    print('Array is sorted in ' + str(suma) + ' swaps.')
    print('First Element: ' + str(a[0]))
    print('Last Element: ' + str(a[n-1]))
#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    arr = []
    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))
    #print (2*"---")
    #sumMayor = 0
    for i in range(2,6,1): #recorre las filas iniciando en la fila 2
        for j in range(2,6,1):#recorre las columnas iniciando en la columna 2
            '''
            a b c #el inidice de c es (0,2)
              d
            e f g #el inidice de g es (2,2)
            Nos interesa el indice g, porque es el limite del subconjunto
            '''
            #Tomando el limite del subconjunto, calulamos los valores
            sum1 = arr[i-2][j] + arr[i-2][j-1] + arr[i-2][j-2]
            sum2 = arr[i-1][j-1]
            sum3 = arr[i][j] + arr[i][j-1] + arr[i][j-2]
            sum = sum1 + sum2 + sum3
            if (i == 2 and j == 2):#condicion inicial
                sumMayor = sum #la primer suma siempre sera la mayor
            if sum > sumMayor:
                sumMayor = sum
    print (sumMayor)

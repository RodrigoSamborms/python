#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(input().strip())
    #binary_num = bin(n)[2:] #retira el prefijo '0b'
    #print(binary_num)
    #n = 13  # Ejemplo: 13 es 1101 en binario
    n=bin(n)[2:] #retira el prefijo '0b'
    #print (n)
    i = 0
    mayor = 0
    count = 0
    while i < len(n):
        i+=1
        if n[i-1] == '1':
            count += 1
        else:
            count = 0
        if count > mayor:
            mayor = count
    print (mayor)
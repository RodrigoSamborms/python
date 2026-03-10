#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'factorial' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER n as parameter.
#

def factorial(n):
    # Write your code here
    if (n != 0):
        res = n * factorial(n -1) #recursividad para el factorial
        return res
    else:
        return 1 #condicion de salida para la función

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #$env:OUTPUT_PATH = "output.txt" en la teminal PS para evitar el error
    #de variable de entorno no encontrada. antes de llamar al script.
    n = int(input().strip())

    result = factorial(n)

    fptr.write(str(result) + '\n')

    fptr.close()

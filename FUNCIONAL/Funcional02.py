from functools import reduce

numeros = [1, 2, 3, 4, 5, 6]

#### LAS SIGUIENTES LINEAS SE REDUCEN ####
# 1. Filtramos los pares
#pares = filter(lambda x: x % 2 == 0, numeros)
# 2. Elevamos al cuadrado
#cuadrados = map(lambda x: x ** 2, pares)
# 3. Reducimos la lista a un solo valor (la suma)
#resultado = reduce(lambda x, y: x + y, cuadrados)
#### ESTO ES UNA FORMA MAS PYTHONICA ####

# Versión compacta funcional en Python
resultado = sum([x**2 for x in numeros if x % 2 == 0])

print(resultado) # Resultado: 56
from functools import reduce

numeros = [1, 2, 3, 4, 5, 6]

# 1. Filtramos los pares
pares = filter(lambda x: x % 2 == 0, numeros)

# 2. Elevamos al cuadrado
cuadrados = map(lambda x: x ** 2, pares)

# 3. Reducimos la lista a un solo valor (la suma)
resultado = reduce(lambda x, y: x + y, cuadrados)

print(resultado) # Resultado: 56
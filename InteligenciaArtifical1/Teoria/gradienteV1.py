import numpy as np
import matplotlib.pyplot as plt

# Función de costo simple: f(x) = x^2
f = lambda x: x**2
grad = lambda x: 2*x

# Descenso de gradiente
x = 10
eta = 0.1
hist = [x]

for _ in range(20):
    x = x - eta*grad(x)
    hist.append(x)
#mostrar el grafico
plt.plot(range(len(hist)), [f(h) for h in hist], marker='o')
plt.xlabel("Iteración")
plt.ylabel("f(x)")
plt.title("Convergencia Descenso de Gradiente")
plt.show()
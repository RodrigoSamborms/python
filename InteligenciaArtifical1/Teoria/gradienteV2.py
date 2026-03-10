import numpy as np
import matplotlib.pyplot as plt

# Función de costo: f(x, y) = x^2 + y^2
f = lambda x, y: x**2 + y**2
grad = lambda x, y: np.array([2*x, 2*y])

# Descenso de gradiente
x = np.array([10.0, 10.0])
eta = 0.1
hist = [x.copy()]

for _ in range(20):
    x = x - eta * grad(x[0], x[1])
    hist.append(x.copy())

# Mostrar el gráfico en 3D
hist = np.array(hist)
x_hist = hist[:, 0]
y_hist = hist[:, 1]
z_hist = f(x_hist, y_hist)

x_vals = np.linspace(-12, 12, 100)
y_vals = np.linspace(-12, 12, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = f(X, Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
ax.plot(x_hist, y_hist, z_hist, color='red', marker='o', linewidth=2)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x, y)")
ax.set_title("Convergencia Descenso de Gradiente (3D)")
plt.show()
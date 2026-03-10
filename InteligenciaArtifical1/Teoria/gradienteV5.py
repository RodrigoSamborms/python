import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. Definición de la función y sus derivadas
def f(x, y):
    return 0.5 * (3*x**2 + 2*x*y + 2*y**2) - 5*x - 3*y

def gradiente_f(x, y):
    return np.array([3*x + y - 5, x + 2*y - 3])

def hessiana_f():
    # La hessiana es constante para esta función
    return np.array([[3.0, 1.0], [1.0, 2.0]])

# 2. Algoritmo de Newton almacenando el historial
punto_actual = np.array([0.0, 0.0]) # Punto inicial
historial = [punto_actual]

# Como es cuadrática, 1 sola iteración basta
H = hessiana_f()
grad = gradiente_f(punto_actual[0], punto_actual[1])
paso = np.linalg.solve(H, grad)
punto_siguiente = punto_actual - paso
historial.append(punto_siguiente)

historial = np.array(historial)

# 3. Configuración de la Gráfica 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Crear la malla (grid) para la superficie
x_range = np.linspace(-1, 4, 100)
y_range = np.linspace(-1, 4, 100)
X, Y = np.meshgrid(x_range, y_range)
Z = f(X, Y)

# Dibujar la superficie
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, edgecolor='none')

# Dibujar la trayectoria del algoritmo
z_hist = f(historial[:, 0], historial[:, 1])
ax.plot(historial[:, 0], historial[:, 1], z_hist, color='red', marker='o', 
        markersize=8, linewidth=2, label='Trayectoria de Newton', zorder=10)

# Marcar el punto inicial y final
ax.scatter(historial[0,0], historial[0,1], z_hist[0], color='blue', s=100, label='Inicio (0,0)')
ax.scatter(historial[-1,0], historial[-1,1], z_hist[-1], color='gold', s=150, marker='*', label='Mínimo Encontrado')

# Etiquetas y detalles
ax.set_title('Optimización de Newton en 3D')
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('f(x, y)')
ax.legend()

plt.show()
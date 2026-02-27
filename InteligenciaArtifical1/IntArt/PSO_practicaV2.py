import numpy as np
import matplotlib.pyplot as plt

# Función objetivo (función de Booth)
# Mínimo global en (1, 3) con valor 0
def funcion_objetivo(x):
    return (x[0] + 2*x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2

# Parámetros del algoritmo
num_particulas = 30
dimensiones = 2
limites = (-10, 10)
max_iter = 100

w = 0.5      # inercia
c1 = 0.9     # coeficiente cognitivo
c2 = 0.4     # coeficiente social

# Inicialización aleatoria de partículas
posiciones = np.random.uniform(limites[0], limites[1], (num_particulas, dimensiones))
velocidades = np.random.uniform(-1, 1, (num_particulas, dimensiones))
mejor_pos_personal = np.copy(posiciones)
mejor_val_personal = np.array([funcion_objetivo(p) for p in posiciones])

# Mejor posición global
mejor_idx = np.argmin(mejor_val_personal)
mejor_pos_global = mejor_pos_personal[mejor_idx]

# Bucle principal de PSO
for iteracion in range(max_iter):
    for i in range(num_particulas):
        r1, r2 = np.random.rand(), np.random.rand()

        # Actualizar velocidad
        velocidades[i] = (
            w * velocidades[i]
            + c1 * r1 * (mejor_pos_personal[i] - posiciones[i])
            + c2 * r2 * (mejor_pos_global - posiciones[i])
        )

        # Actualizar posición
        posiciones[i] += velocidades[i]

        # Limitar dentro del rango
        posiciones[i] = np.clip(posiciones[i], limites[0], limites[1])

        # Evaluar
        valor_actual = funcion_objetivo(posiciones[i])

        # Actualizar mejor personal
        if valor_actual < mejor_val_personal[i]:
            mejor_val_personal[i] = valor_actual
            mejor_pos_personal[i] = posiciones[i]

    # Actualizar mejor global
    mejor_idx = np.argmin(mejor_val_personal)
    mejor_pos_global = mejor_pos_personal[mejor_idx]

    print(f"Iteración {iteracion+1}: Mejor valor = {mejor_val_personal[mejor_idx]:.4f}")

# Resultado final
print("\nMejor solución encontrada:")
print("Posición:", mejor_pos_global)
print("Valor:", funcion_objetivo(mejor_pos_global))

# =========================
# | Visualización gráfica |
# =========================
# Crear una malla para evaluar la función de Booth
x_range = np.linspace(limites[0], limites[1], 200)
y_range = np.linspace(limites[0], limites[1], 200)
X, Y = np.meshgrid(x_range, y_range)
Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = funcion_objetivo([X[i, j], Y[i, j]])


# Crear la figura
plt.figure(figsize=(12, 5))  #esta contendra todas las graficas

# Subplot 1: Gráfico de contorno
'''
Gráfico de contorno (izquierda): Muestra las curvas de nivel de la función de Booth 
con las partículas finales en azul, la mejor solución encontrada por PSO
como estrella roja, y el mínimo global (1, 3) marcado en verde.
'''
plt.subplot(1, 2, 1)
contour = plt.contour(X, Y, Z, levels=30, cmap='viridis')
plt.colorbar(contour, label='Valor de la función')
plt.scatter(posiciones[:, 0], posiciones[:, 1], c='blue', s=30, alpha=0.6, label='Partículas finales')
plt.scatter(mejor_pos_global[0], mejor_pos_global[1], c='red', s=200, marker='*', 
            edgecolors='black', linewidths=2, label='Mejor solución PSO', zorder=5)
plt.scatter(1, 3, c='green', s=150, marker='X', 
            edgecolors='black', linewidths=2, label='Mínimo global (1, 3)', zorder=5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Función de Booth - Vista de contorno')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2: Gráfico 3D de superficie
'''
Gráfico 3D (derecha): Muestra la superficie de la función de Booth con las mismas 
marcas para visualizar la convergencia en el espacio tridimensional
'''
ax = plt.subplot(1, 2, 2, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, edgecolor='none')
ax.scatter(posiciones[:, 0], posiciones[:, 1], 
           [funcion_objetivo(p) for p in posiciones], 
           c='blue', s=30, alpha=0.8, label='Partículas finales')
ax.scatter(mejor_pos_global[0], mejor_pos_global[1], funcion_objetivo(mejor_pos_global), 
           c='red', s=200, marker='*', edgecolors='black', linewidths=2, label='Mejor solución PSO')
ax.scatter(1, 3, 0, c='green', s=150, marker='X', 
           edgecolors='black', linewidths=2, label='Mínimo global')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
ax.set_title('Función de Booth - Vista 3D')
plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
ax.legend()

plt.tight_layout()
plt.show()
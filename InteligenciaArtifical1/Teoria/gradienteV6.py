import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. Definición de la función y sus componentes (basados en tus cálculos de Maxima)
def f(x, y):
    return 0.5 * (3*x**2 + 2*x*y + 2*y**2) - 5*x - 3*y

def gradiente_f(x, y):
    # Resultado de Maxima: [3x + y - 5, x + 2y - 3]
    return np.array([3*x + y - 5, x + 2*y - 3])

def hessiana_f():
    # Resultado de Maxima: [[3, 1], [1, 2]]
    return np.array([[3.0, 1.0], [1.0, 2.0]])

# 2. Algoritmo de Newton con salida a consola y registro de historial
def optimizacion_newton_visual(punto_inicial, max_iter=5, tol=1e-6):
    x_k = np.array(punto_inicial, dtype=float)
    historial = [x_k.copy()]
    
    print(f"{'Iteración':<10} | {'Punto (x, y)':<25} | {'f(x,y)':<15}")
    print("-" * 60)
    
    for i in range(max_iter):
        valor_z = f(x_k[0], x_k[1])
        print(f"{i:<10} | {str(np.round(x_k, 4)):<25} | {valor_z:<15.6f}")
        
        grad = gradiente_f(x_k[0], x_k[1])
        
        # Si el gradiente es muy pequeño, ya estamos en el mínimo
        if np.linalg.norm(grad) < tol:
            print("-" * 60)
            print(f"Convergencia alcanzada en la iteración {i}.")
            break
            
        H = hessiana_f()
        
        # Paso de Newton: Inversa de Hessiana por Gradiente
        paso = np.linalg.solve(H, grad)
        x_k = x_k - paso
        historial.append(x_k.copy())
        
    return np.array(historial)

# --- EJECUCIÓN ---
punto_inicio = [0.0, 0.0]
historial_puntos = optimizacion_newton_visual(punto_inicio)

# 3. Creación de la Gráfica 3D
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection='3d')

# Crear malla para la superficie
x_range = np.linspace(-1, 4, 100)
y_range = np.linspace(-1, 4, 100)
X, Y = np.meshgrid(x_range, y_range)
Z = f(X, Y)

# Dibujar superficie
surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.5, antialiased=True)

# Dibujar la trayectoria (puntos y línea)
z_hist = [f(p[0], p[1]) for p in historial_puntos]
ax.plot(historial_puntos[:, 0], historial_puntos[:, 1], z_hist, 
        color='black', marker='o', markersize=5, linewidth=2, label='Trayectoria Newton', zorder=10)

# Resaltar puntos clave
ax.scatter(historial_puntos[0,0], historial_puntos[0,1], z_hist[0], 
           color='blue', s=100, label='Inicio (0,0)')
ax.scatter(historial_puntos[-1,0], historial_puntos[-1,1], z_hist[-1], 
           color='green', s=150, marker='*', label=f'Mínimo: {np.round(historial_puntos[-1], 2)}')



# Estética de la gráfica
ax.set_title('Visualización del Método de Newton')
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('f(x, y)')
ax.legend()

plt.show()
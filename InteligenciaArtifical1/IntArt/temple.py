import numpy as np
import math
import random
import matplotlib.pyplot as plt

# ---------------------
# Definición de funciones
# ---------------------
#pagina de referencia https://www.sfu.ca/~ssurjano/optimization.html

'''
# Función peaks
def peaks(x, y):
    return  3*(1 - x)**2 * np.exp(-(x**2) - (y + 1)**2) \
          - 10*(x/5 - x**3 - y**5) * np.exp(-x**2 - y**2) \
          - (1/3)*np.exp(-(x + 1)**2 - y**2)
'''

def booth(x, y):
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2    

# Función objetivo (negada para convertir a minimización)
def objective_function(position):
    x, y = position
    #return peaks(x, y)
    return booth(x,y)

# Límites del espacio de búsqueda
lower_bound = np.array([-3, -3])
upper_bound = np.array([3, 3])  #rangos de los valores de la funcion peaks y booth para busqueda

# Generar vecino dentro de los límites
def neighbor(position, step_size=0.1):
    new_position = position + np.random.uniform(-step_size, step_size, size=2)
    return np.clip(new_position, lower_bound, upper_bound)

# Probabilidad de aceptación
def acceptance_probability(current_energy, neighbor_energy, temperature):
    if neighbor_energy < current_energy:
        return 1.0
    return math.exp((current_energy - neighbor_energy) / temperature)

# Simulated Annealing con salto aleatorio
def simulated_annealing(initial_solution, initial_temperature,
                        cooling_rate, max_iterations,
                        max_no_improve=100):
    
    current_solution = initial_solution
    current_energy = objective_function(current_solution)
    
    best_solution = current_solution
    best_energy = current_energy

    temperature = initial_temperature
    path = [current_solution.copy()]
    jump_points = []  # Para guardar dónde se hicieron los saltos aleatorios

    no_improve_count = 0

    for iteration in range(max_iterations):
        new_solution = neighbor(current_solution)
        new_energy = objective_function(new_solution)

        if acceptance_probability(current_energy, new_energy, temperature) > random.random():
            current_solution = new_solution
            current_energy = new_energy
            path.append(current_solution.copy())

        if current_energy < best_energy:
            best_solution = current_solution
            best_energy = current_energy
            no_improve_count = 0
        else:
            no_improve_count += 1

        # Salto aleatorio si no hay mejora tras X iteraciones
        if no_improve_count >= max_no_improve:
            current_solution = np.random.uniform(lower_bound, upper_bound)
            current_energy = objective_function(current_solution)
            path.append(current_solution.copy())
            jump_points.append(current_solution.copy())
            no_improve_count = 0
            temperature *= 1.05  # Recalentamiento leve

        temperature *= cooling_rate

    return best_solution, best_energy, path, jump_points

# ---------------------
# Parámetros
# ---------------------

initial_solution = np.random.uniform(lower_bound, upper_bound)
initial_temperature = 1000
cooling_rate = 0.95
max_iterations = 10000

# Ejecutar algoritmo
best_solution, best_energy, path, jump_points = simulated_annealing(
    initial_solution,
    initial_temperature,
    cooling_rate,
    max_iterations
)

# ---------------------
# Visualización
# ---------------------

# Crear malla para el gráfico
x = np.linspace(lower_bound[0], upper_bound[0], 300)
y = np.linspace(lower_bound[1], upper_bound[1], 300)
X, Y = np.meshgrid(x, y)
#Z = peaks(X, Y)
Z = booth(X, Y)

# Convertir trayectoria a arrays
path = np.array(path)
px, py = path[:, 0], path[:, 1]

plt.figure(figsize=(10, 8))
contour = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
plt.colorbar(label='f(x, y)')

# Ruta del algoritmo
plt.plot(px, py, color='white', linestyle='-', linewidth=1, label='Trayectoria')

# Punto inicial
plt.plot(px[0], py[0], 'o', color='red', label='Inicio')

# Mejor solución
plt.plot(best_solution[0], best_solution[1], 'o', color='red', markersize=20, label='Mejor solución')

# Puntos de salto aleatorio
if jump_points:
    jump_points = np.array(jump_points)
    plt.plot(jump_points[:, 0], jump_points[:, 1], 's', color='cyan', markersize=8, label='Saltos aleatorios')

plt.title("Simulated Annealing en la función Peaks (con saltos aleatorios)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.xlim(lower_bound[0], upper_bound[0])
plt.ylim(lower_bound[1], upper_bound[1])
plt.show()

# ---------------------
# Resultado final
# ---------------------
print("\nRESULTADO FINAL:")
print(f"Mejor solución encontrada: x = {best_solution[0]:.5f}, y = {best_solution[1]:.5f}")
print(f"Valor máximo de f(x, y) = { -best_energy:.5f}")
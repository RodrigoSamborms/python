import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parámetros del Algoritmo PSO ---
W = 0.5   # Inercia
C1 = 1.0  # Factor Cognitivo
C2 = 1.5  # Factor Social (reducido un poco para ver más movimiento)
N_PARTICULAS = 15
ITERACIONES = 30
TARGET = 0 # El mínimo de f(x) = x^2

# --- Función de Fitness (lo que queremos minimizar) ---
def funcion_objetivo(x):
    return x**2

class Particula:
    def __init__(self):
        # Posición y velocidad inicial aleatoria amplia para visualizar mejor
        self.posicion = random.uniform(-20, 20)
        self.velocidad = random.uniform(-2, 2)
        self.pbest = self.posicion
        self.fitness_pbest = funcion_objetivo(self.posicion)

    def actualizar_velocidad(self, gbest):
        r1, r2 = random.random(), random.random()
        comp_inercia = W * self.velocidad
        comp_cognitivo = C1 * r1 * (self.pbest - self.posicion)
        comp_social = C2 * r2 * (gbest - self.posicion)
        self.velocidad = comp_inercia + comp_cognitivo + comp_social

    def actualizar_posicion(self):
        self.posicion += self.velocidad
        fitness_actual = funcion_objetivo(self.posicion)
        if fitness_actual < self.fitness_pbest:
            self.fitness_pbest = fitness_actual
            self.pbest = self.posicion

# --- Preparación de la Simulación ---
enjambre = [Particula() for _ in range(N_PARTICULAS)]
gbest = enjambre[0].posicion
# Historial para la animación: [iteracion][particula_id] = posicion
historial_posiciones = []

# --- Preparación de la Gráfica con Matplotlib ---
fig, ax = plt.subplots(figsize=(10, 6))
plt.title("Simulación de Optimización por Enjambre de Partículas (PSO)")
plt.xlabel("Posición (x)")
plt.ylabel("Fitness f(x) = x²")

# Graficar la función objetivo de fondo (la parábola)
x_parabola = np.linspace(-25, 25, 400)
y_parabola = funcion_objetivo(x_parabola)
ax.plot(x_parabola, y_parabola, 'g--', alpha=0.5, label='Función Objetivo f(x)=x²')
ax.axvline(x=0, color='red', linestyle='-', alpha=0.3, label='Objetivo (Mínimo)')

# Elementos que se actualizarán en la animación
particulas_plot, = ax.plot([], [], 'bo', ms=6, label='Partículas')
gbest_plot, = ax.plot([], [], 'r*', ms=12, label='Mejor Global (gbest)')
iteracion_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Configurar límites de la gráfica
ax.set_xlim(-25, 25)
ax.set_ylim(-10, 650) # f(25) = 625
ax.legend(loc='upper right')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# --- Función de Inicialización de la Animación ---
def init():
    particulas_plot.set_data([], [])
    gbest_plot.set_data([], [])
    iteracion_text.set_text('')
    return particulas_plot, gbest_plot, iteracion_text

# --- Función de Actualización por Frame (Iteración) ---
def update(frame):
    global gbest
    
    # Obtener las posiciones actuales para guardar en el historial
    posiciones_actuales = [p.posicion for p in enjambre]
    historial_posiciones.append(posiciones_actuales)

    # Actualizar la lógica de PSO
    for p in enjambre:
        if funcion_objetivo(p.pbest) < funcion_objetivo(gbest):
            gbest = p.pbest
        p.actualizar_velocidad(gbest)
        p.actualizar_posicion()

    # Actualizar los puntos en la gráfica
    x_data = [p.posicion for p in enjambre]
    y_data = [funcion_objetivo(p.posicion) for p in enjambre]
    particulas_plot.set_data(x_data, y_data)
    
    gbest_plot.set_data([gbest], [funcion_objetivo(gbest)])
    
    iteracion_text.set_text(f'Iteración: {frame+1}/{ITERACIONES}\nMejor Global x: {gbest:.4f}')
    
    return particulas_
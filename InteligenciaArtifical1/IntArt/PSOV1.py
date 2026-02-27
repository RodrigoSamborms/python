import random

# Parámetros del algoritmo (Hiperparámetros)
W = 0.5   # Inercia: qué tanto mantiene su dirección previa
C1 = 1.0  # Factor Cognitivo: qué tanto confía en su propia experiencia
C2 = 2.0  # Factor Social: qué tanto confía en el grupo
TARGET = 0 # El valor óptimo que queremos alcanzar

class Particula:
    def __init__(self):
        # Posición y velocidad inicial aleatoria
        self.posicion = random.uniform(-10, 10)
        self.velocidad = random.uniform(-1, 1)
        self.pbest = self.posicion  # Su mejor marca personal inicial
        self.fitness_pbest = self.posicion**2

    def actualizar_velocidad(self, gbest):
        r1, r2 = random.random(), random.random()
        
        # --- AQUÍ ESTÁ LA FÓRMULA QUE VIMOS ---
        componente_inercia = W * self.velocidad
        componente_cognitivo = C1 * r1 * (self.pbest - self.posicion)
        componente_social = C2 * r2 * (gbest - self.posicion)
        
        self.velocidad = componente_inercia + componente_cognitivo + componente_social

    def actualizar_posicion(self):
        self.posicion += self.velocidad
        
        # Evaluar si esta nueva posición es su mejor marca personal
        fitness_actual = self.posicion**2
        if fitness_actual < self.fitness_pbest:
            self.fitness_pbest = fitness_actual
            self.pbest = self.posicion

# 1. Crear un enjambre de 5 partículas
enjambre = [Particula() for _ in range(5)]
gbest = enjambre[0].posicion # Empezamos asumiendo que la primera es la mejor

# 2. Ciclo de optimización (10 iteraciones)
for i in range(10):
    for p in enjambre:
        # Actualizar el mejor global del grupo (gbest)
        if p.fitness_pbest < gbest**2:
            gbest = p.pbest
        
        # Aplicar movimiento
        p.actualizar_velocidad(gbest)
        p.actualizar_posicion()
    
    print(f"Iteración {i+1}: Mejor posición grupal (gbest) = {gbest:.4f}")
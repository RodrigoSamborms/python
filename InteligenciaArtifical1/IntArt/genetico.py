import random

# Definimos la función objetivo que queremos minimizar: f(x) = x^2
def objective_function(x):
    return x ** 2

# Generamos una población inicial
def generate_population(size, lower_bound, upper_bound):
    population = []
    for _ in range(size):
        individual = random.uniform(lower_bound, upper_bound)
        population.append(individual)
    return population

# Evaluamos la población
def evaluate_population(population):
    return [(individual, objective_function(individual)) for individual in population]

# Seleccionamos individuos para reproducirse (torneo)
def tournament_selection(population, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda x: x[1])  # Ordenamos por el valor de la función objetivo
    return tournament[0][0]  # Retornamos el mejor individuo

# Cruzamos dos individuos (cruce de un punto)
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2  # Promedio simple como operador de cruce

# Mutamos un individuo (mutación gaussiana)
def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        individual += random.gauss(0, 1)  # Se agrega un valor aleatorio gaussiano
    return individual

# Algoritmo Genético
def genetic_algorithm(population_size, lower_bound, upper_bound, generations, mutation_rate):
    # Generamos la población inicial
    population = generate_population(population_size, lower_bound, upper_bound)
    
    # Evolucionamos la población a través de generaciones
    for generation in range(generations):
        # Evaluamos la población
        evaluated_population = evaluate_population(population)
        evaluated_population.sort(key=lambda x: x[1])  # Ordenamos por mejor valor de la función objetivo
        
        # Imprimimos la mejor solución de la generación actual (opcional)
        print(f"Generation {generation + 1}: Best solution = {evaluated_population[0][0]}, Best fitness = {evaluated_population[0][1]}")
        
        # Nueva población
        new_population = []
        
        # Selección, Cruce y Mutación para crear la nueva población
        for _ in range(population_size):
            parent1 = tournament_selection(evaluated_population)
            parent2 = tournament_selection(evaluated_population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        # Reemplazamos la población antigua con la nueva
        population = new_population
    
    # Retornamos la mejor solución encontrada
    best_solution = min(evaluate_population(population), key=lambda x: x[1])
    return best_solution

# Parámetros del algoritmo
population_size = 30  # Tamaño de la población
lower_bound = -10  # Límite inferior del rango de búsqueda
upper_bound = 10  # Límite superior del rango de búsqueda
generations = 50  # Número de generaciones
mutation_rate = 0.1  # Tasa de mutación

# Ejecutamos el Algoritmo Genético
best_solution = genetic_algorithm(population_size, lower_bound, upper_bound, generations, mutation_rate)

print("\nResultado final:")
print(f"Mejor solución encontrada: x = {best_solution[0]}")
print(f"Valor mínimo de f(x) = {best_solution[1]}")
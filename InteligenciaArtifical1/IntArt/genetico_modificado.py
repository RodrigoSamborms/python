import math
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


# Generamos un paso de vuelo de Levy usando la distribucion pesada de Mantegna.
# Este paso permite hacer saltos grandes de vez en cuando para explorar mejor el espacio.
def levy_step(beta=1.5):
    numerator = math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
    denominator = math.gamma((1 + beta) / 2) * beta * (2 ** ((beta - 1) / 2))
    sigma_u = (numerator / denominator) ** (1 / beta)

    u = random.gauss(0, sigma_u)
    v = random.gauss(0, 1)
    return u / (abs(v) ** (1 / beta))


# Aplicamos un vuelo de Levy sobre el hijo generado.
# La idea es moverlo respecto al mejor individuo actual para combinar explotacion y exploracion.
def levy_mutation(individual, best_individual, lower_bound, upper_bound, levy_rate=0.2, beta=1.5, step_scale=0.1):
    if random.random() < levy_rate:
        step = levy_step(beta) * step_scale
        individual = individual + step * (individual - best_individual)

    return max(lower_bound, min(upper_bound, individual))

# Algoritmo Genético
def genetic_algorithm(population_size, lower_bound, upper_bound, generations, mutation_rate, levy_rate=0.2, levy_beta=1.5, levy_scale=0.1):
    # Generamos la población inicial
    population = generate_population(population_size, lower_bound, upper_bound)
    
    # Evolucionamos la población a través de generaciones
    for generation in range(generations):
        # Evaluamos la población
        evaluated_population = evaluate_population(population)
        evaluated_population.sort(key=lambda x: x[1])  # Ordenamos por mejor valor de la función objetivo
        # El mejor individuo de la generación se usa como referencia para el vuelo de Levy.
        best_individual = evaluated_population[0][0]
        
        # Imprimimos la mejor solución de la generación actual (opcional)
        print(f"Generation {generation + 1}: Best solution = {best_individual}, Best fitness = {evaluated_population[0][1]}")
        
        # Nueva población
        new_population = []
        
        # Selección, Cruce y Mutación para crear la nueva población
        for _ in range(population_size):
            parent1 = tournament_selection(evaluated_population)
            parent2 = tournament_selection(evaluated_population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            child = levy_mutation(
                child,
                best_individual,
                lower_bound,
                upper_bound,
                levy_rate=levy_rate,
                beta=levy_beta,
                step_scale=levy_scale,
            )
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
# Estos parametros controlan la mejora con Levy:
# levy_rate: frecuencia de los saltos, levy_beta: forma de la distribucion,
# levy_scale: intensidad del desplazamiento.
levy_rate = 0.2
levy_beta = 1.5
levy_scale = 0.1

# Ejecutamos el Algoritmo Genético
best_solution = genetic_algorithm(
    population_size,
    lower_bound,
    upper_bound,
    generations,
    mutation_rate,
    levy_rate=levy_rate,
    levy_beta=levy_beta,
    levy_scale=levy_scale,
)

print("\nResultado final:")
print(f"Mejor solución encontrada: x = {best_solution[0]}")
print(f"Valor mínimo de f(x) = {best_solution[1]}")
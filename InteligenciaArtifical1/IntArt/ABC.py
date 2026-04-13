import numpy as np

class ArtificialBeeColony:
    def __init__(self, fitness_function, lower_bounds, upper_bounds, num_bees=30, max_iter=100):
        self.fitness_function = fitness_function
        self.lower_bounds = np.array(lower_bounds)
        self.upper_bounds = np.array(upper_bounds)
        self.num_bees = num_bees
        self.max_iter = max_iter
        self.num_params = len(lower_bounds)
        self.population = np.random.uniform(self.lower_bounds, self.upper_bounds, (self.num_bees, self.num_params))
        self.fitness = np.apply_along_axis(self.fitness_function, 1, self.population)
        self.best_bee = self.population[np.argmin(self.fitness)]

    def optimize(self):
        for iteration in range(self.max_iter):
            for i in range(self.num_bees):
                k = np.random.randint(0, self.num_params)
                phi = np.random.uniform(-1, 1)
                new_solution = np.copy(self.population[i])
                new_solution[k] = self.population[i, k] + phi * (self.population[i, k] - self.best_bee[k])
                new_solution = np.clip(new_solution, self.lower_bounds, self.upper_bounds)
                new_fitness = -self.fitness_function(new_solution)

                if new_fitness < self.fitness[i]:
                    self.population[i] = new_solution
                    self.fitness[i] = new_fitness

                if new_fitness < np.min(self.fitness):
                    self.best_bee = new_solution

            print(f"Iteration {iteration + 1}, Best Fitness: {np.min(self.fitness)}")

        return self.best_bee

# Definición de la función peaks
def peaks(x):
    x1, x2 = x
    return -(3 * (1 - x1) ** 2 * np.exp(-x1 ** 2 - (x2 + 1) ** 2) - 10 * (x1 / 5 - x1 ** 3 - x2 ** 5) * np.exp(-x1 ** 2 - x2 ** 2) - 1 / 3 * np.exp(-(x1 + 1) ** 2 - x2 ** 2))

lower_bounds = [-3, -3]
upper_bounds = [3, 3]

abc = ArtificialBeeColony(peaks, lower_bounds, upper_bounds)
best_solution = abc.optimize()
print("Best solution found:", best_solution)
import argparse
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def psnr(reference: np.ndarray, target: np.ndarray) -> float:
    ref = reference.astype(np.float32)
    tgt = target.astype(np.float32)
    mse = np.mean((ref - tgt) ** 2)
    if mse == 0:
        return float("inf")
    return 20 * np.log10(255.0) - 10 * np.log10(mse)


def apply_gaussian_smoothing(image: Image.Image, sigma: float) -> Image.Image:
    return image.filter(ImageFilter.GaussianBlur(radius=sigma))


def generate_population(size: int, lower_bound: float, upper_bound: float) -> list[float]:
    return [random.uniform(lower_bound, upper_bound) for _ in range(size)]


def evaluate_population(
    population: list[float],
    noisy_image: Image.Image,
    reference_array: np.ndarray,
) -> list[tuple[float, float]]:
    evaluated = []
    for sigma in population:
        smoothed = apply_gaussian_smoothing(noisy_image, sigma)
        smoothed_array = np.array(smoothed)
        fitness = psnr(reference_array, smoothed_array)
        evaluated.append((sigma, fitness))
    return evaluated


def tournament_selection(
    evaluated_population: list[tuple[float, float]],
    tournament_size: int = 3,
) -> float:
    tournament = random.sample(evaluated_population, tournament_size)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return tournament[0][0]


def crossover(parent1: float, parent2: float) -> float:
    return (parent1 + parent2) / 2


def mutate(
    individual: float,
    lower_bound: float,
    upper_bound: float,
    mutation_rate: float = 0.1,
) -> float:
    if random.random() < mutation_rate:
        individual += random.gauss(0, 0.2)
    return max(lower_bound, min(upper_bound, individual))


def genetic_algorithm(
    population_size: int,
    lower_bound: float,
    upper_bound: float,
    generations: int,
    mutation_rate: float,
    noisy_image: Image.Image,
    reference_array: np.ndarray,
) -> tuple[float, float]:
    population = generate_population(population_size, lower_bound, upper_bound)

    for generation in range(generations):
        evaluated_population = evaluate_population(
            population, noisy_image, reference_array
        )
        evaluated_population.sort(key=lambda x: x[1], reverse=True)

        print(
            "Generation "
            f"{generation + 1}: Best sigma = {evaluated_population[0][0]:.4f}, "
            f"Best PSNR = {evaluated_population[0][1]:.4f} dB"
        )

        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(evaluated_population)
            parent2 = tournament_selection(evaluated_population)
            child = crossover(parent1, parent2)
            child = mutate(child, lower_bound, upper_bound, mutation_rate)
            new_population.append(child)

        population = new_population

    evaluated_population = evaluate_population(
        population, noisy_image, reference_array
    )
    return max(evaluated_population, key=lambda x: x[1])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Optimiza el sigma del filtro gaussiano usando PSNR y "
            "guarda la imagen suavizada."
        )
    )
    parser.add_argument(
        "--input-original",
        default="Diana.bmp",
        help="Ruta de la imagen original (por defecto Diana.bmp).",
    )
    parser.add_argument(
        "--input-noisy",
        default="Diana_Ruido.bmp",
        help="Ruta de la imagen con ruido (por defecto Diana_Ruido.bmp).",
    )
    parser.add_argument(
        "--output",
        default="Diana_Suavisado.bmp",
        help="Ruta de salida (por defecto Diana_Suavisado.bmp).",
    )
    parser.add_argument(
        "--pop-size",
        type=int,
        default=30,
        help="Tamano de poblacion (por defecto 30).",
    )
    parser.add_argument(
        "--sigma-min",
        type=float,
        default=0.5,
        help="Sigma minimo (por defecto 0.5).",
    )
    parser.add_argument(
        "--sigma-max",
        type=float,
        default=5.0,
        help="Sigma maximo (por defecto 5.0).",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=40,
        help="Numero de generaciones (por defecto 40).",
    )
    parser.add_argument(
        "--mutation-rate",
        type=float,
        default=0.1,
        help="Tasa de mutacion (por defecto 0.1).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Semilla opcional para reproducibilidad.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_original = Path(args.input_original)
    input_noisy = Path(args.input_noisy)
    output_smoothed = Path(args.output)

    if not input_original.exists():
        raise FileNotFoundError(f"No se encontro la imagen: {input_original}")
    if not input_noisy.exists():
        raise FileNotFoundError(f"No se encontro la imagen: {input_noisy}")

    original_image = Image.open(input_original)
    noisy_image = Image.open(input_noisy)

    reference_array = np.array(original_image)

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    population_size = args.pop_size
    lower_bound = args.sigma_min
    upper_bound = args.sigma_max
    generations = args.generations
    mutation_rate = args.mutation_rate

    best_sigma, best_psnr = genetic_algorithm(
        population_size,
        lower_bound,
        upper_bound,
        generations,
        mutation_rate,
        noisy_image,
        reference_array,
    )

    best_smoothed = apply_gaussian_smoothing(noisy_image, best_sigma)
    best_smoothed.save(output_smoothed)

    print("\nResultado final:")
    print(f"Mejor sigma encontrado: {best_sigma:.4f}")
    print(f"PSNR maximo: {best_psnr:.4f} dB")
    print(f"Imagen suavizada guardada en: {output_smoothed}")


if __name__ == "__main__":
    main()
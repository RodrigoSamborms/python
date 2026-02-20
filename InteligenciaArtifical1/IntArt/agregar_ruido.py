import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def add_gaussian_noise(image_array: np.ndarray, sigma: float, rng: np.random.Generator) -> np.ndarray:
    noise = rng.normal(0.0, sigma, size=image_array.shape)
    noisy = image_array.astype(np.float32) + noise
    noisy = np.clip(noisy, 0, 255)
    return noisy.astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Agregar ruido a una imagen BMP.")
    parser.add_argument(
        "--input",
        default="Diana.bmp",
        help="Ruta de la imagen de entrada (por defecto Diana.bmp).",
    )
    parser.add_argument(
        "--output",
        default="Diana_Ruido.bmp",
        help="Ruta de salida (por defecto Diana_Ruido.bmp).",
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=25.0,
        help="Desviacion estandar del ruido gaussiano (por defecto 25).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Semilla opcional para reproducibilidad.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"No se encontro la imagen: {input_path}")

    image = Image.open(input_path)
    image_array = np.array(image)

    rng = np.random.default_rng(args.seed)
    noisy_array = add_gaussian_noise(image_array, args.sigma, rng)

    noisy_image = Image.fromarray(noisy_array)
    noisy_image.save(output_path)

    print(f"Imagen con ruido guardada en: {output_path}")


if __name__ == "__main__":
    main()

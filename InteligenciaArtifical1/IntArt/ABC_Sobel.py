"""Deteccion de bordes con Sobel.

Este script toma una imagen de entrada, la convierte a escala de grises y
aplica los operadores Sobel horizontal y vertical para calcular la magnitud
del gradiente. El resultado se guarda como una imagen en escala de grises.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


KERNEL_X = np.array(
    [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
    dtype=np.float32,
)

KERNEL_Y = np.array(
    [[1, 2, 1], [0, 0, 0], [-1, -2, -1]],
    dtype=np.float32,
)


def cargar_imagen_gris(ruta: str | Path) -> np.ndarray:
    """Carga una imagen y la devuelve como arreglo uint8 en escala de grises."""
    imagen = Image.open(ruta).convert("L")
    return np.array(imagen, dtype=np.uint8)


def convolucion2d(imagen: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Aplica una convolucion 2D con relleno de borde replicado."""
    alto, ancho = imagen.shape
    kernel_alto, kernel_ancho = kernel.shape
    pad_y = kernel_alto // 2
    pad_x = kernel_ancho // 2

    extendida = np.pad(imagen.astype(np.float32), ((pad_y, pad_y), (pad_x, pad_x)), mode="edge")
    salida = np.zeros((alto, ancho), dtype=np.float32)

    for y in range(alto):
        for x in range(ancho):
            ventana = extendida[y : y + kernel_alto, x : x + kernel_ancho]
            salida[y, x] = float(np.sum(ventana * kernel))

    return salida


def detectar_bordes_sobel(imagen_gris: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Devuelve gradiente horizontal, vertical y magnitud normalizada."""
    grad_x = convolucion2d(imagen_gris, KERNEL_X)
    grad_y = convolucion2d(imagen_gris, KERNEL_Y)
    magnitud = np.hypot(grad_x, grad_y)

    maximo = float(np.max(magnitud))
    if maximo > 0:
        magnitud = (magnitud / maximo) * 255.0

    return grad_x, grad_y, magnitud.astype(np.uint8)


def guardar_imagen(ruta: str | Path, imagen: np.ndarray) -> None:
    """Guarda una matriz de pixeles como imagen en escala de grises."""
    Image.fromarray(imagen, mode="L").save(ruta)


def construir_ruta_salida_automatica(ruta_entrada: str | Path) -> str:
    """Construye una ruta de salida con sufijo _Sobel antes de la extension."""
    ruta = Path(ruta_entrada)
    extension = ruta.suffix if ruta.suffix else ".png"
    nombre_salida = f"{ruta.stem}_Sobel{extension}"
    return str(ruta.with_name(nombre_salida))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detecta bordes en una imagen usando el operador Sobel."
    )
    parser.add_argument(
        "entrada",
        nargs="?",
        default="test_input.png",
        help="Ruta de la imagen de entrada (por defecto test_input.png).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Ruta de salida. Si no se define, se genera automaticamente.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    ruta_entrada = Path(args.entrada)
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No se encontro la imagen de entrada: {ruta_entrada}")

    ruta_salida = Path(args.output) if args.output else Path(construir_ruta_salida_automatica(ruta_entrada))

    imagen_gris = cargar_imagen_gris(ruta_entrada)
    grad_x, grad_y, bordes = detectar_bordes_sobel(imagen_gris)

    guardar_imagen(ruta_salida, bordes)

    print("Procesamiento Sobel completado")
    print(f"Entrada: {ruta_entrada}")
    print(f"Salida: {ruta_salida}")
    print(f"Gradiente X -> min: {grad_x.min():.2f}, max: {grad_x.max():.2f}")
    print(f"Gradiente Y -> min: {grad_y.min():.2f}, max: {grad_y.max():.2f}")
    print(f"Bordes -> min: {bordes.min()}, max: {bordes.max()}")


if __name__ == "__main__":
    main()
"""
Implementación simple del Algoritmo del Gradiente Descendente en 3 dimensiones.
"""

import matplotlib.pyplot as plt
import numpy as np


def funcion_objetivo(x, y, z):
    return (x - 3) ** 2 + (y + 2) ** 2 + (z - 1) ** 2


def gradiente(x, y, z):
    return 2 * (x - 3), 2 * (y + 2), 2 * (z - 1)


def gradiente_descendente_3d(punto_inicial, tasa_aprendizaje=0.1, iteraciones=100):
    """
    Gradiente descendente para f(x, y, z) = (x-3)^2 + (y+2)^2 + (z-1)^2.

    Args:
        punto_inicial: Tupla (x, y, z)
        tasa_aprendizaje: Tamaño de paso
        iteraciones: Número de iteraciones

    Returns:
        punto_final: Tupla (x, y, z)
        historial: Lista de tuplas con los puntos visitados
        historial_f: Lista con los valores de f en cada iteración
    """
    x, y, z = punto_inicial
    historial = [(x, y, z)]
    historial_f = [funcion_objetivo(x, y, z)]

    for i in range(iteraciones):
        gx, gy, gz = gradiente(x, y, z)

        x = x - tasa_aprendizaje * gx
        y = y - tasa_aprendizaje * gy
        z = z - tasa_aprendizaje * gz

        historial.append((x, y, z))
        historial_f.append(funcion_objetivo(x, y, z))

        if (i + 1) % 20 == 0:
            print(
                f"Iteración {i+1}: "
                f"x={x:.6f}, y={y:.6f}, z={z:.6f}, f={historial_f[-1]:.6f}"
            )

    return (x, y, z), historial, historial_f


def visualizar_3d(historial):
    puntos = np.array(historial)
    xs = puntos[:, 0]
    ys = puntos[:, 1]

    x_superficie = np.linspace(xs.min() - 1, xs.max() + 1, 60)
    y_superficie = np.linspace(ys.min() - 1, ys.max() + 1, 60)
    X, Y = np.meshgrid(x_superficie, y_superficie)
    Z = (X - 3) ** 2 + (Y + 2) ** 2

    z_camino = np.array([funcion_objetivo(x, y, z) for x, y, z in historial])

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, linewidth=0)
    ax.plot(xs, ys, z_camino, 'r.-', label='Trayectoria del gradiente')

    ax.scatter(xs[0], ys[0], z_camino[0], color='blue', s=60, label='Inicio')
    ax.scatter(xs[-1], ys[-1], z_camino[-1], color='red', s=80, label='Final')

    ax.set_title('Gradiente Descendente en 3D')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y, z)')
    ax.legend()
    plt.show()


if __name__ == "__main__":
    print("=" * 60)
    print("GRADIENTE DESCENDENTE EN 3 DIMENSIONES")
    print("=" * 60)
    print("Función: f(x, y, z) = (x-3)^2 + (y+2)^2 + (z-1)^2")
    print("Mínimo real en: (3, -2, 1)\n")

    punto_inicial = (0, 0, 0)
    tasa_aprendizaje = 0.1
    iteraciones = 100

    print("Parámetros:")
    print(f"  punto_inicial = {punto_inicial}")
    print(f"  tasa_aprendizaje = {tasa_aprendizaje}")
    print(f"  iteraciones = {iteraciones}\n")

    punto_final, historial, historial_f = gradiente_descendente_3d(
        punto_inicial,
        tasa_aprendizaje=tasa_aprendizaje,
        iteraciones=iteraciones,
    )

    x_final, y_final, z_final = punto_final

    print(f"\n{'=' * 60}")
    print("Resultado Final:")
    print(f"  punto_final = ({x_final:.6f}, {y_final:.6f}, {z_final:.6f})")
    print(f"  f(punto_final) = {funcion_objetivo(x_final, y_final, z_final):.6f}")
    print(
        "  Error absoluto = "
        f"({abs(x_final - 3):.6f}, {abs(y_final + 2):.6f}, {abs(z_final - 1):.6f})"
    )
    print(f"{'=' * 60}\n")

    print("Generando gráfica 3D de la función...")
    visualizar_3d(historial)

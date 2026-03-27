"""
Busqueda Armonica V3: visualizacion 3D de la funcion objetivo y trayectoria.

Esta version conserva el algoritmo Harmony Search (HS) y agrega una
representacion tridimensional de:
1) Superficie de la funcion objetivo z = f(x1, x2)
2) Puntos candidatos evaluados en cada iteracion
3) Trayectoria del mejor punto historico
4) Mejor punto final y (opcional) minimo conocido

Se recomienda usar funciones de 2 variables para que la grafica 3D sea
interpretable. En este archivo se incluye Himmelblau como funcion de ejemplo,
porque presenta un paisaje con varios minimos y se visualiza mejor que Sphere.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple
import random

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (habilita proyeccion 3D)


ObjectiveFunction = Callable[[Sequence[float]], float]


@dataclass
class Harmony:
    """Representa una solucion candidata y su fitness interno de optimizacion."""

    values: List[float]
    fitness: float


class BusquedaArmonicaV3:
    """
    Implementacion de Harmony Search con trazabilidad para visualizacion 3D.

    Parametros clave del algoritmo:
    - HMS (harmony_memory_size): tamano de memoria armonica.
    - HMCR (harmony_memory_consideration_rate): probabilidad de usar memoria.
    - PAR (pitch_adjustment_rate): probabilidad de ajuste local de tono.
    - RR (randomize_rate): probabilidad de improvisacion totalmente aleatoria.
    - bandwidth: amplitud relativa del ajuste local.
    """

    def __init__(
        self,
        objective_function: ObjectiveFunction,
        bounds: Sequence[Tuple[float, float]],
        harmony_memory_size: int = 30,
        harmony_memory_consideration_rate: float = 0.90,
        pitch_adjustment_rate: float = 0.35,
        bandwidth: float = 0.02,
        randomize_rate: float = 0.08,
        maximize: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        self.objective_function = objective_function
        self.bounds = list(bounds)
        self.dimension = len(self.bounds)

        self.harmony_memory_size = harmony_memory_size
        self.hmcr = harmony_memory_consideration_rate
        self.par = pitch_adjustment_rate
        self.bandwidth = bandwidth
        self.randomize_rate = randomize_rate
        self.maximize = maximize

        self.rng = random.Random(seed)

        self.harmony_memory: List[Harmony] = []

        # Registros para analisis/visualizacion en problemas 2D:
        # (x1, x2, f_original, aceptado_en_hm)
        self.search_points_2d: List[Tuple[float, float, float, bool]] = []
        self.best_points_2d_history: List[Tuple[float, float, float]] = []
        self.best_fitness_history: List[float] = []

        self._validar_parametros()

    def _validar_parametros(self) -> None:
        """Verifica consistencia de parametros y dominios."""
        if self.dimension == 0:
            raise ValueError("'bounds' no puede estar vacio.")

        for i, (low, high) in enumerate(self.bounds):
            if low >= high:
                raise ValueError(f"Limites invalidos en dimension {i}: ({low}, {high}).")

        if self.harmony_memory_size < 2:
            raise ValueError("'harmony_memory_size' debe ser >= 2.")
        if not 0.0 <= self.hmcr <= 1.0:
            raise ValueError("'harmony_memory_consideration_rate' debe estar en [0, 1].")
        if not 0.0 <= self.par <= 1.0:
            raise ValueError("'pitch_adjustment_rate' debe estar en [0, 1].")
        if self.bandwidth < 0.0:
            raise ValueError("'bandwidth' no puede ser negativo.")
        if not 0.0 <= self.randomize_rate <= 1.0:
            raise ValueError("'randomize_rate' debe estar en [0, 1].")

    def _evaluar(self, values: Sequence[float]) -> float:
        """
        Evalua fitness interno.

        Para maximizacion se transforma a minimizacion mediante signo negativo.
        """
        score = self.objective_function(values)
        return -score if self.maximize else score

    def _objective_original(self, values: Sequence[float]) -> float:
        """Evalua funcion objetivo en escala original, sin transformacion."""
        return self.objective_function(values)

    @staticmethod
    def _clip(value: float, low: float, high: float) -> float:
        """Recorta un valor dentro de [low, high]."""
        return min(max(value, low), high)

    def _crear_armonia_aleatoria(self) -> Harmony:
        """Genera una armonia completamente aleatoria dentro de los limites."""
        values = [self.rng.uniform(low, high) for low, high in self.bounds]
        return Harmony(values=values, fitness=self._evaluar(values))

    def _inicializar_harmony_memory(self) -> None:
        """Inicializa HM con armonias aleatorias y las ordena por fitness."""
        self.harmony_memory = [
            self._crear_armonia_aleatoria() for _ in range(self.harmony_memory_size)
        ]
        self.harmony_memory.sort(key=lambda h: h.fitness)

    def _seleccionar_valor_desde_memoria(self, idx_dimension: int) -> float:
        """Harmony Memory Consideration para una dimension."""
        return self.rng.choice(self.harmony_memory).values[idx_dimension]

    def _ajustar_pitch(self, value: float, idx_dimension: int) -> float:
        """
        Pitch adjustment local alrededor de valor proveniente de HM.

        delta ~ U(-bandwidth * rango, +bandwidth * rango)
        """
        low, high = self.bounds[idx_dimension]
        value_range = high - low
        delta = self.rng.uniform(-self.bandwidth * value_range, self.bandwidth * value_range)
        return self._clip(value + delta, low, high)

    def _improvisar_nueva_armonia(self) -> Harmony:
        """
        Improvisa nueva armonia combinando exploracion y explotacion.

        Reglas:
        - Con probabilidad RR: armonia totalmente aleatoria.
        - Si no, por dimension:
          1) Con HMCR, tomar valor de memoria.
          2) Si se tomo de memoria, con PAR ajustar pitch.
          3) Con (1 - HMCR), tomar valor aleatorio del dominio.
        """
        if self.rng.random() < self.randomize_rate:
            return self._crear_armonia_aleatoria()

        values: List[float] = []
        for i, (low, high) in enumerate(self.bounds):
            if self.rng.random() < self.hmcr:
                value = self._seleccionar_valor_desde_memoria(i)
                if self.rng.random() < self.par:
                    value = self._ajustar_pitch(value, i)
            else:
                value = self.rng.uniform(low, high)

            values.append(self._clip(value, low, high))

        return Harmony(values=values, fitness=self._evaluar(values))

    def _actualizar_harmony_memory(self, candidate: Harmony) -> bool:
        """Reemplaza peor armonia si el candidato mejora (Harmony Memory Update)."""
        worst = self.harmony_memory[-1]
        if candidate.fitness < worst.fitness:
            self.harmony_memory[-1] = candidate
            self.harmony_memory.sort(key=lambda h: h.fitness)
            return True
        return False

    def optimizar(self, iterations: int = 500, verbose: bool = False) -> Tuple[List[float], float]:
        """Ejecuta la busqueda y registra trayectoria de optimizacion."""
        if iterations <= 0:
            raise ValueError("'iterations' debe ser mayor que 0.")

        self.search_points_2d.clear()
        self.best_points_2d_history.clear()
        self.best_fitness_history.clear()

        self._inicializar_harmony_memory()
        report_step = max(1, iterations // 10)

        for it in range(1, iterations + 1):
            candidate = self._improvisar_nueva_armonia()
            accepted = self._actualizar_harmony_memory(candidate)

            if self.dimension == 2:
                x1, x2 = candidate.values
                z = self._objective_original(candidate.values)
                self.search_points_2d.append((x1, x2, z, accepted))

            best = self.harmony_memory[0]
            best_original = self._objective_original(best.values)
            self.best_fitness_history.append(best_original)

            if self.dimension == 2:
                bx, by = best.values
                self.best_points_2d_history.append((bx, by, best_original))

            if verbose and (it == 1 or it == iterations or it % report_step == 0):
                print(f"Iteracion {it:5d} | Mejor valor objetivo: {best_original:.10f}")

        best = self.harmony_memory[0]
        return best.values, self._objective_original(best.values)


def funcion_himmelblau(x: Sequence[float]) -> float:
    """
    Funcion de Himmelblau (2D): superficie no convexa con varios minimos.

    f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2

    Algunos minimos globales (valor ~ 0):
    - ( 3.000000,  2.000000)
    - (-2.805118,  3.131312)
    - (-3.779310, -3.283186)
    - ( 3.584428, -1.848126)
    """
    x1, x2 = x
    return (x1 * x1 + x2 - 11.0) ** 2 + (x1 + x2 * x2 - 7.0) ** 2


def graficar_superficie_3d_y_puntos(
    optimizer: BusquedaArmonicaV3,
    title: str = "Busqueda Armonica V3 - Superficie 3D",
    save_path: str = "InteligenciaArtifical1/IntArt/busqueda_armonica_v3_3d.png",
    known_optimum: Optional[Tuple[float, float]] = None,
    grid_points: int = 180,
) -> None:
    """
    Genera grafica 3D de la funcion objetivo y superpone trayectoria de busqueda.

    Elementos del grafico:
    - Superficie z=f(x1,x2)
    - Puntos candidatos por iteracion (color temporal)
    - Curva del mejor historico
    - Mejor punto final
    - Optimo conocido (si se proporciona)
    """
    if optimizer.dimension != 2:
        raise ValueError("La grafica 3D requiere un problema de 2 dimensiones.")

    if not optimizer.search_points_2d:
        raise ValueError("No hay puntos registrados. Ejecuta optimizar() primero.")

    (x_min, x_max), (y_min, y_max) = optimizer.bounds

    x = np.linspace(x_min, x_max, grid_points)
    y = np.linspace(y_min, y_max, grid_points)
    X, Y = np.meshgrid(x, y)

    # Calculo de la superficie objetivo sobre malla regular.
    Z = np.zeros_like(X, dtype=float)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = optimizer.objective_function([float(X[i, j]), float(Y[i, j])])

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")

    # Superficie semitransparente para no ocultar los puntos de busqueda.
    surface = ax.plot_surface(
        X,
        Y,
        Z,
        cmap="viridis",
        linewidth=0,
        antialiased=True,
        alpha=0.68,
    )
    cbar = fig.colorbar(surface, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label("Valor de la funcion objetivo")

    # Puntos candidatos evaluados en cada iteracion.
    xs = np.array([p[0] for p in optimizer.search_points_2d], dtype=float)
    ys = np.array([p[1] for p in optimizer.search_points_2d], dtype=float)
    zs = np.array([p[2] for p in optimizer.search_points_2d], dtype=float)
    t = np.arange(len(xs), dtype=float)

    points = ax.scatter(
        xs,
        ys,
        zs,
        c=t,
        cmap="plasma",
        s=18,
        alpha=0.88,
        depthshade=True,
        label="Puntos de busqueda",
    )
    cbar_points = fig.colorbar(points, ax=ax, shrink=0.6, pad=0.02)
    cbar_points.set_label("Iteracion")

    # Trayectoria del mejor punto historico.
    bxs = [p[0] for p in optimizer.best_points_2d_history]
    bys = [p[1] for p in optimizer.best_points_2d_history]
    bzs = [p[2] for p in optimizer.best_points_2d_history]
    ax.plot(
        bxs,
        bys,
        bzs,
        color="white",
        linewidth=2.2,
        alpha=0.95,
        label="Trayectoria del mejor",
    )

    # Mejor punto final.
    best_values = optimizer.harmony_memory[0].values
    best_z = optimizer._objective_original(best_values)
    ax.scatter(
        [best_values[0]],
        [best_values[1]],
        [best_z],
        color="red",
        marker="*",
        s=260,
        depthshade=False,
        label="Mejor punto final",
    )

    # Punto de optimo conocido.
    if known_optimum is not None:
        kx, ky = known_optimum
        kz = optimizer.objective_function([kx, ky])
        ax.scatter(
            [kx],
            [ky],
            [kz],
            color="cyan",
            marker="X",
            s=180,
            depthshade=False,
            label="Optimo conocido",
        )

    ax.set_title(title)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("f(x1, x2)")

    # Angulo de observacion para facilitar lectura del relieve.
    ax.view_init(elev=33, azim=-58)

    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(save_path, dpi=230)
    plt.close(fig)


def imprimir_resumen(optimizer: BusquedaArmonicaV3, optimum_value: Optional[float] = None) -> None:
    """Imprime indicadores basicos de convergencia al terminar la corrida."""
    if not optimizer.best_fitness_history:
        print("No hay historial disponible.")
        return

    final_best = optimizer.best_fitness_history[-1]
    print("\nResumen de convergencia:")
    print(f"Mejor valor final: {final_best:.12f}")

    if optimum_value is not None:
        error = abs(final_best - optimum_value)
        print(f"Error absoluto frente al optimo teorico: {error:.12f}")

    # Metrica simple: fraccion de iteraciones con mejora respecto al inicio.
    initial = optimizer.best_fitness_history[0]
    improved_count = sum(1 for v in optimizer.best_fitness_history if v < initial)
    print(f"Iteraciones con mejora frente al inicio: {improved_count} de {len(optimizer.best_fitness_history)}")


if __name__ == "__main__":
    # Dominio sugerido para Himmelblau.
    bounds = [(-6.0, 6.0), (-6.0, 6.0)]

    hs = BusquedaArmonicaV3(
        objective_function=funcion_himmelblau,
        bounds=bounds,
        harmony_memory_size=35,
        harmony_memory_consideration_rate=0.92,
        pitch_adjustment_rate=0.35,
        bandwidth=0.03,
        randomize_rate=0.08,
        maximize=False,
        seed=42,
    )

    best_x, best_f = hs.optimizar(iterations=500, verbose=True)

    print("\nResultado final:")
    print(f"Mejor solucion: {best_x}")
    print(f"Mejor valor objetivo: {best_f:.12f}")

    # Para Himmelblau, el valor del minimo global es aproximadamente 0.
    imprimir_resumen(hs, optimum_value=0.0)

    # Se muestra uno de los minimos globales conocidos para referencia visual.
    graph_path = "InteligenciaArtifical1/IntArt/busqueda_armonica_v3_3d.png"
    graficar_superficie_3d_y_puntos(
        optimizer=hs,
        title="Harmony Search V3 sobre Himmelblau (3D)",
        save_path=graph_path,
        known_optimum=(3.0, 2.0),
        grid_points=180,
    )

    print(f"Grafico 3D guardado en: {graph_path}")

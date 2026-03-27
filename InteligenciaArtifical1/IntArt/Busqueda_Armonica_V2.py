"""
Implementacion academica de Harmony Search (Busqueda Armonica) - Version V2.

Objetivo de esta version:
1) Mantener una implementacion clara y comentada del algoritmo.
2) Registrar los puntos explorados durante la busqueda.
3) Graficar la funcion objetivo (en 2D) y superponer los puntos generados
   para observar la aproximacion progresiva al optimo.

Notas metodologicas:
- Esta implementacion esta orientada a minimizacion por defecto.
- Tambien soporta maximizacion mediante transformacion del fitness interno.
- Para la visualizacion de superficie/contornos se requiere un problema de
  dimension 2 (dos variables de decision).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple
import random

import matplotlib.pyplot as plt
import numpy as np


ObjectiveFunction = Callable[[Sequence[float]], float]


@dataclass
class Harmony:
    """Representa una armonia (solucion candidata) y su valor de fitness."""

    values: List[float]
    fitness: float


class BusquedaArmonicaV2:
    """
    Implementacion de Harmony Search con registro de trayectoria.

    Parametros principales:
    - harmony_memory_size (HMS): tamano de la memoria armonica.
    - harmony_memory_consideration_rate (HMCR): probabilidad de reutilizar
      componentes de soluciones previas.
    - pitch_adjustment_rate (PAR): probabilidad de ajustar localmente el valor
      reutilizado desde la memoria.
    - randomize_rate (RR): probabilidad de generar una armonia completamente
      aleatoria para reforzar exploracion global.
    - bandwidth: magnitud de perturbacion local del pitch adjustment.
    """

    def __init__(
        self,
        objective_function: ObjectiveFunction,
        bounds: Sequence[Tuple[float, float]],
        harmony_memory_size: int = 20,
        harmony_memory_consideration_rate: float = 0.90,
        pitch_adjustment_rate: float = 0.30,
        bandwidth: float = 0.05,
        randomize_rate: float = 0.05,
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

        # Estructuras internas del algoritmo.
        self.harmony_memory: List[Harmony] = []

        # Registro completo de los puntos evaluados (candidatos improvisados).
        # Cada entrada: (x, y, valor_objetivo_original, aceptado_en_memoria)
        # Solo se completa para dimension 2, donde x e y tienen interpretacion
        # grafica directa.
        self.search_points_2d: List[Tuple[float, float, float, bool]] = []

        # Historial del mejor valor por iteracion en escala original.
        self.best_fitness_history: List[float] = []

        # Historial del mejor punto (solo para dimension 2).
        self.best_points_2d_history: List[Tuple[float, float]] = []

        self._validar_parametros()

    def _validar_parametros(self) -> None:
        """Valida consistencia de entrada para prevenir configuraciones invalidas."""
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
        Evalua el fitness interno del algoritmo.

        Convencion interna:
        - Minimizar f(x)               si maximize = False.
        - Minimizar -f(x)              si maximize = True.
        """
        score = self.objective_function(values)
        return -score if self.maximize else score

    def _objective_original(self, values: Sequence[float]) -> float:
        """Evalua la funcion objetivo en su escala original (sin transformacion)."""
        return self.objective_function(values)

    @staticmethod
    def _clip(value: float, low: float, high: float) -> float:
        """Satura un valor al intervalo permitido [low, high]."""
        return min(max(value, low), high)

    def _crear_armonia_aleatoria(self) -> Harmony:
        """Genera una nueva armonia completamente aleatoria dentro de los limites."""
        values = [self.rng.uniform(low, high) for low, high in self.bounds]
        return Harmony(values=values, fitness=self._evaluar(values))

    def _inicializar_harmony_memory(self) -> None:
        """Crea la memoria armonica inicial (HM) con soluciones aleatorias."""
        self.harmony_memory = [
            self._crear_armonia_aleatoria() for _ in range(self.harmony_memory_size)
        ]
        self.harmony_memory.sort(key=lambda h: h.fitness)

    def _seleccionar_valor_desde_memoria(self, idx_dimension: int) -> float:
        """
        Implementa Harmony Memory Consideration (HMC) para una dimension.

        Selecciona una armonia al azar de la HM y toma su valor en la dimension
        solicitada.
        """
        harmony = self.rng.choice(self.harmony_memory)
        return harmony.values[idx_dimension]

    def _ajustar_pitch(self, value: float, idx_dimension: int) -> float:
        """
        Implementa Pitch Adjustment sobre un valor proveniente de la HM.

        Ajuste:
            x' = x + delta,
        con delta uniforme en el intervalo:
            [-bandwidth * rango_dimension, +bandwidth * rango_dimension]
        """
        low, high = self.bounds[idx_dimension]
        value_range = high - low
        delta = self.rng.uniform(-self.bandwidth * value_range, self.bandwidth * value_range)
        return self._clip(value + delta, low, high)

    def _improvisar_nueva_armonia(self) -> Harmony:
        """
        Improvisa una nueva armonia segun las reglas de HS.

        Regla principal de exploracion global:
        - Con probabilidad randomize_rate, se genera una armonia completamente
          aleatoria.

        Si no se activa randomize_rate:
        - Por cada dimension se decide entre:
          a) usar HMCR para tomar un valor desde HM,
          b) o generar un valor aleatorio dentro del dominio.
        - Si se tomo desde HM, PAR controla si se hace pitch adjustment.
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
        """
        Implementa Harmony Memory Update.

        Si el candidato mejora al peor elemento de HM, se reemplaza y se
        reordena la memoria.
        """
        worst = self.harmony_memory[-1]
        if candidate.fitness < worst.fitness:
            self.harmony_memory[-1] = candidate
            self.harmony_memory.sort(key=lambda h: h.fitness)
            return True
        return False

    def optimizar(self, iterations: int = 1000, verbose: bool = False) -> Tuple[List[float], float]:
        """
        Ejecuta Harmony Search y registra trayectoria para analisis.

        Retorna:
        - mejor vector encontrado,
        - mejor valor objetivo en escala original.
        """
        if iterations <= 0:
            raise ValueError("'iterations' debe ser mayor que 0.")

        self.search_points_2d.clear()
        self.best_fitness_history.clear()
        self.best_points_2d_history.clear()

        self._inicializar_harmony_memory()
        report_step = max(1, iterations // 10)

        for it in range(1, iterations + 1):
            candidate = self._improvisar_nueva_armonia()
            accepted = self._actualizar_harmony_memory(candidate)

            if self.dimension == 2:
                x, y = candidate.values
                original_value = self._objective_original(candidate.values)
                self.search_points_2d.append((x, y, original_value, accepted))

            best = self.harmony_memory[0]
            best_original = self._objective_original(best.values)
            self.best_fitness_history.append(best_original)

            if self.dimension == 2:
                self.best_points_2d_history.append((best.values[0], best.values[1]))

            if verbose and (it == 1 or it == iterations or it % report_step == 0):
                print(f"Iteracion {it:5d} | Mejor valor objetivo: {best_original:.8f}")

        best = self.harmony_memory[0]
        return best.values, self._objective_original(best.values)


def funcion_esfera_2d(x: Sequence[float]) -> float:
    """
    Funcion esfera en 2 dimensiones: f(x, y) = x^2 + y^2

    Minimo global teorico:
    - Punto: (0, 0)
    - Valor: 0
    """
    return x[0] ** 2 + x[1] ** 2


def graficar_funcion_objetivo_y_busqueda(
    optimizer: BusquedaArmonicaV2,
    title: str = "Busqueda Armonica V2 - Funcion Objetivo y Puntos de Busqueda",
    save_path: str = "busqueda_armonica_v2_resultado.png",
    known_optimum: Optional[Tuple[float, float]] = None,
    grid_points: int = 220,
) -> None:
    """
    Genera un grafico de contornos de la funcion objetivo y superpone:
    1) puntos candidatos evaluados,
    2) trayectoria del mejor punto por iteracion,
    3) mejor punto final,
    4) optimo conocido (si se proporciona).

    Requisito: problema de 2 dimensiones.
    """
    if optimizer.dimension != 2:
        raise ValueError("La visualizacion 2D requiere exactamente dos dimensiones.")

    if not optimizer.search_points_2d:
        raise ValueError("No hay puntos registrados. Ejecuta optimizar() antes de graficar.")

    (x_min, x_max), (y_min, y_max) = optimizer.bounds

    # Construccion de malla regular para evaluar la funcion objetivo.
    x_values = np.linspace(x_min, x_max, grid_points)
    y_values = np.linspace(y_min, y_max, grid_points)
    X, Y = np.meshgrid(x_values, y_values)

    # Evaluacion vectorizada de la funcion sobre la malla.
    Z = np.zeros_like(X, dtype=float)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = optimizer.objective_function([float(X[i, j]), float(Y[i, j])])

    fig, ax = plt.subplots(figsize=(10, 8))

    # Mapa de contornos para lectura de relieve de la funcion.
    contour = ax.contourf(X, Y, Z, levels=60, cmap="viridis")
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label("Valor de la funcion objetivo")

    # Puntos evaluados por el algoritmo (candidatos improvisados).
    xs = [p[0] for p in optimizer.search_points_2d]
    ys = [p[1] for p in optimizer.search_points_2d]

    # Colorear puntos por indice temporal (iteracion) para observar dinamica.
    time_index = np.arange(len(xs))
    scatter = ax.scatter(
        xs,
        ys,
        c=time_index,
        cmap="plasma",
        s=16,
        alpha=0.65,
        edgecolors="none",
        label="Puntos de busqueda (candidato por iteracion)",
    )
    cbar_time = fig.colorbar(scatter, ax=ax)
    cbar_time.set_label("Iteracion")

    # Trayectoria del mejor punto historico por iteracion.
    best_x = [p[0] for p in optimizer.best_points_2d_history]
    best_y = [p[1] for p in optimizer.best_points_2d_history]
    ax.plot(
        best_x,
        best_y,
        color="white",
        linewidth=1.5,
        alpha=0.9,
        label="Trayectoria del mejor punto",
    )

    # Mejor punto final.
    final_best = optimizer.harmony_memory[0].values
    ax.scatter(
        [final_best[0]],
        [final_best[1]],
        color="red",
        marker="*",
        s=220,
        label="Mejor punto final",
        zorder=5,
    )

    # Punto del optimo teorico, si se conoce y se proporciona.
    if known_optimum is not None:
        ax.scatter(
            [known_optimum[0]],
            [known_optimum[1]],
            color="cyan",
            marker="X",
            s=140,
            label="Optimo conocido",
            zorder=6,
        )

    ax.set_title(title)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig(save_path, dpi=220)
    plt.close(fig)


def imprimir_resumen_aproximacion(
    optimizer: BusquedaArmonicaV2,
    known_optimum_value: Optional[float] = None,
    threshold: float = 1e-3,
) -> None:
    """
    Muestra un resumen textual de la aproximacion al valor objetivo.

    - Informa mejor valor final.
    - Si se proporciona valor optimo teorico, reporta error absoluto final.
    - Indica cuantas iteraciones quedaron por debajo de un umbral de valor
      objetivo para evidenciar acercamiento al optimo.
    """
    if not optimizer.best_fitness_history:
        print("No existe historial de optimizacion para resumir.")
        return

    final_best = optimizer.best_fitness_history[-1]
    print("\nResumen de aproximacion:")
    print(f"Mejor valor final encontrado: {final_best:.10f}")

    if known_optimum_value is not None:
        abs_error = abs(final_best - known_optimum_value)
        print(f"Error absoluto respecto al optimo teorico: {abs_error:.10f}")

    below_threshold = sum(1 for val in optimizer.best_fitness_history if val <= threshold)
    print(f"Iteraciones con mejor valor <= {threshold}: {below_threshold} de {len(optimizer.best_fitness_history)}")


if __name__ == "__main__":
    # Ejemplo academico en 2D para poder graficar funcion y trayectoria.
    limites = [(-5.0, 5.0), (-5.0, 5.0)]

    hs_v2 = BusquedaArmonicaV2(
        objective_function=funcion_esfera_2d,
        bounds=limites,
        harmony_memory_size=30,
        harmony_memory_consideration_rate=0.90,
        pitch_adjustment_rate=0.35,
        bandwidth=0.02,
        randomize_rate=0.08,
        maximize=False,
        seed=42,
    )

    mejor_x, mejor_f = hs_v2.optimizar(iterations=400, verbose=True)

    print("\nResultado final:")
    print(f"Mejor solucion encontrada: {mejor_x}")
    print(f"Mejor valor objetivo: {mejor_f:.10f}")

    imprimir_resumen_aproximacion(
        optimizer=hs_v2,
        known_optimum_value=0.0,
        threshold=1e-3,
    )

    salida_grafico = "InteligenciaArtifical1/IntArt/busqueda_armonica_v2_resultado.png"
    graficar_funcion_objetivo_y_busqueda(
        optimizer=hs_v2,
        title="Harmony Search V2 sobre Funcion Esfera 2D",
        save_path=salida_grafico,
        known_optimum=(0.0, 0.0),
        grid_points=220,
    )

    print(f"Grafico guardado en: {salida_grafico}")

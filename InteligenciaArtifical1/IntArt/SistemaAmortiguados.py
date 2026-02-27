import numpy as np
import matplotlib.pyplot as plt

# Configuración de tiempo
t = np.linspace(0, 10, 1000)

# Función para calcular la respuesta del sistema
def respuesta_sistema(zeta, t, wn=2.0):
    if zeta < 1:    # Subamortiguado
        wd = wn * np.sqrt(1 - zeta**2)
        return np.exp(-zeta * wn * t) * np.cos(wd * t)
    elif zeta == 1: # Críticamente amortiguado
        return (1 + wn * t) * np.exp(-wn * t)
    else:           # Sobreamortiguado
        r1 = -wn * (zeta - np.sqrt(zeta**2 - 1))
        r2 = -wn * (zeta + np.sqrt(zeta**2 - 1))
        # Simplificación para visualización
        return 0.5 * (np.exp(r1 * t) + np.exp(r2 * t))

# Crear la gráfica
plt.figure(figsize=(10, 6))

# 1. Subamortiguado (Zeta entre 0 y 1)
plt.plot(t, respuesta_sistema(0.2, t), label='Subamortiguado ($\zeta=0.2$)', color='blue')

# 2. Críticamente amortiguado (Zeta igual a 1)
plt.plot(t, respuesta_sistema(1.0, t), label='Crítico ($\zeta=1.0$)', color='red', linewidth=3)

# 3. Sobreamortiguado (Zeta mayor a 1)
plt.plot(t, respuesta_sistema(2.5, t), label='Sobreamortiguado ($\zeta=2.5$)', color='green')

# Configuración visual
plt.axhline(0, color='black', lw=1)
plt.title('Comparación de Sistemas Amortiguados')
plt.xlabel('Tiempo (s)')
plt.ylabel('Desplazamiento (x)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
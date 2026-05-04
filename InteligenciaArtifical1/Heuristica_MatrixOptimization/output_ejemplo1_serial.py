# CÓDIGO GENERADO AUTOMÁTICAMENTE - VERSIÓN SERIAL
# Expresión: (A @ B) + (C @ D)

import numpy as np
import time

def execute_serial(matrices):
    """Ejecución SERIAL de la expresión matricial."""
    start_time = time.time()

    temp_0 = np.matmul(matrices['A'], matrices['B'])
    temp_1 = np.matmul(matrices['C'], matrices['D'])
    temp_2 = temp_0 + temp_1

    end_time = time.time()
    return temp_2, end_time - start_time
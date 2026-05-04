# CÓDIGO GENERADO AUTOMÁTICAMENTE - VERSIÓN PARALELA
# Expresión: (A @ B) + (C @ D)

import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def execute_parallel(matrices, num_workers=4):
    """Ejecución PARALELA de la expresión matricial."""
    start_time = time.time()

    # Diccionario para almacenar resultados
    results = {}
    
    # Copiar referencias a matrices de entrada
    for key, value in matrices.items():
        results[key] = value
    
    # Definir funciones de operación
    def op_1(left, right):
        return np.matmul(left, right)

    def op_2(left, right):
        return np.matmul(left, right)

    def op_0(left, right):
        return left + right

    # Lista de tareas a ejecutar
    tasks = []  # (op_id, func, left_operand_key, right_operand_key)
    
    tasks.append((1, op_1, 'A', 'B', 'temp_1'))
    tasks.append((2, op_2, 'C', 'D', 'temp_2'))
    tasks.append((0, op_0, 'temp_1', 'temp_2', 'temp_0'))
    
    # Ejecutar tareas en paralelo respetando dependencias
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_task = {}
        pending_tasks = list(tasks)
        
        # Ciclo: lanzar tareas cuando sus dependencias se completan
        while pending_tasks or future_to_task:
            # Lanzar tareas cuyas dependencias ya están en results
            remaining_tasks = []
            for task in pending_tasks:
                op_id, func, left_key, right_key, result_key = task
                if left_key in results and right_key in results:
                    left = results[left_key]
                    right = results[right_key]
                    future = executor.submit(func, left, right)
                    future_to_task[future] = (op_id, result_key)
                else:
                    remaining_tasks.append(task)
            pending_tasks = remaining_tasks
            
            # Recopilar resultados conforme se completen
            if future_to_task:
                done_futures = list(as_completed(future_to_task))
                for future in done_futures:
                    op_id, result_key = future_to_task.pop(future)
                    results[result_key] = future.result()
    
    end_time = time.time()
    return results['temp_0'], end_time - start_time
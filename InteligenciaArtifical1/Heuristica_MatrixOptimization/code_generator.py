"""
Generador de código Python para expresiones matriciales.

Genera versiones serial y paralela del código basándose en el AST.
"""

from typing import Union, Dict, Set, List
from matrix_parser import BinOp, MatrixVar, get_dependencies
import textwrap


class CodeGeneratorSerial:
    """Genera código Python serial (ejecución secuencial)."""
    
    def __init__(self, ast: Union[BinOp, MatrixVar], matrix_vars: Set[str]):
        """
        Inicializa el generador serial.
        
        Args:
            ast: Árbol de sintaxis abstracta
            matrix_vars: Conjunto de nombres de variables matriciales
        """
        self.ast = ast
        self.matrix_vars = matrix_vars
        self.ops_list, self.graph, _ = get_dependencies(ast)
        self.var_counter = 0
    
    def _new_var_name(self) -> str:
        """Genera un nuevo nombre de variable temporal."""
        name = f"temp_{self.var_counter}"
        self.var_counter += 1
        return name
    
    def generate(self) -> str:
        """
        Genera código Python serial.
        
        Returns:
            Código Python como string
        """
        code_lines = []
        
        # Header
        code_lines.append("import numpy as np")
        code_lines.append("import time")
        code_lines.append("")
        code_lines.append("def execute_serial(matrices):")
        code_lines.append('    """Ejecución SERIAL de la expresión matricial."""')
        code_lines.append("    start_time = time.time()")
        code_lines.append("")
        
        # Mapeo de op_id -> variable temporal
        op_to_var = {}
        
        # Generar código para cada operación
        for op_info in self.ops_list:
            op_id = op_info['id']
            op = op_info['op']
            
            # Obtener operandos
            left_operand = self._get_operand(op_info['left'], op_info['left_id'], op_to_var)
            right_operand = self._get_operand(op_info['right'], op_info['right_id'], op_to_var)
            
            # Crear variable temporal para resultado
            result_var = self._new_var_name()
            op_to_var[op_id] = result_var
            
            # Generar línea de operación
            if op == '@':
                operation = f"{result_var} = np.matmul({left_operand}, {right_operand})"
            elif op == '+':
                operation = f"{result_var} = {left_operand} + {right_operand}"
            elif op == '-':
                operation = f"{result_var} = {left_operand} - {right_operand}"
            
            code_lines.append(f"    {operation}")
        
        # Retornar resultado
        final_op_id = self.ops_list[-1]['id'] if self.ops_list else None
        final_var = op_to_var.get(final_op_id)
        
        code_lines.append("")
        code_lines.append("    end_time = time.time()")
        code_lines.append(f"    return {final_var}, end_time - start_time")
        
        return "\n".join(code_lines)
    
    def _get_operand(self, node: Union[BinOp, MatrixVar], op_id: int, 
                     op_to_var: Dict) -> str:
        """
        Obtiene la representación del operando (variable o resultado temporal).
        
        Args:
            node: Nodo del AST
            op_id: ID de la operación (si es binop)
            op_to_var: Mapeo de op_id a variable temporal
            
        Returns:
            String con el nombre de la variable o referencia
        """
        if isinstance(node, MatrixVar):
            return f"matrices['{node.name}']"
        elif isinstance(node, BinOp):
            return op_to_var[op_id]


class CodeGeneratorParallel:
    """Genera código Python paralelo (con ThreadPoolExecutor o multiprocessing)."""
    
    def __init__(self, ast: Union[BinOp, MatrixVar], matrix_vars: Set[str], 
                 num_workers: int = 4):
        """
        Inicializa el generador paralelo.
        
        Args:
            ast: Árbol de sintaxis abstracta
            matrix_vars: Conjunto de nombres de variables matriciales
            num_workers: Número de workers para paralelismo
        """
        self.ast = ast
        self.matrix_vars = matrix_vars
        self.ops_list, self.graph, _ = get_dependencies(ast)
        self.num_workers = num_workers
        self.var_counter = 0
    
    def _new_var_name(self) -> str:
        """Genera un nuevo nombre de variable temporal."""
        name = f"temp_{self.var_counter}"
        self.var_counter += 1
        return name
    
    def generate(self) -> str:
        """
        Genera código Python paralelo.
        
        Usa ThreadPoolExecutor para ejecutar operaciones independientes en paralelo.
        
        Returns:
            Código Python como string
        """
        # Nota para estudiantes:
        # - La versión paralela usa `ThreadPoolExecutor` que es simple de entender
        #   y funciona bien cuando cada tarea libera el GIL (por ejemplo numpy
        #   usa C internals). Sin embargo, para cargas puramente CPU-bound
        #   en Python, `ProcessPoolExecutor` o `multiprocessing` puede ser
        #   más efectivo porque evita el GIL.
        # - La sección donde se lanzan tareas (submit) y se recoge resultados
        #   (as_completed) es clave: respeta dependencias del DAG evitando
        #   condiciones de carrera.
        code_lines = []
        
        # Header
        code_lines.append("import numpy as np")
        code_lines.append("import time")
        code_lines.append("from concurrent.futures import ThreadPoolExecutor, as_completed")
        code_lines.append("")
        code_lines.append("def execute_parallel(matrices, num_workers=4):")
        code_lines.append('    """Ejecución PARALELA de la expresión matricial."""')
        code_lines.append("    start_time = time.time()")
        code_lines.append("")
        code_lines.append("    # Diccionario para almacenar resultados")
        code_lines.append("    results = {}")
        code_lines.append("    ")
        code_lines.append("    # Copiar referencias a matrices de entrada")
        code_lines.append("    for key, value in matrices.items():")
        code_lines.append("        results[key] = value")
        code_lines.append("    ")
        
        # Generar funciones de operación
        code_lines.append("    # Definir funciones de operación")
        op_func_names = {}
        for op_info in self.ops_list:
            op_id = op_info['id']
            func_name = f"op_{op_id}"
            op_func_names[op_id] = func_name
            
            op = op_info['op']
            
            if op == '@':
                code_lines.append(f"    def {func_name}(left, right):")
                code_lines.append(f"        return np.matmul(left, right)")
            elif op == '+':
                code_lines.append(f"    def {func_name}(left, right):")
                code_lines.append(f"        return left + right")
            elif op == '-':
                code_lines.append(f"    def {func_name}(left, right):")
                code_lines.append(f"        return left - right")
            code_lines.append("")
        
        # Generar lista de tareas
        code_lines.append("    # Lista de tareas a ejecutar")
        code_lines.append("    tasks = []  # (op_id, func, left_operand_key, right_operand_key)")
        code_lines.append("    ")
        
        # Mapeo de operandos
        op_to_key = {}  # op_id -> clave en results
        
        for op_info in self.ops_list:
            op_id = op_info['id']
            func_name = op_func_names[op_id]
            
            # Obtener claves de operandos
            left_key = self._get_operand_key(op_info['left'], op_info['left_id'], op_to_key)
            right_key = self._get_operand_key(op_info['right'], op_info['right_id'], op_to_key)
            
            # Crear clave para resultado
            result_key = f"temp_{op_id}"
            op_to_key[op_id] = result_key
            
            code_lines.append(f"    tasks.append(({op_id}, {func_name}, '{left_key}', '{right_key}', '{result_key}'))")
        
        code_lines.append("    ")
        code_lines.append("    # Ejecutar tareas en paralelo respetando dependencias")
        code_lines.append("    with ThreadPoolExecutor(max_workers=num_workers) as executor:")
        code_lines.append("        future_to_task = {}")
        code_lines.append("        pending_tasks = list(tasks)")
        code_lines.append("        ")
        code_lines.append("        # Ciclo: lanzar tareas cuando sus dependencias se completan")
        code_lines.append("        while pending_tasks or future_to_task:")
        code_lines.append("            # Lanzar tareas cuyas dependencias ya están en results")
        code_lines.append("            remaining_tasks = []")
        code_lines.append("            for task in pending_tasks:")
        code_lines.append("                op_id, func, left_key, right_key, result_key = task")
        code_lines.append("                if left_key in results and right_key in results:")
        code_lines.append("                    left = results[left_key]")
        code_lines.append("                    right = results[right_key]")
        code_lines.append("                    future = executor.submit(func, left, right)")
        code_lines.append("                    future_to_task[future] = (op_id, result_key)")
        code_lines.append("                else:")
        code_lines.append("                    remaining_tasks.append(task)")
        code_lines.append("            pending_tasks = remaining_tasks")
        code_lines.append("            ")
        code_lines.append("            # Recopilar resultados conforme se completen")
        code_lines.append("            if future_to_task:")
        code_lines.append("                done_futures = list(as_completed(future_to_task))")
        code_lines.append("                for future in done_futures:")
        code_lines.append("                    op_id, result_key = future_to_task.pop(future)")
        code_lines.append("                    results[result_key] = future.result()")
        code_lines.append("    ")
        
        # Retornar resultado
        final_op_id = self.ops_list[-1]['id'] if self.ops_list else None
        final_key = op_to_key.get(final_op_id)
        
        code_lines.append("    end_time = time.time()")
        code_lines.append(f"    return results['{final_key}'], end_time - start_time")
        
        return "\n".join(code_lines)
    
    def _get_operand_key(self, node: Union[BinOp, MatrixVar], op_id: int, 
                         op_to_key: Dict) -> str:
        """
        Obtiene la clave del operando en el diccionario de resultados.
        
        Args:
            node: Nodo del AST
            op_id: ID de la operación (si es binop)
            op_to_key: Mapeo de op_id a clave
            
        Returns:
            String con la clave
        """
        if isinstance(node, MatrixVar):
            return node.name
        elif isinstance(node, BinOp):
            return op_to_key[op_id]


# Ejemplos de uso
if __name__ == "__main__":
    from matrix_parser import MatrixExpressionParser
    
    # Parsear expresión
    expr = "(A @ B) + (C @ D)"
    parser = MatrixExpressionParser(expr)
    ast = parser.parse()
    _, _, vars_set = get_dependencies(ast)
    
    print("=" * 60)
    print(f"EXPRESIÓN: {expr}")
    print("=" * 60)
    print()
    
    # Generar código serial
    print("CÓDIGO SERIAL:")
    print("-" * 60)
    gen_serial = CodeGeneratorSerial(ast, vars_set)
    code_serial = gen_serial.generate()
    print(code_serial)
    print()
    
    # Generar código paralelo
    print("CÓDIGO PARALELO:")
    print("-" * 60)
    gen_parallel = CodeGeneratorParallel(ast, vars_set, num_workers=4)
    code_parallel = gen_parallel.generate()
    print(code_parallel)

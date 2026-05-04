"""
Interfaz Gráfica (GUI) para el proyecto de Heurística de Optimización Matricial.

Proporciona interfaz visual para:
- Fase 1: Comparación serial vs paralelo
- Fase 2: Optimización con Algoritmo Genético

Implementado con tkinter (librería estándar Python).
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import numpy as np
from typing import Dict, Tuple
import traceback

from matrix_parser import MatrixExpressionParser, get_dependencies
from executor import MatrixExpressionExecutor
from plan_optimizer import PlanOptimizer


class GUIApp:
    """Aplicación gráfica para la Heurística de Optimización Matricial."""
    
    def __init__(self, root: tk.Tk):
        """Inicializa la GUI."""
        self.root = root
        self.root.title("Heurística de Optimización de Expresiones Matriciales")
        self.root.geometry("900x700")
        
        # Variables globales
        self.is_running = False
        self.matrices: Dict = {}
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz gráfica."""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Panel principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # ===== SECCIÓN 1: Entrada de Expresión =====
        frame_expr = ttk.LabelFrame(main_frame, text="Expresión Matricial", padding="10")
        frame_expr.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        frame_expr.columnconfigure(1, weight=1)
        
        ttk.Label(frame_expr, text="Expresión:").grid(row=0, column=0, sticky=tk.W)
        self.expr_entry = ttk.Entry(frame_expr)
        self.expr_entry.insert(0, "(A @ B) + (C @ D)")
        self.expr_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # ===== SECCIÓN 2: Parámetros de Matrices =====
        frame_params = ttk.LabelFrame(main_frame, text="Parámetros", padding="10")
        frame_params.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        frame_params.columnconfigure(1, weight=1)
        frame_params.columnconfigure(3, weight=1)
        
        ttk.Label(frame_params, text="Tamaño de matrices:").grid(row=0, column=0, sticky=tk.W)
        self.size_entry = ttk.Entry(frame_params, width=10)
        self.size_entry.insert(0, "300")
        self.size_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_params, text="Número de workers:").grid(row=0, column=2, sticky=tk.W)
        self.workers_var = tk.IntVar(value=4)
        self.workers_spinbox = ttk.Spinbox(
            frame_params, from_=1, to=8, textvariable=self.workers_var, width=5
        )
        self.workers_spinbox.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # ===== SECCIÓN 3: Parámetros del AG =====
        frame_ag = ttk.LabelFrame(main_frame, text="Parámetros Algoritmo Genético", padding="10")
        frame_ag.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        frame_ag.columnconfigure(1, weight=1)
        frame_ag.columnconfigure(3, weight=1)
        frame_ag.columnconfigure(5, weight=1)
        
        ttk.Label(frame_ag, text="Población:").grid(row=0, column=0, sticky=tk.W)
        self.pop_spinbox = ttk.Spinbox(frame_ag, from_=5, to=50, width=5)
        self.pop_spinbox.set(15)
        self.pop_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_ag, text="Generaciones:").grid(row=0, column=2, sticky=tk.W)
        self.gen_spinbox = ttk.Spinbox(frame_ag, from_=5, to=100, width=5)
        self.gen_spinbox.set(20)
        self.gen_spinbox.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(frame_ag, text="Mutación (0-1):").grid(row=0, column=4, sticky=tk.W)
        self.mut_spinbox = ttk.Spinbox(frame_ag, from_=0.0, to=1.0, increment=0.05, width=5)
        self.mut_spinbox.set(0.15)
        self.mut_spinbox.grid(row=0, column=5, sticky=tk.W, padx=5)
        
        # ===== SECCIÓN 4: Botones de Acción =====
        frame_buttons = ttk.Frame(main_frame, padding="10")
        frame_buttons.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.btn_fase1 = ttk.Button(
            frame_buttons, text="▶ Ejecutar FASE 1 (Serial vs Paralelo)",
            command=self._run_fase1
        )
        self.btn_fase1.pack(side=tk.LEFT, padx=5)
        
        self.btn_fase2 = ttk.Button(
            frame_buttons, text="▶ Ejecutar FASE 2 (Algoritmo Genético)",
            command=self._run_fase2
        )
        self.btn_fase2.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = ttk.Button(
            frame_buttons, text="🗑️ Limpiar", command=self._clear_output
        )
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # ===== SECCIÓN 5: Área de Salida =====
        frame_output = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        frame_output.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        frame_output.columnconfigure(0, weight=1)
        frame_output.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            frame_output, height=15, width=100, wrap=tk.WORD
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de progreso
        frame_progress = ttk.Frame(main_frame)
        frame_progress.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_bar = ttk.Progressbar(
            frame_progress, mode='indeterminate'
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.status_label = ttk.Label(frame_progress, text="Listo")
        self.status_label.pack(side=tk.LEFT, padx=5)
    
    def _log(self, message: str):
        """Añade mensaje al área de salida."""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def _clear_output(self):
        """Limpia el área de salida."""
        self.output_text.delete(1.0, tk.END)
        self.status_label.config(text="Listo")
    
    def _get_matrices(self) -> Dict:
        """Crea matrices de prueba según la expresión."""
        try:
            # Parsear expresión para obtener variables
            parser = MatrixExpressionParser(self.expr_entry.get())
            ast = parser.parse()
            _, _, matrix_vars = get_dependencies(ast)
            
            # Obtener tamaño
            size_str = self.size_entry.get()
            if 'x' in size_str:
                rows, cols = map(int, size_str.split('x'))
            else:
                rows = cols = int(size_str)
            
            # Crear matrices
            np.random.seed(42)
            matrices = {}
            for var in sorted(matrix_vars):
                matrices[var] = np.random.randn(rows, cols).astype(np.float64)
            
            return matrices
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear matrices: {str(e)}")
            return {}
    
    def _run_fase1(self):
        """Ejecuta Fase 1 en hilo separado (serial vs paralelo)."""
        if self.is_running:
            messagebox.showwarning("Ocupado", "Ya hay una ejecución en curso")
            return
        
        self.is_running = True
        self.progress_bar.start()
        self.status_label.config(text="Ejecutando Fase 1...")
        
        def task():
            try:
                self._clear_output()
                expression = self.expr_entry.get().strip()
                
                if not expression:
                    self._log("Error: Ingrese una expresión válida")
                    return
                
                self._log("="*70)
                self._log("FASE 1: COMPARACIÓN SERIAL VS PARALELO")
                self._log("="*70)
                self._log("")
                self._log(f"Expresión: {expression}")
                self._log("")
                
                # Crear matrices
                matrices = self._get_matrices()
                if not matrices:
                    return
                
                self._log(f"Matrices creadas: {list(matrices.keys())}")
                self._log(f"Tamaño: {matrices[list(matrices.keys())[0]].shape}")
                self._log("")
                
                # Crear executor
                num_workers = self.workers_var.get()
                executor = MatrixExpressionExecutor(
                    expression, matrices, num_workers=num_workers
                )
                
                # Ejecutar comparación
                self._log("Ejecutando versión SERIAL...")
                result_s, time_s, std_s = executor.execute_serial(num_runs=2)
                self._log(f"  Tiempo: {time_s*1000:.4f} ms (±{std_s*1000:.4f} ms)")
                self._log("")
                
                self._log("Ejecutando versión PARALELA...")
                result_p, time_p, std_p = executor.execute_parallel(num_runs=2)
                self._log(f"  Tiempo: {time_p*1000:.4f} ms (±{std_p*1000:.4f} ms)")
                self._log("")
                
                # Calcular métricas
                speedup = time_s / time_p if time_p > 0 else 0
                improvement = ((time_s - time_p) / time_s * 100) if time_s > 0 else 0
                
                self._log("="*70)
                self._log("RESULTADOS:")
                self._log("="*70)
                self._log(f"Speedup: {speedup:.3f}x")
                self._log(f"Mejora: {improvement:+.2f}%")
                self._log(f"Resultados coinciden: {np.allclose(result_s, result_p)}")
                self._log("")
                
                if speedup > 1.0:
                    self._log("✓ PARALELO es más rápido")
                else:
                    self._log("✓ SERIAL es más rápido (overhead no compensa)")
                
            except Exception as e:
                self._log(f"ERROR: {str(e)}")
                self._log(traceback.format_exc())
            
            finally:
                self.is_running = False
                self.progress_bar.stop()
                self.status_label.config(text="Listo")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=task)
        thread.daemon = True
        thread.start()
    
    def _run_fase2(self):
        """Ejecuta Fase 2 en hilo separado (Algoritmo Genético)."""
        if self.is_running:
            messagebox.showwarning("Ocupado", "Ya hay una ejecución en curso")
            return
        
        self.is_running = True
        self.progress_bar.start()
        self.status_label.config(text="Ejecutando Fase 2...")
        
        def task():
            try:
                self._clear_output()
                expression = self.expr_entry.get().strip()
                
                if not expression:
                    self._log("Error: Ingrese una expresión válida")
                    return
                
                self._log("="*70)
                self._log("FASE 2: OPTIMIZACIÓN CON ALGORITMO GENÉTICO")
                self._log("="*70)
                self._log("")
                self._log(f"Expresión: {expression}")
                self._log("")
                
                # Crear matrices
                matrices = self._get_matrices()
                if not matrices:
                    return
                
                self._log(f"Matrices creadas: {list(matrices.keys())}")
                self._log(f"Tamaño: {matrices[list(matrices.keys())[0]].shape}")
                self._log("")
                
                # Parámetros del AG
                population_size = int(self.pop_spinbox.get())
                generations = int(self.gen_spinbox.get())
                mutation_rate = float(self.mut_spinbox.get())
                
                self._log(f"Parámetros del AG:")
                self._log(f"  Población: {population_size}")
                self._log(f"  Generaciones: {generations}")
                self._log(f"  Mutación: {mutation_rate}")
                self._log("")
                self._log("Optimizando...")
                self._log("")
                
                # Crear optimizador
                optimizer = PlanOptimizer(
                    expression=expression,
                    matrices=matrices,
                    population_size=population_size,
                    generations=generations,
                    mutation_rate=mutation_rate,
                    crossover_rate=0.8,
                    num_runs=1,
                    verbose=False
                )
                
                # Optimizar
                best_plan, stats = optimizer.optimize()
                
                self._log("="*70)
                self._log("MEJOR PLAN ENCONTRADO")
                self._log("="*70)
                self._log(f"Usar paralelo: {best_plan.use_parallel}")
                if best_plan.use_parallel:
                    self._log(f"Número de workers: {best_plan.num_workers}")
                    strategies = {0: "Greedy", 1: "Balanced", 2: "Adaptive"}
                    self._log(f"Estrategia: {strategies.get(best_plan.scheduling_strategy, '?')}")
                self._log(f"Umbral de tamaño: {best_plan.size_threshold}")
                self._log(f"Fitness: {best_plan.fitness:.4f} ms")
                self._log("")
                
                self._log("ESTADÍSTICAS:")
                self._log(f"  Mejor fitness: {stats['best_fitness']:.4f} ms")
                self._log(f"  Peor fitness: {stats['worst_fitness']:.4f} ms")
                self._log(f"  Promedio: {stats['avg_fitness']:.4f} ms")
                self._log(f"  Mejora: {stats['improvement']:.2f}%")
                self._log("")
                
                # Recomendación
                if best_plan.use_parallel:
                    self._log("✓ RECOMENDACIÓN: PARALELIZAR")
                else:
                    self._log("✓ RECOMENDACIÓN: EJECUTAR SECUENCIAL")
                
            except Exception as e:
                self._log(f"ERROR: {str(e)}")
                self._log(traceback.format_exc())
            
            finally:
                self.is_running = False
                self.progress_bar.stop()
                self.status_label.config(text="Listo")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=task)
        thread.daemon = True
        thread.start()


def run_gui():
    """Inicia la aplicación gráfica."""
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()

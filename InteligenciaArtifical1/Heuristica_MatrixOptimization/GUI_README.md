# Uso de la Interfaz Gráfica (GUI)

## ¿Cómo ejecutar la GUI?

### Opción 1: Desde el menú principal
```bash
python main.py
```
Luego selecciona opción `2. Interfaz gráfica (GUI)`.

### Opción 2: Directamente
```bash
python gui.py
```

---

## Componentes de la Interfaz

### 1. **Expresión Matricial**
- Campo de entrada para tu expresión
- Ejemplo: `(A @ B) + (C @ D)`
- Operadores: `@` (multiplicación), `+` (suma), `-` (resta)

### 2. **Parámetros de Matrices**
- **Tamaño**: Ingresa un número para matriz cuadrada (ej: 300) 
  o ancho×alto (ej: 300x500)
- **Workers**: Número de hilos para paralelismo [1-8]

### 3. **Parámetros del Algoritmo Genético (Fase 2)**
- **Población**: Número de individuos [5-50]
- **Generaciones**: Iteraciones del AG [5-100]
- **Mutación**: Probabilidad de mutación [0.0-1.0]

### 4. **Botones de Acción**
- **▶ Ejecutar FASE 1**: Compara serial vs paralelo
- **▶ Ejecutar FASE 2**: Optimiza con Algoritmo Genético
- **🗑️ Limpiar**: Borra la salida anterior

### 5. **Área de Resultados**
- Muestra toda la salida de las ejecuciones
- Puedes hacer scroll para ver mensajes antiguos
- Incluye barra de progreso durante la ejecución

---

## Ejemplos de Uso

### Ejemplo 1: Comparar Serial vs Paralelo (Fase 1)

1. Deja la expresión por defecto: `(A @ B) + (C @ D)`
2. Tamaño: `300` (matrices 300×300)
3. Haz clic en "▶ Ejecutar FASE 1 (Serial vs Paralelo)"
4. Espera los resultados (toma unos segundos)
5. Observa: ¿Serial o paralelo fue más rápido?

### Ejemplo 2: Optimizar con Algoritmo Genético (Fase 2)

1. Expresión: `(A @ B) + (C @ D)`
2. Tamaño: `150` (menos para que sea rápido)
3. Parámetros AG: Población=10, Generaciones=5, Mutación=0.15
4. Haz clic en "▶ Ejecutar FASE 2 (Algoritmo Genético)"
5. El AG evoluciona el mejor plan
6. Ve la recomendación: ¿paralelizar o no?

---

## Notas para Estudiantes

- Los resultados de time son **ruidosos** (varían entre ejecuciones).
  Esto es normal en computación paralela.
- Para experimentos reproducibles, ejecuta múltiples veces
  y observa el promedio.
- **Prueba diferente tamaños**: 
  - Pequeño (100): serial probablemente gane
  - Grande (1000): paralelo probablemente gane
- **Experimenta con el AG**:
  - Población pequeña = menos tiempo pero peor solución
  - Población grande = más tiempo pero mejor solución

---

## Requisitos

- Python 3.7+
- tkinter (incluido en Python estándar)
- numpy (ya instalado en el proyecto)

---

## Solución de Problemas

### "No se puede importar gui.py"
- Asegúrate de estar en la carpeta `Heuristica_MatrixOptimization/`
- Verifica que `gui.py` esté en la misma carpeta que `main.py`

### GUI no abre o parece congelada
- Esto puede suceder en sistemas sin servidor X11
- Usa la interfaz CLI en su lugar: `python main.py` → opción 1

### Los tiempos son muy variables
- Esto es normal en paralelismo
- Aumenta `num_runs` en el código si necesitas resultados más estables

---

¡Listo! Disfruta experimentando con la GUI.

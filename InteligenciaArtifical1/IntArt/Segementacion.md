# Guía rápida: Segmentación de imagen con ACO

Este documento explica cómo ejecutar `SegmentacionImagen.py`, qué significa el comando:

`python .\SegmentacionImagen.py .\tu_imagen.jpg --umbrales 2 --hormigas 20 --iteraciones 80`

y una breve teoría del método usado.

---

## 1) ¿Qué hace el programa?

`SegmentacionImagen.py` toma una imagen (por ejemplo `.jpg` o `.png`), la convierte a escala de grises y busca **umbrales óptimos** para segmentarla en varios niveles.

El resultado se guarda automáticamente con este formato:

`NombreArchivo_Output_Segmentada.Extension`

Ejemplo:
- Entrada: `tu_imagen.jpg`
- Salida: `tu_imagen_Output_Segmentada.jpg`

---

## 2) Explicación del comando

Comando:

`python .\SegmentacionImagen.py .\tu_imagen.jpg --umbrales 2 --hormigas 20 --iteraciones 80`

Significado de cada parte:

- `python`
  - Ejecuta Python.
- `.\SegmentacionImagen.py`
  - Es el script del programa.
- `.\tu_imagen.jpg`
  - Ruta de la imagen de entrada.
- `--umbrales 2`
  - Usa 2 umbrales (segmentación multinivel con 3 clases: baja, media y alta intensidad).
- `--hormigas 20`
  - Número de hormigas por iteración del algoritmo ACO.
- `--iteraciones 80`
  - Número de iteraciones totales del algoritmo.

---

## 3) ¿Cómo ejecutar el programa?

1. Abre una terminal en la carpeta donde están los archivos (`IntArt`).
2. Ejecuta, por ejemplo:

`python .\SegmentacionImagen.py .\mi_foto.png --umbrales 2 --hormigas 20 --iteraciones 80`

3. Espera a que termine (verás resultados por iteración, a menos que uses `--silencioso`).
4. Revisa la imagen generada en la misma carpeta.

También puedes usar más parámetros opcionales:

- `--alpha` peso de feromona (default 1.0)
- `--beta` peso heurístico (default 2.0)
- `--rho` evaporación (default 0.4)
- `--q` depósito de feromona (default 50.0)
- `--semilla` semilla aleatoria (default 42)
- `--silencioso` oculta el progreso por iteraciones

---

## 4) Breve teoría detrás del programa

El programa combina:

1. **ACO (Ant Colony Optimization)**
   - Varias hormigas construyen soluciones candidatas (conjuntos de umbrales).
   - Cada decisión usa probabilidad basada en:
     - **Feromona** (`tau`): memoria de buenas decisiones previas.
     - **Heurística** (`eta`): información local de qué tan prometedora es la transición.
   - Después de evaluar soluciones, se actualiza feromona con evaporación y depósito.

2. **Entropía de Shannon (Kapur)**
   - Para cada conjunto de umbrales, se calcula la entropía de las clases generadas en el histograma.
   - Se busca **maximizar** la entropía total, porque separaciones con mayor información suelen producir mejor segmentación.

En resumen:
- ACO explora y mejora umbrales iterativamente.
- Shannon/Kapur evalúa la calidad de esos umbrales.
- El mejor conjunto final se aplica para producir la imagen segmentada.

---

## 5) Recomendaciones rápidas

- Si la segmentación se ve pobre, prueba:
  - subir `--iteraciones` (por ejemplo 120 o 200)
  - subir `--hormigas` (por ejemplo 30 o 40)
  - ajustar `--umbrales` según la complejidad de la imagen
- Usa una semilla fija (`--semilla`) para repetir experimentos con resultados comparables.

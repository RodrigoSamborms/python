# Métricas de Calidad de Imagen

Este directorio contiene implementaciones de tres métricas fundamentales para evaluar la calidad de imágenes digitales, comparando una imagen original con una imagen procesada.

---

## 1. MSE (Mean Squared Error - Error Cuadrático Medio)

### Descripción

El Error Cuadrático Medio es una métrica que calcula el promedio de los cuadrados de las diferencias de píxeles entre dos imágenes. Es una métrica simple y fácil de calcular, pero no siempre correlaciona bien con la percepción visual humana.

**Características:**
- Rango: 0 a ∞
- 0 = Imágenes idénticas
- Valores más altos = Mayor diferencia entre imágenes
- No tiene en cuenta la percepción visual humana

### Pseudocódigo

```
Algoritmo Calcular_MSE
    Entrada: Imagen_Original, Imagen_Procesada, Ancho, Alto
    
    Suma_Cuadrados = 0
    
    Para cada píxel (i, j) en la imagen:
        Diferencia = Imagen_Original[i][j] - Imagen_Procesada[i][j]
        Suma_Cuadrados += Diferencia^2
    
    MSE = Suma_Cuadrados / (Ancho * Alto)
    
    Devolver MSE
Fin Algoritmo
```

### Archivos

- **MSE.py**: Implementación del cálculo de MSE
- **MSE_imagen.py**: Programa para cargar imágenes PGM y calcular MSE

### Instrucciones de Uso

#### Opción 1: Usar argumentos de línea de comandos

```powershell
cd c:\Users\sambo\Documents\Programacion\GitHub\python\InteligenciaArtifical1\IntArt\métricas
python MSE_imagen.py --original "imagen_original.pgm" --procesada "imagen_procesada.pgm"
```

#### Opción 2: Modo interactivo

```powershell
cd c:\Users\sambo\Documents\Programacion\GitHub\python\InteligenciaArtifical1\IntArt\métricas
python MSE_imagen.py
```

El programa solicitará las rutas de las imágenes interactivamente.

### Salida Esperada

```
Dimension: 512x512
MSE: 45.123456
RMSE: 6.717391
```

---

## 2. PSNR (Peak Signal-to-Noise Ratio - Relación Señal-Ruido de Pico)

### Descripción

El PSNR es una métrica derivada del MSE que mide la calidad de una imagen en términos de relación entre la potencia de la señal máxima posible y la potencia del ruido que la corrompe. Se expresa en decibelios (dB) y valores más altos indican mejor calidad.

**Características:**
- Rango: 0 a ∞ (típicamente 20 a 50 dB)
- > 50 dB = Excelente
- 40-50 dB = Muy buena
- 30-40 dB = Buena
- 20-30 dB = Aceptable
- < 20 dB = Pobre

### Pseudocódigo

```
Algoritmo Calcular_PSNR
    Entrada: MSE, Valor_Maximo_Pixel (ej. 255)
    
    Si MSE == 0:
        Devolver Infinito  // Las imágenes son idénticas
    
    Numerador = Valor_Maximo_Pixel^2
    Relacion = Numerador / MSE
    PSNR = 10 * Logaritmo10(Relacion)
    
    Devolver PSNR
Fin Algoritmo
```

### Archivos

- **PSNR.py**: Implementación del cálculo de PSNR
- **PSNR_imagen.py**: Programa para cargar imágenes PGM y calcular PSNR y MSE

### Instrucciones de Uso

#### Opción 1: Usar argumentos de línea de comandos

```powershell
cd c:\Users\sambo\Documents\Programacion\GitHub\python\InteligenciaArtifical1\IntArt\métricas
python PSNR_imagen.py --original "imagen_original.pgm" --procesada "imagen_procesada.pgm"
```

#### Opción 2: Modo interactivo

```powershell
cd c:\Users\sambo\Documents\Programacion\GitHub\python\InteligenciaArtifical1\IntArt\métricas
python PSNR_imagen.py
```

### Salida Esperada

```
=== Resultados de comparación de imágenes ===
Dimension: 512x512
Valor máximo de pixel: 255

Métricas de calidad:
  MSE (Error Cuadrático Medio): 45.123456
  RMSE (Raíz del ECM): 6.717391
  PSNR (Peak Signal-to-Noise Ratio): 31.58 dB
  Interpretación: Buena
```

---

## 3. SSIM (Structural Similarity Index - Índice de Similitud Estructural)

### Descripción

El SSIM es una métrica perceptual que mide la similitud estructural entre dos imágenes teniendo en cuenta cómo el sistema visual humano percibe las diferencias. A diferencia de MSE y PSNR, SSIM considera la luminancia, el contraste y la estructura, proporcionando una correlación mucho mejor con la calidad visual percibida.

**Características:**
- Rango: -1 a 1 (típicamente 0 a 1)
- 1.0 = Imágenes idénticas
- 0.95-1.0 = Excelente (casi idénticas)
- 0.80-0.95 = Muy buena
- 0.60-0.80 = Buena
- 0.40-0.60 = Similitud moderada
- 0.20-0.40 = Baja similitud
- < 0.20 = Muy baja o negativa
- < 0 = Correlación negativa

### Pseudocódigo

```
Algoritmo Calcular_SSIM_Global
    Entrada: Imagen_X, Imagen_Y
    Lista_SSIM_Locales = []
    
    // Se divide la imagen en bloques (ventanas)
    Para cada Ventana_x, Ventana_y en Imagen_X, Imagen_Y:
        
        // 1. Calcular estadísticas locales
        Media_x = Promedio(Ventana_x)
        Media_y = Promedio(Ventana_y)
        Varianza_x = Varianza(Ventana_x)
        Varianza_y = Varianza(Ventana_y)
        Covarianza_xy = Covarianza(Ventana_x, Ventana_y)
        
        // 2. Aplicar fórmula de similitud estructural
        Numerador = (2 * Media_x * Media_y + C1) * (2 * Covarianza_xy + C2)
        Denominador = (Media_x^2 + Media_y^2 + C1) * (Varianza_x + Varianza_y + C2)
        
        SSIM_Local = Numerador / Denominador
        Agregar SSIM_Local a Lista_SSIM_Locales
    
    // El SSIM final es el promedio de todos los bloques
    SSIM_Final = Promedio(Lista_SSIM_Locales)
    
    Devolver SSIM_Final
Fin Algoritmo
```

**Donde:**
- C1 = (0.01 * L)²
- C2 = (0.03 * L)²
- L = Valor máximo de píxel (ej. 255)
- Las constantes C1 y C2 estabilizan numéricamente la métrica

### Archivos

- **SSIM.py**: Implementación del cálculo de SSIM con funciones auxiliares
- **SSIM_imagen.py**: Programa para cargar imágenes PGM y calcular SSIM

### Instrucciones de Uso

#### Opción 1: Usar argumentos de línea de comandos (con tamaño de ventana personalizado)

```powershell
cd c:\Users\sambo\Documents\Programacion\GitHub\python\InteligenciaArtifical1\IntArt\métricas
python SSIM_imagen.py --original "imagen_original.pgm" --procesada "imagen_procesada.pgm" --ventana 8
```

#### Opción 2: Usar argumentos con ventana por defecto (8x8)

```powershell
python SSIM_imagen.py --original "imagen_original.pgm" --procesada "imagen_procesada.pgm"
```

#### Opción 3: Modo interactivo

```powershell
python SSIM_imagen.py
```

### Salida Esperada

```
=== Resultados de comparación de imágenes ===
Dimensión: 512x512
Valor máximo de pixel: 255
Tamaño de ventana: 8x8

Métrica de similitud estructural:
  SSIM (Structural Similarity Index): 0.8547
  Interpretación: Muy buena

Escala de referencia:
  1.0000 = Imágenes idénticas
  0.95-1.0 = Excelente (casi idénticas)
  0.80-0.95 = Muy buena
  0.60-0.80 = Buena
  0.40-0.60 = Similitud moderada
  0.20-0.40 = Baja similitud
  < 0.20 = Muy baja o negativa
```

---

## Comparativa de Métricas

| Métrica | Rango | Ventajas | Desventajas |
|---------|-------|----------|------------|
| **MSE** | 0 a ∞ | Simple, rápido, determinístico | No correlaciona bien con percepción visual |
| **PSNR** | 20-50 dB | Derivado del MSE, fácil interpretación | Limitaciones similares a MSE |
| **SSIM** | -1 a 1 | Correlaciona bien con percepción visual | Computacionalmente más costoso |

---

## Requisitos de Formato

Los programas trabajan con imágenes en formato **PGM (Portable Graymap)**:

- **P2**: Imágenes PGM en formato texto
- **P5**: Imágenes PGM en formato binario

Ambas están soportadas automáticamente.

---

## Notas Importantes

- **Sin dependencias externas**: Todos los programas utilizan solo bibliotecas estándar de Python
- **Compatibilidad**: Los programas funcionan con Python 3.x
- **Imágenes idénticas**: 
  - MSE retorna 0
  - PSNR retorna Infinito
  - SSIM retorna 1.0
- **Tamaño de ventana SSIM**: El programa ajusta automáticamente si es mayor que las dimensiones de la imagen

---

## Ejemplo de Uso Completo

```powershell
# Ir al directorio de métricas
cd c:\Users\sambo\Documents\Programacion\GitHub\python\InteligenciaArtifical1\IntArt\métricas

# Calcular MSE
python MSE_imagen.py --original "original.pgm" --procesada "procesada.pgm"

# Calcular PSNR
python PSNR_imagen.py --original "original.pgm" --procesada "procesada.pgm"

# Calcular SSIM
python SSIM_imagen.py --original "original.pgm" --procesada "procesada.pgm" --ventana 8
```

---

## Referencias

- **MSE**: Se utiliza ampliamente en procesamiento de imágenes como referencia base
- **PSNR**: Métrica estándar en compresión de imágenes (JPEG, H.264, etc.)
- **SSIM**: Propuesto por Wang et al. (2004), mejor correlación con calidad visual percibida


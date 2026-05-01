# CLAHE + Algoritmo del Cuco en Python

## 1. Objetivo
En [Cuco.py](Cuco.py) se implementa un flujo de mejora de contraste en imagenes:

1. Cargar imagen de entrada desde linea de comandos.
2. Convertir a escala de grises.
3. Optimizar parametros de CLAHE con Cuckoo Search.
4. Aplicar CLAHE con los parametros optimos.
5. Evaluar antes/despues con metricas.

## 2. Rol de cada parte
- CLAHE: tecnica de mejora de contraste local.
- Cuckoo Search: optimizador que busca automaticamente los mejores parametros de CLAHE.
- Funcion objetivo: criterio que el algoritmo del cuco maximiza para decidir que parametros son mejores.

## 3. Funcion objetivo usada
La implementacion utiliza la funcion:

$$
J = w_1\hat{H} + w_2\hat{\sigma} + w_3\hat{E} - w_4\hat{N} - w_5\widehat{\Delta\mu}
$$

Donde:
- $\hat{H}$: entropia normalizada.
- $\hat{\sigma}$: desviacion estandar normalizada (contraste global).
- $\hat{E}$: energia de bordes normalizada.
- $\hat{N}$: estimacion de ruido normalizada.
- $\widehat{\Delta\mu}$: cambio de brillo medio normalizado respecto a la imagen original.

## 4. Parametros que optimiza el cuco
Cada nido representa un conjunto de parametros CLAHE:

1. clipLimit
2. tileGridSizeX
3. tileGridSizeY

## 5. Metricas reportadas
El script reporta:

1. Entropia antes y despues.
2. MSE, RMSE, PSNR y SSIM, reutilizando modulos de [métricas](métricas) cuando estan disponibles.

## 6. Ejecucion desde linea de comandos
Desde la raiz del proyecto:

```powershell
python InteligenciaArtifical1/IntArt/Cuco.py --input InteligenciaArtifical1/IntArt/casa.png --output InteligenciaArtifical1/IntArt/casa_clahe_cuco.png
```

Tambien puedes entrar a la carpeta y ejecutar:

```powershell
cd InteligenciaArtifical1/IntArt
python Cuco.py --input casa.png --output casa_clahe_cuco.png
```

## 7. Comando recomendado (primera corrida)
```powershell
python InteligenciaArtifical1/IntArt/Cuco.py --input InteligenciaArtifical1/IntArt/casa.png --output InteligenciaArtifical1/IntArt/casa_clahe_cuco.png --nests 25 --iterations 60 --pa 0.25 --clip-min 1 --clip-max 10 --tile-min 4 --tile-max 16 --w1 0.35 --w2 0.25 --w3 0.25 --w4 0.10 --w5 0.05
```

## 8. Argumentos principales
- --input: ruta de imagen de entrada (requerido).
- --output: ruta de imagen de salida.
- --nests: numero de nidos.
- --iterations: numero de iteraciones.
- --pa: probabilidad de abandono de nidos.
- --alpha: tamano de paso de Levy.
- --beta: parametro beta del vuelo de Levy.
- --clip-min, --clip-max: limites de clipLimit.
- --tile-min, --tile-max: limites de tamano de grilla para CLAHE.
- --w1, --w2, --w3, --w4, --w5: pesos de la funcion objetivo.
- --ssim-window: ventana para SSIM.
- --quiet: oculta progreso por iteraciones.

## 9. Salida esperada
Al terminar, el programa imprime:

1. Mejor valor de la funcion objetivo J.
2. Parametros optimos de CLAHE.
3. Entropia antes/despues.
4. MSE, RMSE, PSNR y SSIM (si las metricas locales se cargan correctamente).

Y guarda la imagen mejorada en la ruta indicada por --output.

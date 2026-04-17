# Guia de ejecucion de Nitidez.py

Este documento explica como lanzar el programa [Nitidez.py](Nitidez.py), que realiza:

1. Suavizado gaussiano.
2. Afilado laplaciano sobre la imagen suavizada.
3. Guardado de imagen intermedia y resultado final.

## Requisitos

- Python 3.10 o superior (recomendado).
- Paquetes:
  - numpy
  - pillow

Instalacion rapida:

```powershell
pip install numpy pillow
```

## Parametros disponibles

- `--input` Ruta de la imagen de entrada. Obligatorio.
- `--sigma` Intensidad del suavizado gaussiano. Opcional, por defecto: `1.5`.
- `--alpha` Intensidad del afilado laplaciano. Opcional, por defecto: `1.0`.
- `--gaussian-output` Ruta para guardar la imagen intermedia gaussiana. Opcional.
- `--output` Ruta para guardar la imagen final afilada. Opcional.

Si no defines salidas, el script crea automaticamente:

- Intermedia: `*_gauss.ext`
- Final: `*_gauss_lap.ext`

## Ejecucion desde la carpeta IntArt

Si tu terminal esta en [InteligenciaArtifical1/IntArt](.):

```powershell
python .\Nitidez.py --input .\Diana_Ruido.bmp --sigma 1.5 --alpha 1.0
```

## Ejecucion desde la raiz del repositorio

Si tu terminal esta en [python](../../):

```powershell
python .\InteligenciaArtifical1\IntArt\Nitidez.py --input .\InteligenciaArtifical1\IntArt\Diana_Ruido.bmp --sigma 1.5 --alpha 1.0
```

## Ejemplo con salida personalizada

```powershell
python .\Nitidez.py --input .\Diana_Ruido.bmp --sigma 1.5 --alpha 1.0 --gaussian-output .\mi_gauss.bmp --output .\mi_final.bmp
```

## Interpretacion de parametros clave

- `sigma`: controla cuanto se suaviza la imagen.
  - Menor valor: menos suavizado.
  - Mayor valor: mas suavizado.

- `alpha`: controla la fuerza del afilado laplaciano.
  - `alpha = 0`: no afila.
  - Valores entre `0.3` y `1.0`: afilado moderado.
  - Valores altos: puede introducir halos o amplificar ruido.

## Archivos esperados

Con este comando:

```powershell
python .\Nitidez.py --input .\Diana_Ruido.bmp --sigma 1.5 --alpha 1.0
```

Se generan:

- [Diana_Ruido_gauss.bmp](Diana_Ruido_gauss.bmp)
- [Diana_Ruido_gauss_lap.bmp](Diana_Ruido_gauss_lap.bmp)

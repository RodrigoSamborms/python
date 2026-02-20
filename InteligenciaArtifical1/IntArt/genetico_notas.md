# Notas

## Imagen con ruido (Diana.bmp)

Se genero una version con ruido gaussiano usando el script `agregar_ruido.py`.

Comando utilizado:

```bash
python agregar_ruido.py --input Diana.bmp --output Diana_Ruido.bmp --sigma 25
```

Resultado:
- Archivo de salida: `Diana_Ruido.bmp`
- Tipo de ruido: gaussiano
- Sigma: 25

## Suavizado con algoritmo genetico (Diana_Ruido.bmp)

Ejecucion por defecto (equivalente a los parametros usados para generar
`Diana_Suavisado.bmp`):

```bash
python genetico_practica.py
```

Comando con opciones (mismos valores por defecto):

```bash
python genetico_practica.py --input-original Diana.bmp --input-noisy Diana_Ruido.bmp --output Diana_Suavisado.bmp --pop-size 30 --sigma-min 0.5 --sigma-max 5.0 --generations 40 --mutation-rate 0.1
```

Resultado:
- Archivo de salida: `Diana_Suavisado.bmp`
- Criterio: PSNR maximo vs `Diana.bmp`
- Rango sigma: 0.5 a 5.0

# Algoritmo del Cuco (Cuckoo Search) en Python

## 1. Idea principal
Cuckoo Search es un algoritmo metaheuristico de optimizacion inspirado en el comportamiento de reproduccion del cuco.

En este contexto:
- Cada nido representa una solucion candidata x.
- La calidad del nido se mide con una funcion objetivo f(x) (fitness).
- Queremos minimizar f(x).

El algoritmo combina:
- Exploracion global mediante vuelos de Levy.
- Seleccion de mejores soluciones.
- Reemplazo de soluciones peores (abandono de nidos).

## 2. Objetivo del programa
En [Cuco.py](Cuco.py) se implementa Cuckoo Search para minimizar funciones en R^d:

$$
\min f(x),\quad x=(x_1, x_2, ..., x_d)
$$

La nueva solucion se construye con:

$$
x_{nuevo} = x_i + \alpha \cdot L(\beta)
$$

Donde:
- $\alpha$ controla el tamano del paso.
- $L(\beta)$ es un paso aleatorio tipo Levy.

## 3. Pseudocodigo implementado
```text
Inicio
    Objetivo: Minimizar f(x), donde x = (x1, ..., xd)
    Generar una poblacion inicial de n nidos anfitriones (soluciones xi)

    Mientras (t < Iteraciones_Maximas)

        1. Obtener un cuco aleatorio (nueva solucion) mediante vuelo de Levy:
           x_nuevo = x_i + alpha * L(beta)

        2. Evaluar su calidad (fitness) F_nuevo = f(x_nuevo)

        3. Elegir un nido j al azar entre los n nidos

        4. Si (F_nuevo < F_j)  // minimizacion
              Reemplazar el nido j por x_nuevo
           Fin Si

        5. Abandono de nidos:
           Una fraccion pa de los peores nidos se abandona.
           Esos nidos se reconstruyen en nuevas posiciones con vuelos de Levy.

        6. Mantener las mejores soluciones

        7. Clasificar soluciones y actualizar la mejor actual (G-Best)

    Fin Mientras

    Mostrar el mejor nido (solucion optima encontrada)
Fin
```

Nota:
- En minimizacion, una solucion mejor cumple $F_{nuevo} < F_j$.

## 4. Funciones objetivo disponibles
El programa permite elegir distintas funciones objetivo desde la linea de comandos:

1. Sphere
2. Rastrigin
3. Rosenbrock
4. Ackley

Tambien se puede usar all para ejecutar todas en una sola corrida.

## 5. Estructura general del codigo
En [Cuco.py](Cuco.py) se incluyen:

1. Funciones objetivo: sphere, rastrigin, rosenbrock, ackley.
2. Generador de paso Levy con el metodo de Mantegna.
3. Clase CuckooSearch con:
   - Inicializacion de nidos.
   - Generacion de nuevos cucos por Levy.
   - Reemplazo por calidad.
   - Abandono de peores nidos.
   - Actualizacion de mejor global (G-Best).
4. Interfaz por argumentos para seleccionar funcion y parametros.

## 6. Parametros principales
- n_nests: numero de nidos.
- dimension: dimension del vector solucion.
- max_iterations: numero maximo de iteraciones.
- alpha: escala del paso de Levy.
- beta: parametro de Levy (tipico 1.5).
- pa: fraccion de nidos que se abandonan.
- seed: semilla aleatoria para reproducibilidad.

## 7. Instrucciones de ejecucion
Desde la raiz del proyecto:

```powershell
cd InteligenciaArtifical1/IntArt
python Cuco.py --objective all --quiet
```

Si tu entorno usa python3:

```powershell
python3 Cuco.py --objective all --quiet
```

## 8. Ejemplos de uso
Ejecutar todas las funciones objetivo:

```powershell
python Cuco.py --objective all --quiet
```

Ejecutar solo Sphere:

```powershell
python Cuco.py --objective sphere --iterations 120 --dimension 5
```

Ejecutar solo Rastrigin:

```powershell
python Cuco.py --objective rastrigin --iterations 200 --nests 30 --dimension 10
```

Ejecutar solo Rosenbrock:

```powershell
python Cuco.py --objective rosenbrock --iterations 200 --dimension 5
```

Ejecutar solo Ackley:

```powershell
python Cuco.py --objective ackley --iterations 150 --dimension 10
```

## 9. Que muestra la salida
Para cada funcion objetivo seleccionada, el programa imprime:

1. Nombre de la funcion.
2. Mejor nido encontrado (x*).
3. Mejor fitness encontrado f(x*).

Si no se usa --quiet, tambien muestra progreso por iteraciones.

## 10. Recomendaciones para experimentar
1. Aumentar iteraciones para mejorar calidad de solucion.
2. Probar diferentes valores de alpha y pa.
3. Comparar desempeno entre funciones objetivo.
4. Incrementar dimension para observar mayor dificultad del problema.

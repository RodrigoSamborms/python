import numpy as np

def funcion_f(x_vec):
    x, y = x_vec[0], x_vec[1]
    return 0.5 * (3*x**2 + 2*x*y + 2*y**2) - 5*x - 3*y

def gradiente_f(x_vec):
    x, y = x_vec[0], x_vec[1]
    # Resultado obtenido en Maxima: [3x + y - 5, x + 2y - 3]
    return np.array([3*x + y - 5, x + 2*y - 3])

def hessiana_f(x_vec):
    # Resultado obtenido en Maxima: [[3, 1], [1, 2]]
    return np.array([[3.0, 1.0], 
                     [1.0, 2.0]])

def metodo_newton(punto_inicial, tolerancia=1e-6, max_iter=10):
    x_k = np.array(punto_inicial, dtype=float)
    
    print(f"{'Iteración':<10} | {'Punto (x, y)':<25} | {'Valor f(x,y)':<15}")
    print("-" * 55)
    
    for i in range(max_iter):
        valor_actual = funcion_f(x_k)
        print(f"{i:<10} | {str(x_k):<25} | {valor_actual:<15.6f}")
        
        grad = gradiente_f(x_k)
        
        # Condición de parada: si el gradiente es casi cero
        if np.linalg.norm(grad) < tolerancia:
            print("-" * 55)
            print(f"Convergencia alcanzada en la iteración {i}.")
            break
            
        H = hessiana_f(x_k)
        
        # Inversa de la Hessiana multiplicada por el gradiente
        # x_{k+1} = x_k - H^-1 * grad
        paso_newton = np.linalg.solve(H, grad) # Más eficiente que invertir la matriz directamente
        x_k = x_k - paso_newton
        
    return x_k

# Ejecución
punto_optimo = metodo_newton(punto_inicial=[0, 0])
print(f"El mínimo global se encuentra en: {punto_optimo}")
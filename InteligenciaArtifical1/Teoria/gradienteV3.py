import numpy as np

def optimizar_newton_2d(gradiente, hessiana, punto_inicial, tol=1e-8, max_iter=50):
    xy = np.array(punto_inicial, dtype=float)
    
    for i in range(max_iter):
        g = gradiente(xy)
        h = hessiana(xy)
        
        # Resolvemos el sistema H * paso = g (es más estable que invertir la matriz)
        try:
            paso = np.linalg.solve(h, g)
        except np.linalg.LinAlgError:
            print("La matriz Hessiana es singular. No se puede continuar.")
            break
            
        xy_nuevo = xy - paso
        
        print(f"Iter {i+1}: Punto {xy_nuevo}, Norma del paso: {np.linalg.norm(paso):.6e}")
        
        if np.linalg.norm(paso) < tol:
            return xy_nuevo
            
        xy = xy_nuevo
        
    return xy

# --- Ejemplo: f(x, y) = x^2 + y^2 ---
# Gradiente: [2x, 2y]
def mi_gradiente(p):
    x, y = p
    return np.array([2*x, 2*y])

# Hessiana: [[2, 0], [0, 2]]
def mi_hessiana(p):
    return np.array([[2.0, 0.0], [0.0, 2.0]])

punto_min = optimizar_newton_2d(mi_gradiente, mi_hessiana, punto_inicial=[5, 10])
print(f"\nMínimo encontrado en: {punto_min}")
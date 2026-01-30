import matplotlib.pyplot as plt
import numpy as np
def f(x): #este
    return 5*np.cos(x)-np.cos(2*x)
def grad_f(x): #tambien este
    return -5*np.sin(x)+5*np.sin(5*x)
#algoritmo de gradiente descendente
def gradiente_descent(grad, start, lerning_rate, num_iter):
    x = start
    history=[x]
    for i in range(num_iter):
        x = x - lerning_rate*grad(x)
        history.append(x)
    return x, history
#start = (np.pi/2+0-1)
start=(np.pi/3)
learning_rate=0.1
num_iter=50

x_min, history = gradiente_descent(grad_f, start, learning_rate, num_iter)
print("El valor minimo encontrado de x es: {x_min}")
history=np.array(history)

x_vals = np.linspace(-3, 3, 1000)
y_vals = f(x_vals) #np.linspace(-30, 30, 100)
plt.plot(x_vals, y_vals, label='f(x)=x^2')
plt.plot(history, f(history), 'ro-', label='trayectoria de x')
plt.legend()
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('gradiente descendiente en funcionamiento')
plt.show()
##buscar la respuesta a porque se estanca el algoritmo en ciertos puntos
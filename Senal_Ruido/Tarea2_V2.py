#-----------PROGRAMA 2-----------
#Este programa muestra funciones senos
import numpy as np
import matplotlib.pyplot as plt
import math
pi = math.pi

#+++++ Defininimos las funciones +++++
def g(t,A = 1,f = 1/(2*pi),o =0):
    return A*np.sin((2*pi*f)*t + o)#A*np.sin(w*t + o)
def r1(t,A = 1, f = 1/(2*pi), o=0):
    return (A/6)*np.sin(8*(2*pi*f)*t + o)
def r2(t,A  = 1, f = 1/(2*pi), o = 0):
    return (A/10)*np.sin(16*(2*pi*f)*t + o)


#Valores constantes calculados para modificar la grafica

Vfrec1 = 1
Vfrec2 = 1
Vfrec3 = 1 

Periodos = 1*2 #Numero de periodos a mostrar
#Definimos los rangos de valores para los ejes X y Y
xlist = np.arange(0, Periodos*(2*pi), 0.01) #se indican cuantos peridos debemos mostrar

#diferentes funciones
try:
    Amplitud = float (input ("Indique la amplitud de la funcion: "))
    if (Amplitud <=0):
        Bandera = False
        print ("La amplitud debe ser mayor o igual a 1 por lo menos")
    else:
        Frecuencia = float (input("Ingrese la frecuencia de la funcion: "))
        Vfrec1 = Vfrec2 = Vfrec3 = Frecuencia
        if (Frecuencia <=0):
            print("La frecuencia debe ser mayor o igual a 1 al menos")
            Bandera = False
    seleccion = int(input("Seleccione ejercicio (1-8): "))
except ValueError as err:
    print(err)
    Bandera = False

frec1 = (1/(2*pi))*Vfrec1
frec2 = (1/(2*pi))*Vfrec2
frec3 = (1/(2*pi))*Vfrec3
grafica = True
bandera = True

match seleccion:
    case 1: 
        print("Ejercicio 1")
        y1list = g(xlist, Amplitud, frec1) #funcion: 1*seno(1*t + 0)
    case 2: 
        print("Ejercicio 2")
        Periodos = 1
        xlist = np.arange(0, Periodos*(2*pi), 0.01)
        y2list = r1(xlist, Amplitud/8, frec2) #funcion: 1*seno(1*t + 0)
        y3list = r2(xlist, Amplitud/16, frec3) #funcion: 1*seno(1*t + 0)
        grafica = False
    case 3: 
        print("Ejercicio 3")
        y1list = g(xlist, Amplitud, frec1) + r1(xlist, 1, frec2) #funcion: 1*seno(1*t + 0)
    case 4: 
        print("Ejercicio 4")
        y1list = g(xlist, Amplitud, frec1) + r2(xlist, 1, frec3) #funcion: 1*seno(1*t + 0)
    case 5: 
        print("Ejercicio 5")
        y1list = g(xlist, Amplitud, frec1) * r1(xlist, 1, frec2) + r2(xlist, 1, frec3) #funcion: 1*seno(1*t + 0)
    case 6: 
        print("Ejercicio 6")
        y1list = g(xlist, Amplitud, frec1) * r2(xlist, 1, frec3)  #funcion: 1*seno(1*t + 0)
    case 7: 
        print("Ejercicio 7")
        y1list = g(xlist, Amplitud, frec1) + r1(xlist, 1, frec2) + pow(r2(xlist, 1, frec3),2) #funcion: 1*seno(1*t + 0)
    case 8: 
        print("Ejercicio 8")
        y1list = pow(g(xlist, Amplitud, frec1),2) + pow(r1(xlist, 1, frec2),2) + pow(r2(xlist, 1, frec3),2) #funcion: 1*seno(1*t + 0)
    case _:
        print("numero diferente de 1 a 8")
        bandera = False
        
#y1list = g(xlist, Amplitud, frec1) + r2(xlist, 1, frec3) #funcion: 1*seno(1*t + 0)

plt.figure(num=0, dpi=140)


if (grafica == True and bandera == True):
    plt.plot(xlist, y1list, label = "g(x)")
    plt.title("Funcion Seno")
    plt.xlabel("Pi Radianes")
    plt.ylabel("Valores de la Función")
    plt.legend()
    plt.show()
else:
    if (bandera == True):
        plt.plot(xlist, y2list, label = "r1(x)")
        plt.plot(xlist, y3list, label = "r2(x)")
        plt.title("Funcion Seno")
        plt.xlabel("Pi Radianes")
        plt.ylabel("Valores de la Función")
        plt.legend()
        plt.show()
    







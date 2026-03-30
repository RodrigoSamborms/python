#Write your code here
class Calculator:
    def __init__(self): #creamos el constructor de la clase
        pass

    def power(self, n, p): #creamos el metodo power
        if n < 0 or p < 0: #El metodo levanta una excepcion
            raise Exception("n and p should be non-negative") #Si n o p son negativos envia el mensaje en la varible e
        else:
            return n**p #Si n y p son positivos, retorna la potencia

myCalculator=Calculator() #Creamos un objeto de la clase Calculator
T=int(input())
for i in range(T):
    n,p = map(int, input().split())
    try:
        ans=myCalculator.power(n,p) #llamamos al metodo power(n,p)
        print(ans) #intenta imprimir el resultado, en caso de que se levante una excepcion
    except Exception as e: #esta se maneja por Exception as e variable donde se regreso el menaje de error
        print(e)   
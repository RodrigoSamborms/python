class AdvancedArithmetic(object):
    def __init__(self):
        pass        #Creamos el constructor de la clase padre
    def divisorSum(n):
        raise NotImplementedError   #metodo abstracto, se espera que la clase hija lo implemente

class Calculator(AdvancedArithmetic):
    def __init__(self):
        super().__init__() #la clase hija llama al constructor de la clase padre
    def divisorSum(self, n):
        #encontrar los divisores de n y guardarlos en una lista
        divisors = []
        for i in range (n, 0, -1):
            if n % i == 0:
                divisors.append(i)
        #for i in range (len(divisors)):
        #    print (divisors[i])
        #print (sum(divisors))
        return sum(divisors)



n = int(input())
my_calculator = Calculator()
s = my_calculator.divisorSum(n)
print("I implemented: " + type(my_calculator).__bases__[0].__name__)
print(s)
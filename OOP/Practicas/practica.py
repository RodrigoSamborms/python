# Variables globales
PREANALISIS = None
posicion = 0
cadena = ""

def obtener_siguiente_token():
    """Obtiene el siguiente token de la cadena"""
    global PREANALISIS, posicion
    if posicion < len(cadena):
        PREANALISIS = cadena[posicion]
    else:
        PREANALISIS = None  # Fin de cadena

def coincidir(token_esperado):
    """Verifica que el token actual coincida con el esperado y avanza"""
    global PREANALISIS, posicion
    if PREANALISIS == token_esperado:
        posicion += 1
        obtener_siguiente_token()
    else:
        raise SyntaxError(f"Cadena no pertenece al lenguaje")

def Lista():
    digito()
    Resto_lista()

def Resto_lista():
    if PREANALISIS == '+':
        coincidir('+')
        digito()
        Resto_lista()
    elif PREANALISIS == '-':
        coincidir('-')
        digito()
        Resto_lista()
    else:
        pass #cadena vacia para remarcar

def digito():
    if PREANALISIS == '0':
        coincidir('0')
    elif PREANALISIS == '1':
        coincidir('1')
    elif PREANALISIS == '2':
        coincidir('2')
    elif PREANALISIS == '3':
        coincidir('3')
    elif PREANALISIS == '4':
        coincidir('4')
    elif PREANALISIS == '5':
        coincidir('5')
    elif PREANALISIS == '6':
        coincidir('6')
    elif PREANALISIS == '7':
        coincidir('7')
    elif PREANALISIS == '8':
        coincidir('8')
    elif PREANALISIS == '9':
        coincidir('9')
    else:
        raise SyntaxError(f"Cadena no pertenece al lenguaje")

def analizar(entrada):
    """Función principal del analizador"""
    global PREANALISIS, posicion, cadena
    
    cadena = entrada
    posicion = 0
    PREANALISIS = None
    
    obtener_siguiente_token()
    
    try:
        Lista()
        
        # Verificar que se consumió toda la entrada
        if PREANALISIS is not None:
            raise SyntaxError(f"Cadena no pertenece al lenguaje")
        
        print("Cadena pertenece al lenguaje")
    except SyntaxError:
        print("Cadena no pertenece al lenguaje")

# Entrada del usuario
if __name__ == "__main__":
    cadena_usuario = input("Ingrese la cadena a analizar: ")
    analizar(cadena_usuario)

import sys

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
        encontrado = PREANALISIS if PREANALISIS is not None else "fin de cadena"
        raise SyntaxError(
            f"Error de sintaxis en posicion {posicion + 1}: se esperaba '{token_esperado}' y se encontro '{encontrado}'"
        )

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
    elif PREANALISIS == '*':
        coincidir('*')
        digito()
        Resto_lista()
    elif PREANALISIS == '/':
        coincidir('/')
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
        encontrado = PREANALISIS if PREANALISIS is not None else "fin de cadena"
        raise SyntaxError(
            f"Error de sintaxis en posicion {posicion + 1}: se esperaba un digito y se encontro '{encontrado}'"
        )

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
            raise SyntaxError(
                f"Error de sintaxis en posicion {posicion + 1}: token inesperado '{PREANALISIS}'"
            )
        
        return True, "Programa fuente valido de acuerdo a la gramatica"
    except SyntaxError as error:
        return False, str(error)


def cargar_fuente(ruta_archivo):
    """Lee el archivo fuente y elimina espacios en blanco para el analisis."""
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
    return "".join(contenido.split())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python traductor4.py <archivo_fuente>")
        raise SystemExit(1)

    ruta = sys.argv[1]

    try:
        fuente = cargar_fuente(ruta)
    except FileNotFoundError:
        print(f"Error: no se encontro el archivo '{ruta}'.")
        raise SystemExit(1)
    except OSError as error:
        print(f"Error al leer el archivo fuente: {error}")
        raise SystemExit(1)

    if not fuente:
        print("Error: el archivo fuente esta vacio.")
        raise SystemExit(1)

    es_valido, mensaje = analizar(fuente)
    if es_valido:
        print(mensaje)
    else:
        print(f"Programa fuente no valido: {mensaje}")
        raise SystemExit(1)
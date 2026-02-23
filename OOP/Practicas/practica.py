import re
class AnalizadorSintactico:
    def _init_(self, texto):
        # Tokenizador simple para separar números y operadores
        self.tokens = re.findall(r'\d+|[+\-*/()]', texto)
        self.pos = 0
        self.token_actual = self.tokens[0] if self.tokens else None

    def error(self):
        raise Exception(f"Error de sintaxis en el token: '{self.token_actual}'")

    def consumir(self, token_esperado):
        if self.token_actual == token_esperado:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.token_actual = self.tokens[self.pos]
            else:
                self.token_actual = None # Fin de la cadena
        else:
            self.error()

    # --- Funciones de la Gramática ---

    def expr(self):
        # expr -> term resto_expr
        self.term()
        self.resto_expr()

    def resto_expr(self):
        # resto_expr -> + term resto_expr | - term resto_expr | epsilon
        if self.token_actual == '+':
            self.consumir('+')
            self.term()
            self.resto_expr()
        elif self.token_actual == '-':
            self.consumir('-')
            self.term()
            self.resto_expr()
        else:
            pass # Epsilon (no hacer nada)

    def term(self):
        # term -> factor resto_term
        self.factor()
        self.resto_term()

    def resto_term(self):
        # resto_term -> * factor resto_term | / factor resto_term | epsilon
        if self.token_actual == '*':
            self.consumir('*')
            self.factor()
            self.resto_term()
        elif self.token_actual == '/':
            self.consumir('/')
            self.factor()
            self.resto_term()
        else:
            pass # Epsilon

    def factor(self):
        # factor -> ( expr ) | digito
        if self.token_actual == '(':
            self.consumir('(')
            self.expr()
            self.consumir(')')
        elif self.token_actual and self.token_actual.isdigit():
            self.consumir(self.token_actual)
        else:
            self.error()

# --- Prueba ---
entrada = "3 + 5 * ( 2 - 8 )"
parser = AnalizadorSintactico(entrada)

try:
    parser.expr()
    if parser.token_actual is None:
        print("¡Éxito! La cadena es sintácticamente correcta.")
    else:
        print("Error: Se esperaba el fin de la cadena.")
except Exception as e:
    print(e)


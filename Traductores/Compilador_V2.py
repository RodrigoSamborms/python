
"""Compilador: parser para la gramática solicitada y generación
de código de tres direcciones (TAC).

Uso:
 - El programa analiza una entrada que sigue la gramática pedida
     (palabras clave en español: begin, end, entero, real, if, else,
     while, endwhile). La entrada puede pasarse por stdin o escribirse
     tras el prompt.

Formato de ejecución (desde la raíz del repo):

```bash
python Traductores/Compilador.py          # luego pegar o redirigir el programa
echo "begin entero x; x := 1; end" | python Traductores/Compilador.py
```

Qué hace:
 - Realiza un análisis léxico y sintáctico (parser recursivo-descendente)
     según la gramática proporcionada en la petición.
 - Genera código de tres direcciones (TAC) en formato legible. Ejemplo
     de instrucciones generadas:
         - `# decl x : entero`  -> declaración de variable
         - `t1 := x + 2`        -> operación aritmética en una temporal
         - `x := t1`           -> asignación final
         - `label L1`, `goto L1`, `if_false a < b goto L2` -> control

Notas y limitaciones:
 - El analizador distingue palabras clave por su texto, no hace comprobación
     estricta de tipos más allá de registrar `entero`/`real` en un diccionario.
 - La entrada debe estar bien espaciada entre tokens para evitar ambigüedades
     (ej.: `x := ( x + 2 )` o `x:=5` funcionan por el lexer).
 - Soporta expresiones aritméticas con precedencia y paréntesis.

Ejemplo de programa de una sola línea aceptado:
    begin entero x; real y; x := 5; y := ( x + 2 ); end

Salida esperada (TAC):
    # decl x : entero
    # decl y : real
    x := 5
    t1 := x + 2
    y := t1

"""

import re
import sys
from pathlib import Path


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"


class Lexer:
    token_specification = [
        ('NUMBER',   r'\d+(?:\.\d+)?'),
        ('ID',       r'[A-Za-z][A-Za-z0-9]*'),
        ('LE',       r'<='),
        ('GE',       r'>='),
        ('NE',       r'<>'),
        ('ASSIGN',   r':='),
        ('EQ',       r'='),
        ('LT',       r'<'),
        ('GT',       r'>'),
        ('PLUS',     r'\+'),
        ('MINUS',    r'-'),
        ('TIMES',    r'\*'),
        ('DIV',      r'/'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('COMMA',    r','),
        ('SEMI',     r';'),
        ('DOT',      r'\.'),
        ('SKIP',     r'[ \t\r\n]+'),
        ('MISMATCH', r'.'),
    ]

    def __init__(self, text):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        self.get_token = re.compile(tok_regex).match
        self.text = text
        self.pos = 0
        self.mo = self.get_token(text)

    def tokens(self):
        while self.mo is not None:
            kind = self.mo.lastgroup
            value = self.mo.group()
            if kind == 'NUMBER':
                yield Token('NUMBER', value)
            elif kind == 'ID':
                yield Token('ID', value)
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected char: {value!r}')
            else:
                yield Token(kind, value)
            self.pos = self.mo.end()
            self.mo = self.get_token(self.text, self.pos)
        yield Token('EOF', '')


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.tok = None
        self.nexttok()
        self.temp_count = 0
        self.label_count = 0
        self.code = []
        self.symbols = {}  # name -> type

    def nexttok(self):
        self.tok = next(self.tokens)

    def error(self, msg='Cadena no pertenece al lenguaje'):
        raise SyntaxError(msg)

    def eat(self, tipo):
        if self.tok.tipo == tipo or (tipo == 'ID' and self.tok.tipo == 'ID'):
            val = self.tok.valor
            self.nexttok()
            return val
        else:
            self.error()

    def new_temp(self):
        self.temp_count += 1
        return f't{self.temp_count}'

    def new_label(self):
        self.label_count += 1
        return f'L{self.label_count}'

    def emit(self, instr):
        self.code.append(instr)

    # Grammar entry
    def parse_programa(self):
        if self.tok.tipo == 'ID' and self.tok.valor.lower() == 'begin':
            self.nexttok()
            self.parse_declaraciones()
            self.parse_ordenes()
            if self.tok.tipo == 'ID' and self.tok.valor.lower() == 'end':
                self.nexttok()
                if self.tok.tipo != 'EOF':
                    self.error()
                return
        self.error()

    # declaraciones -> declaración ; sig_declaraciónes
    def parse_declaraciones(self):
        # allow empty declarations
        if self.tok.tipo == 'ID' and self.tok.valor.lower() in ('entero', 'real'):
            self.parse_declaracion()
            if self.tok.tipo == 'SEMI':
                self.nexttok()
                self.parse_sig_declaraciones()
            else:
                self.error()

    def parse_sig_declaraciones(self):
        while self.tok.tipo == 'ID' and self.tok.valor.lower() in ('entero', 'real'):
            self.parse_declaracion()
            if self.tok.tipo == 'SEMI':
                self.nexttok()
            else:
                self.error()

    # declaración -> tipo lista_variables
    def parse_declaracion(self):
        tipo = self.parse_tipo()
        vars = self.parse_lista_variables()
        for v in vars:
            self.symbols[v] = tipo
            self.emit(f'# decl {v} : {tipo}')

    def parse_tipo(self):
        if self.tok.tipo == 'ID' and self.tok.valor.lower() in ('entero', 'real'):
            t = self.tok.valor.lower()
            self.nexttok()
            return t
        else:
            self.error()

    # lista_variables -> identificador ( , lista_variables )?
    def parse_lista_variables(self):
        vars = []
        if self.tok.tipo == 'ID':
            name = self.eat('ID')
            vars.append(name)
            while self.tok.tipo == 'COMMA':
                self.nexttok()
                if self.tok.tipo == 'ID':
                    name = self.eat('ID')
                    vars.append(name)
                else:
                    self.error()
            return vars
        else:
            self.error()

    # órdenes -> orden ; sig_órdenes
    def parse_ordenes(self):
        if self.tok.tipo == 'ID' and self.tok.valor.lower() in ('if', 'while'):
            # could be statement starting with id too (assignment)
            pass
        # require at least one order
        self.parse_orden()
        if self.tok.tipo == 'SEMI':
            self.nexttok()
            self.parse_sig_ordenes()
        else:
            self.error()

    def parse_sig_ordenes(self):
        while self.tok.tipo != 'EOF' and not (self.tok.tipo == 'ID' and self.tok.valor.lower() == 'end') and not (self.tok.tipo == 'ID' and self.tok.valor.lower() == 'else') and not (self.tok.tipo == 'ID' and self.tok.valor.lower() == 'endwhile'):
            self.parse_orden()
            if self.tok.tipo == 'SEMI':
                self.nexttok()
            else:
                break

    def parse_orden(self):
        if self.tok.tipo == 'ID':
            v = self.tok.valor.lower()
            if v == 'if':
                self.parse_condicion()
            elif v == 'while':
                self.parse_bucle_while()
            else:
                self.parse_asignar()
        else:
            self.error()

    # condición -> if ( comparación ) órdenes sig_condición
    def parse_condicion(self):
        # assume current token is 'if'
        self.nexttok()
        if self.tok.tipo != 'LPAREN':
            self.error()
        self.nexttok()
        left, comp_op, right = self.parse_comparacion()
        if self.tok.tipo != 'RPAREN':
            self.error()
        self.nexttok()

        Lelse = self.new_label()
        Lend = self.new_label()
        # Emit conditional jump: if not (left op right) goto Lelse
        self.emit(f'if_false {left} {comp_op} {right} goto {Lelse}')

        # then block
        self.parse_ordenes()

        # sig_condición -> end | else órdenes end
        if self.tok.tipo == 'ID' and self.tok.valor.lower() == 'end':
            self.nexttok()
            # continue
        elif self.tok.tipo == 'ID' and self.tok.valor.lower() == 'else':
            self.nexttok()
            # jump to end after then
            self.emit(f'goto {Lend}')
            self.emit(f'label {Lelse}')
            self.parse_ordenes()
            if self.tok.tipo == 'ID' and self.tok.valor.lower() == 'end':
                self.nexttok()
            else:
                # allow 'end' as token value
                if self.tok.tipo == 'ID' and self.tok.valor.lower() == 'end':
                    self.nexttok()
                else:
                    self.error()
            self.emit(f'label {Lend}')
        else:
            self.error()

    # comparación -> operador condición_op operador
    def parse_comparacion(self):
        left = self.parse_operador()
        if self.tok.tipo in ('EQ', 'LE', 'GE', 'NE', 'LT', 'GT'):
            op = self.tok.valor
            self.nexttok()
        else:
            self.error()
        right = self.parse_operador()
        return left, op, right

    def parse_operador(self):
        if self.tok.tipo == 'ID':
            name = self.eat('ID')
            return name
        elif self.tok.tipo == 'NUMBER':
            val = self.eat('NUMBER')
            return val
        else:
            self.error()

    # while ( comparación ) órdenes endwhile
    def parse_bucle_while(self):
        # current token is 'while'
        self.nexttok()
        if self.tok.tipo != 'LPAREN':
            self.error()
        self.nexttok()
        left, op, right = self.parse_comparacion()
        if self.tok.tipo != 'RPAREN':
            self.error()
        self.nexttok()

        Lstart = self.new_label()
        Lend = self.new_label()
        self.emit(f'label {Lstart}')
        self.emit(f'if_false {left} {op} {right} goto {Lend}')
        self.parse_ordenes()
        # expect 'endwhile'
        if self.tok.tipo == 'ID' and self.tok.valor.lower() == 'endwhile':
            self.nexttok()
            self.emit(f'goto {Lstart}')
            self.emit(f'label {Lend}')
        else:
            self.error()

    # asignar -> identificador := expresión_arit
    def parse_asignar(self):
        if self.tok.tipo == 'ID':
            var = self.eat('ID')
            if self.tok.tipo == 'ASSIGN':
                self.nexttok()
                place = self.parse_expresion_arit()
                self.emit(f'{var} := {place}')
            else:
                self.error()
        else:
            self.error()

    # expresión_arit: use standard infix parser with precedence
    def parse_expresion_arit(self):
        place = self.expr()
        return place

    def expr(self):
        left = self.term()
        while self.tok.tipo in ('PLUS', 'MINUS'):
            op = self.tok.valor
            self.nexttok()
            right = self.term()
            t = self.new_temp()
            self.emit(f'{t} := {left} {op} {right}')
            left = t
        return left

    def term(self):
        left = self.factor()
        while self.tok.tipo in ('TIMES', 'DIV'):
            op = self.tok.valor
            self.nexttok()
            right = self.factor()
            t = self.new_temp()
            self.emit(f'{t} := {left} {op} {right}')
            left = t
        return left

    def factor(self):
        if self.tok.tipo == 'LPAREN':
            self.nexttok()
            val = self.expr()
            if self.tok.tipo != 'RPAREN':
                self.error()
            self.nexttok()
            return val
        elif self.tok.tipo == 'ID':
            return self.eat('ID')
        elif self.tok.tipo == 'NUMBER':
            return self.eat('NUMBER')
        else:
            self.error()


def analizar(entrada):
    try:
        lex = Lexer(entrada)
        toks = list(lex.tokens())
        # normalize IDs to keep keywords detection case-insensitive
        for t in toks:
            if t.tipo == 'ID':
                t.valor = t.valor
        p = Parser(iter(toks))
        p.parse_programa()
        print('Cadena pertenece al lenguaje')
        print('\nCódigo de tres direcciones:')
        for ln in p.code:
            print(ln)
    except SyntaxError as e:
        print('Cadena no pertenece al lenguaje')


def cargar_entrada(argv):
    """Carga la entrada desde un archivo .txt, desde stdin o desde el prompt."""
    if len(argv) > 1:
        argumento = argv[1]
        ruta = Path(argumento)
        if ruta.is_file():
            return ruta.read_text(encoding='utf-8')
        return argumento

    if not sys.stdin.isatty():
        return sys.stdin.read()

    print('Ingrese el programa. Puede pegar varias líneas y terminar con Ctrl+Z seguido de Enter en Windows:')
    return sys.stdin.read()


if __name__ == '__main__':
    entrada = cargar_entrada(sys.argv).strip()
    if not entrada:
        entrada = input('Ingrese la cadena a analizar: ')
    analizar(entrada)
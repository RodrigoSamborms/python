"""
Parser de expresiones matriciales.

Transforma una cadena como "(A @ B) + (C @ D)" en un AST (Árbol de Sintaxis Abstracta).
El AST representa operaciones y dependencias entre ellas.
"""

import re
from typing import Union, List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class MatrixVar:
    """Representa una variable de matriz."""
    name: str
    
    def __repr__(self):
        return f"MatrixVar({self.name})"


@dataclass
class BinOp:
    """Representa una operación binaria (suma, multiplicación, etc.)"""
    op: str  # '@' para multiplicación matricial, '+' para suma, '-' para resta
    left: Union['BinOp', MatrixVar]
    right: Union['BinOp', MatrixVar]
    
    def __repr__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"


class MatrixExpressionParser:
    """
    Parser recursivo descendente para expresiones matriciales.
    
    Gramática:
        expr     ::= term (('+' | '-') term)*
        term     ::= factor ('@' factor)*
        factor   ::= '(' expr ')' | VARIABLE
        VARIABLE ::= [A-Za-z_][A-Za-z0-9_]*
    """
    
    def __init__(self, expression: str):
        """
        Inicializa el parser.
        
        Args:
            expression: Cadena con la expresión matricial, ej: "(A @ B) + (C @ D)"
        """
        self.expression = expression
        self.tokens = self._tokenize(expression)
        self.pos = 0
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokeniza la expresión en tokens.
        
        Args:
            expression: Cadena con la expresión matricial
            
        Returns:
            Lista de tokens
        """
        # Patrón: variables, operadores, paréntesis
        pattern = r'([A-Za-z_][A-Za-z0-9_]*|[@+\-()\\s])'
        tokens = re.findall(pattern, expression)
        # Filtrar espacios en blanco
        tokens = [t for t in tokens if t.strip()]
        return tokens
    
    def _current_token(self) -> str:
        """Obtiene el token actual sin avanzar."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _consume(self, expected: str = None) -> str:
        """Consume un token y avanza."""
        token = self._current_token()
        if expected and token != expected:
            raise SyntaxError(f"Se esperaba '{expected}', pero se encontró '{token}'")
        self.pos += 1
        return token
    
    def parse(self) -> Union[BinOp, MatrixVar]:
        """
        Parsea la expresión completa.
        
        Returns:
            AST representando la expresión
        """
        ast = self._parse_expr()
        if self.pos < len(self.tokens):
            raise SyntaxError(f"Tokens no consumidos: {self.tokens[self.pos:]}")
        return ast
    
    def _parse_expr(self) -> Union[BinOp, MatrixVar]:
        """Parsea expr: term (('+' | '-') term)*"""
        left = self._parse_term()
        
        while self._current_token() in ['+', '-']:
            op = self._consume()
            right = self._parse_term()
            left = BinOp(op, left, right)
        
        return left
    
    def _parse_term(self) -> Union[BinOp, MatrixVar]:
        """Parsea term: factor ('@' factor)*"""
        left = self._parse_factor()
        
        while self._current_token() == '@':
            op = self._consume()
            right = self._parse_factor()
            left = BinOp(op, left, right)
        
        return left
    
    def _parse_factor(self) -> Union[BinOp, MatrixVar]:
        """Parsea factor: '(' expr ')' | VARIABLE"""
        token = self._current_token()
        
        if token == '(':
            self._consume('(')
            expr = self._parse_expr()
            self._consume(')')
            return expr
        elif token and re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', token):
            var_name = self._consume()
            return MatrixVar(var_name)
        else:
            raise SyntaxError(f"Token inesperado: {token}")


def get_dependencies(ast: Union[BinOp, MatrixVar]) -> Dict:
    """
    Extrae dependencias del AST.
    
    Retorna:
        - list_of_ops: lista de operaciones con IDs
        - graph: dict de dependencias (op_id -> [dependencias])
        - matrix_vars: conjunto de variables matriciales
    
    Args:
        ast: Árbol de sintaxis abstracta
        
    Returns:
        Tupla (list_of_ops, graph, matrix_vars)
    """
    ops_list = []
    graph = {}
    matrix_vars = set()
    op_counter = [0]  # Usar lista para mutabilidad en función anidada
    
    def visit(node: Union[BinOp, MatrixVar]) -> int:
        """Visita recursivamente y retorna el ID del nodo."""
        if isinstance(node, MatrixVar):
            matrix_vars.add(node.name)
            return None  # Las variables no tienen ID
        elif isinstance(node, BinOp):
            op_id = op_counter[0]
            op_counter[0] += 1
            
            left_id = visit(node.left)
            right_id = visit(node.right)
            
            op_info = {
                'id': op_id,
                'op': node.op,
                'left': node.left,
                'right': node.right,
                'left_id': left_id,
                'right_id': right_id
            }
            ops_list.append(op_info)
            
            # Registrar dependencias
            deps = []
            if left_id is not None:
                deps.append(left_id)
            if right_id is not None:
                deps.append(right_id)
            graph[op_id] = deps
            
            return op_id
    
    visit(ast)
    return ops_list, graph, matrix_vars


# Ejemplos de uso
if __name__ == "__main__":
    # Test 1: Expresión simple
    expr1 = "(A @ B) + (C @ D)"
    parser1 = MatrixExpressionParser(expr1)
    ast1 = parser1.parse()
    print(f"Expresión: {expr1}")
    print(f"AST: {ast1}\n")
    
    ops1, graph1, vars1 = get_dependencies(ast1)
    print(f"Operaciones: {ops1}")
    print(f"Grafo de dependencias: {graph1}")
    print(f"Variables matriciales: {vars1}\n")
    
    # Test 2: Cadena de multiplicaciones
    expr2 = "A @ B @ C + D"
    parser2 = MatrixExpressionParser(expr2)
    ast2 = parser2.parse()
    print(f"Expresión: {expr2}")
    print(f"AST: {ast2}\n")
    
    ops2, graph2, vars2 = get_dependencies(ast2)
    print(f"Operaciones: {ops2}")
    print(f"Grafo de dependencias: {graph2}")
    print(f"Variables matriciales: {vars2}\n")
    
    # Test 3: Expresión más compleja
    expr3 = "(A @ B + C) @ (D + E @ F)"
    parser3 = MatrixExpressionParser(expr3)
    ast3 = parser3.parse()
    print(f"Expresión: {expr3}")
    print(f"AST: {ast3}\n")
    
    ops3, graph3, vars3 = get_dependencies(ast3)
    print(f"Operaciones: {ops3}")
    print(f"Grafo de dependencias: {graph3}")
    print(f"Variables matriciales: {vars3}")

# lexer_parser_fortran.py
import re
from collections import namedtuple
from ast_nodes import Program, Assign, If, BinOp, Number, Var
from ast_visualizer import visualize_ast

# ---------- Token ----------
Token = namedtuple('Token', ['type', 'value', 'line', 'col'])

# ---------- Lexer ----------
class Lexer:
    token_spec = [
        ('NUMBER',   r'\d+(\.\d+)?'),             # Números (enteros o decimales)
        ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),  # Identificadores y palabras clave
        ('RELOP',    r'<=|>=|==|/=|<|>'),         # Operadores relacionales
        ('ASSIGN',   r'='),                       # Asignación
        ('PLUS',     r'\+'),                      # Suma
        ('MINUS',    r'-'),                       # Resta
        ('MUL',      r'\*'),                      # Multiplicación
        ('DIV',      r'/'),                       # División
        ('LPAREN',   r'\('),                      # Paréntesis izquierdo
        ('RPAREN',   r'\)'),                      # Paréntesis derecho
        ('NEWLINE',  r'\n'),                      # Salto de línea
        ('SKIP',     r'[ \t\r]+'),                # Ignorar espacios, tabs, retornos
        ('COMMENT',  r'\!.*'),                    # Comentarios (inician con !)
        ('MISMATCH', r'.'),                       # 'MISMATCH' debe ir al final para capturar cualquier caracter inesperado
    ]

    # Compila todas las expresiones regulares en una sola
    master_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in token_spec))

    # Palabras clave que el 'ID' debe diferenciar
    keywords = {'IF','THEN','ELSE','ENDIF'}

    def __init__(self, text):
        # Constructor: inicializa el lexer y lanza el proceso de tokenización
        self.text = text
        self.line = 1
        self.col = 1
        self.pos = 0
        self.tokens = []
        self._tokenize()   # Llama al método que genera los tokens

    def _tokenize(self):
        # Método principal que procesa el texto y genera la lista de tokens
        for mo in self.master_re.finditer(self.text):
            kind = mo.lastgroup
            val = mo.group(kind)
            if kind == 'NUMBER':
                tok = Token('NUMBER', val, self.line, self.col)
                self.tokens.append(tok)
            elif kind == 'ID':
                # Si es un ID, verifica si es una palabra clave (IF, THEN, etc.)
                up = val.upper()
                if up in self.keywords:
                    tok = Token(up, up, self.line, self.col)
                else:
                    tok = Token('ID', val, self.line, self.col)
                self.tokens.append(tok)
            elif kind in ('RELOP','ASSIGN','PLUS','MINUS','MUL','DIV','LPAREN','RPAREN'):
                # Tokens simples de operadores y paréntesis
                tok = Token(kind, val, self.line, self.col)
                self.tokens.append(tok)
            elif kind == 'NEWLINE':
                # Actualiza el contador de líneas
                self.line += 1
                self.col = 0
            elif kind in ('SKIP','COMMENT'):
                pass
            elif kind == 'MISMATCH':
                # Si es MISMATCH, es un error léxico
                raise SyntaxError(f'Unexpected character {val!r} at line {self.line} col {self.col}')
            # Actualiza la columna (posición del caracter en la línea)
            self.col += len(val)
        # Añade el token de Fin de Archivo (End of File)
        self.tokens.append(Token('EOF', '', self.line, self.col))

    def __iter__(self):
        return iter(self.tokens)

# ---------- Analizador Sintáctico (Parser) ----------
class Parser:
    # Implementa el parser de descenso recursivo
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.cur = self.tokens[self.pos]

    def eat(self, tok_type):
        if self.cur.type == tok_type:
            self.pos += 1
            self.cur = self.tokens[self.pos]
        else:
            raise SyntaxError(f'Expected {tok_type} but got {self.cur.type} at line {self.cur.line} col {self.cur.col}')

    # --- Métodos del Parser (basados en la Gramática) ---
    def parse(self):
        stmts = self.stmt_list()
        if self.cur.type != 'EOF':
            raise SyntaxError(f'Unexpected token after program end: {self.cur}')
        return Program(stmts)

    def stmt_list(self):
        stmts = []
        while self.cur.type in ('ID','IF'):
            stmts.append(self.stmt())
        return stmts

    def stmt(self):
        if self.cur.type == 'ID':
            return self.assign_stmt()
        elif self.cur.type == 'IF':
            return self.if_stmt()
        else:
            raise SyntaxError(f'Invalid statement start: {self.cur}')

    def assign_stmt(self):
        name = self.cur.value
        self.eat('ID')
        self.eat('ASSIGN')
        expr = self.expr()
        return Assign(name, expr)

    def if_stmt(self):
        self.eat('IF')
        self.eat('LPAREN')
        cond = self.cond()
        self.eat('RPAREN')
        self.eat('THEN')
        then_body = self.stmt_list()
        else_body = []
        if self.cur.type == 'ELSE':
            self.eat('ELSE')
            else_body = self.stmt_list()
        self.eat('ENDIF')
        return If(cond, then_body, else_body)

    def cond(self):
        left = self.expr()
        if self.cur.type != 'RELOP':
            raise SyntaxError(f'Expected relational operator in condition at {self.cur}')
        op = self.cur.value
        self.eat('RELOP')
        right = self.expr()
        return BinOp(left, op, right)

    def expr(self):
        node = self.term()
        while self.cur.type in ('PLUS','MINUS'):
            op = self.cur.value
            if self.cur.type == 'PLUS': self.eat('PLUS')
            else: self.eat('MINUS')
            node = BinOp(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.cur.type in ('MUL','DIV'):
            op = self.cur.value
            if self.cur.type == 'MUL': self.eat('MUL')
            else: self.eat('DIV')
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        if self.cur.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        elif self.cur.type == 'NUMBER':
            val = self.cur.value
            self.eat('NUMBER')
            return Number(val)
        elif self.cur.type == 'ID':
            name = self.cur.value
            self.eat('ID')
            return Var(name)
        else:
            raise SyntaxError(f'Unexpected factor {self.cur}')

# ---------- Funciones Auxiliares ----------
def print_ast(node, indent=0):
    pad = '  '*indent
    if isinstance(node, Program):
        print(pad + "Program")
        for s in node.stmts: print_ast(s, indent+1)
    elif isinstance(node, Assign):
        print(pad + f"Assign({node.name})")
        print_ast(node.expr, indent+1)
    elif isinstance(node, If):
        print(pad + "If")
        print(pad + " Cond:")
        print_ast(node.cond, indent+2)
        print(pad + " Then:")
        for s in node.then_body: print_ast(s, indent+2)
        if node.else_body:
            print(pad + " Else:")
            for s in node.else_body: print_ast(s, indent+2)
    elif isinstance(node, BinOp):
        print(pad + f"BinOp({node.op})")
        print_ast(node.left, indent+1)
        print_ast(node.right, indent+1)
    elif isinstance(node, Number):
        print(pad + f"Number({node.value})")
    elif isinstance(node, Var):
        print(pad + f"Var({node.name})")
    else:
        print(pad + f"Unknown node: {node}")
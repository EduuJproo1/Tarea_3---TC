# ast_nodes.py
# --------------------------
# Definición de nodos del Árbol Sintáctico
# --------------------------

class AST: 
    pass

class Program(AST):
    def __init__(self, stmts):
        self.stmts = stmts

class Assign(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class If(AST):
    def __init__(self, cond, then_body, else_body):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(AST):
    def __init__(self, value):
        self.value = float(value) if '.' in value else int(value)

class Var(AST):
    def __init__(self, name):
        self.name = name
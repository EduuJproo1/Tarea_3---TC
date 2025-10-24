# ast_visualizer.py
# ---------------------------------------------------------
# Visualización del Árbol Sintáctico (AST) usando Graphviz
# ---------------------------------------------------------

from graphviz import Digraph

# Importa las clases de AST
from ast_nodes import Program, Assign, If, BinOp, Number, Var


def visualize_ast(node, filename='ast'):
    """
    Genera una imagen PNG con la representación gráfica del AST.
    
    Parámetros:
        node: nodo raíz del árbol (objeto Program)
        filename: nombre base del archivo de salida (sin extensión)
    """
    dot = Digraph(comment='Árbol Sintáctico')
    counter = {'n': 0}

    def add_node(n):
        node_id = f"n{counter['n']}"
        counter['n'] += 1
        label = type(n).__name__

        if isinstance(n, Assign):
            label = f"Assign\\n({n.name})"
        elif isinstance(n, If):
            label = "If"
        elif isinstance(n, BinOp):
            label = f"BinOp\\n({n.op})"
        elif isinstance(n, Number):
            label = f"Number\\n({n.value})"
        elif isinstance(n, Var):
            label = f"Var\\n({n.name})"
        elif isinstance(n, Program):
            label = "Program"

        dot.node(node_id, label, shape='ellipse', style='filled', fillcolor='lightblue')
        return node_id

    def build_edges(parent_id, n):
        if isinstance(n, Program):
            for stmt in n.stmts:
                cid = add_node(stmt)
                dot.edge(parent_id, cid)
                build_edges(cid, stmt)
        elif isinstance(n, Assign):
            cid = add_node(n.expr)
            dot.edge(parent_id, cid)
            build_edges(cid, n.expr)
        elif isinstance(n, If):
            cond_id = add_node(n.cond)
            dot.edge(parent_id, cond_id, label='cond')
            build_edges(cond_id, n.cond)
            for s in n.then_body:
                sid = add_node(s)
                dot.edge(parent_id, sid, label='then')
                build_edges(sid, s)
            for s in n.else_body:
                sid = add_node(s)
                dot.edge(parent_id, sid, label='else')
                build_edges(sid, s)
        elif isinstance(n, BinOp):
            l_id = add_node(n.left)
            r_id = add_node(n.right)
            dot.edge(parent_id, l_id)
            dot.edge(parent_id, r_id)
            build_edges(l_id, n.left)
            build_edges(r_id, n.right)

    root_id = add_node(node)
    build_edges(root_id, node)
    dot.render(filename, format='png', cleanup=True)
    print(f"Árbol sintáctico guardado en: {filename}.png")
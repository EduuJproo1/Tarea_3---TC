# run_tests.py
# --------------------------------------------
# Ejecuta automáticamente todas las pruebas .txt
# del analizador léxico-sintáctico
# --------------------------------------------

import os
import sys
sys.path.append('..')

from lexer_parser_fortran_subset import Lexer, Parser, print_ast

TEST_DIR = os.path.dirname(__file__)

def run_test(filename):
    path = os.path.join(TEST_DIR, filename)
    print(f"\nProbando: {filename}")
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        lexer = Lexer(source)
        parser = Parser(list(lexer))
        ast = parser.parse()
        print("Análisis correcto.")
        print_ast(ast)
    except Exception as e:
        print(f"Error detectado: {e}")

def main():
    for file in sorted(os.listdir(TEST_DIR)):
        if file.endswith('.txt') and file != 'run_tests.py':
            run_test(file)

if __name__ == '__main__':
    main()
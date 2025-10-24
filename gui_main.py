# gui_main.py
# ------------------------------------------------------------
# Interfaz gráfica simple para el analizador FORTRAN77 (subset)
# ------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox, filedialog
import os

from lexer_parser_fortran import Lexer, Parser, print_ast
from ast_visualizer import visualize_ast

class FortranAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico-Sintáctico FORTRAN77 (Subset)")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f2f5")

        # ----- Área de texto -----
        self.text_area = tk.Text(root, wrap="word", font=("Consolas", 12), bg="white", fg="#222")
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)

        # ----- Botones -----
        frame_buttons = tk.Frame(root, bg="#f0f2f5")
        frame_buttons.pack(pady=5)

        tk.Button(frame_buttons, text="🗂️ Abrir archivo", command=self.open_file,
                  bg="#4caf50", fg="white", font=("Arial", 11), width=14).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="🔍 Analizar", command=self.analyze_code,
                  bg="#2196f3", fg="white", font=("Arial", 11), width=14).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="🌳 Ver Árbol", command=self.open_tree,
                  bg="#9c27b0", fg="white", font=("Arial", 11), width=14).grid(row=0, column=2, padx=5)
        tk.Button(frame_buttons, text="🧹 Limpiar", command=self.clear_text,
                  bg="#f44336", fg="white", font=("Arial", 11), width=14).grid(row=0, column=3, padx=5)

        self.status_label = tk.Label(root, text="Listo.", anchor="w", bg="#ddd", fg="#000", font=("Arial", 10))
        self.status_label.pack(fill="x", side="bottom")

        self.last_ast_path = None

    # ----- Funciones -----
    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo FORTRAN",
            filetypes=[("Archivos de texto", "*.txt *.f *.for"), ("Todos los archivos", "*.*")]
        )
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", code)
            self.status_label.config(text=f"Archivo cargado: {os.path.basename(filepath)}")

    def analyze_code(self):
        code = self.text_area.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Atención", "El código está vacío.")
            return

        try:
            lexer = Lexer(code)
            parser = Parser(list(lexer))
            ast = parser.parse()
            print("---- AST ----")
            print_ast(ast)

            visualize_ast(ast, "fortran_ast_gui")
            self.last_ast_path = os.path.abspath("fortran_ast_gui.png")

            self.status_label.config(text="Análisis correcto. Árbol generado.")
            messagebox.showinfo("Análisis completado", "El código es válido.\nEl árbol sintáctico fue generado correctamente.")

        except Exception as e:
            self.status_label.config(text="Error detectado.")
            messagebox.showerror("Error en análisis", f"Se detectó un error:\n\n{e}")

    def open_tree(self):
        if self.last_ast_path and os.path.exists(self.last_ast_path):
            os.startfile(self.last_ast_path)
        else:
            messagebox.showinfo("Sin árbol", "Aún no se ha generado ningún árbol sintáctico.")

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.status_label.config(text="Listo.")
        self.last_ast_path = None


if __name__ == "__main__":
    root = tk.Tk()
    app = FortranAnalyzerGUI(root)
    root.mainloop()
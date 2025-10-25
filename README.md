# 🧠 Analizador Léxico-Sintáctico para FORTRAN77 (Subconjunto)

Este proyecto implementa un **analizador léxico y sintáctico** para un subconjunto del lenguaje **FORTRAN77**, desarrollado como parte de un trabajo académico de *Teoría de la Computación*.

El sistema utiliza un **parser de descenso recursivo (LL(1))** en Python que:
- Valida el código fuente.
- Genera un **Árbol Sintáctico Abstracto (AST)**.
- Exporta el AST como imagen (`.png`) usando **Graphviz**.

Además, incluye una **interfaz gráfica (GUI)** desarrollada con Tkinter para facilitar su uso.

---

## ⚙️ Requisitos

Para ejecutar el proyecto necesitas **Python 3** y las siguientes dependencias:

- **Tkinter** → Generalmente incluido con Python.  
- **Graphviz** → Requiere tanto la biblioteca de Python como el software del sistema.

Instala la biblioteca de Python con:

```sh
pip install graphviz
```

> ⚠️ **Importante:** La biblioteca `graphviz` de Python es solo un *conector*.  
> Se debe tener instalado el software **Graphviz (el ejecutable `dot`)**.  
> Descárgalo desde: [https://graphviz.org/download/](https://graphviz.org/download/)

---

## 🖥️ Uso de la Interfaz Gráfica (GUI)

La forma principal de usar el analizador es mediante la GUI.

1. Ejecuta el programa principal desde la terminal:
   ```sh
   python gui_main.py
   ```

2. Aparecerá una ventana.  
   Usa el botón **"🗂️ Abrir archivo"** para cargar un archivo de prueba (por ejemplo, `valid_1.txt` o `invalid_2.txt`).

3. Presiona **"🔍 Analizar"** para ejecutar el parser:
   - Si el código es válido → muestra un mensaje de éxito.  
   - Si el código es inválido → muestra un mensaje de error detallado.

4. Si el análisis fue exitoso, presiona **"🌳 Ver Árbol"**.  
   Se abrirá la imagen del AST (`fortran_ast_gui.png`) generada automáticamente.

---

## 🧪 Ejecución de Pruebas Automáticas

Se pueden ejecutar todas las pruebas desde la terminal con el siguiente comando:

```sh
python run_tests.py
```

El script `run_tests.py` buscará todos los archivos `.txt` en el directorio, los analizará y mostrará los resultados (éxitos y errores) en consola.

---

## 📁 Estructura del Proyecto

```text
.
├── gui_main.py                    # Punto de entrada (interfaz gráfica)
├── lexer_parser_fortran.py        # Analizador léxico y parser recursivo
├── ast_nodes.py                   # Clases para los nodos del AST
├── ast_visualizer.py              # Genera la imagen del AST con Graphviz
├── tests/                         # Carpeta de pruebas
│   ├── run_tests.py               # Script de pruebas automáticas
│   ├── valid_1.txt                # Caso de prueba válido
│   ├── valid_2.txt
│   ├── invalid_1.txt              # Caso de prueba inválido
│   └── ...
└── fortran_ast_gui.png            # Imagen de salida generada por la GUI
```

---

## 🧩 Notas Técnicas

- El parser está implementado como un **descenso recursivo LL(1)**.  
- La gramática admite:
  - Expresiones aritméticas con precedencia y paréntesis.  
  - Estructuras condicionales `IF ... THEN ... [ELSE ...] ENDIF`.  
- La salida gráfica del AST se genera mediante **Graphviz DOT** y se exporta como imagen PNG.

---

## 👨‍💻 Integrantes

Proyecto académico desarrollado por **Eduardo Jaramillo, Eduardo Mariqueo, Vicente Ramirez**  
📘 Asignatura: *Teoría de la Computación*  
🏫 Universidad Católica de Temuco
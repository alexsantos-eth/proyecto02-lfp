# IMPORTS
import keyboard
import os

# FILES
from files.graphviz import get_automaton_graph
from files.html import grammar_dict_to_HTML, get_automaton_html

# TOOLS
from tools.colors import color


# GENERAR AUTOMATA DESDE GRAMÁTICA


def get_automaton_from_grammar(grammar_dict, grammar_name):
    """Genera un archivo svg y html de la gramática y genera el template inicial

    Args:
        grammar_dict (dict): Diccionario de gramática
        grammar_name (str): Nombre de gramática
    """
    # GENERAR GRAFO
    get_automaton_graph(grammar_dict, grammar_name)

    # GENERAR HTML
    grammar_dict_to_HTML(grammar_dict, grammar_name)

    # MENSAJE DE OK
    print(f'{color.BOLD}{color.GREEN}  ✔️  Automata generado correctamente.{color.END}')
    keyboard.read_key()


def get_automaton_input_from_grammar(template, grammar_dict, grammar_name):
    """Obtiene una expresion a evaluar y la convierte en un html

    Args:
        template (str): Tipo de html, recorrido o tabla
        grammar_dict (dict): Diccionario de gramática
        grammar_name (str): Nombre de gramática
    """
    # LIMPIAR
    os.system('clear' if os.name == 'posix' else 'cls')

    # LEER
    print(
        f'\n  {color.BOLD}Escribe una cadena para evaluar el automata: {color.END}')

    count = 0
    while(True):
        word = input('')
        key = keyboard.read_key()

        if count == 0:
            keyboard.send("shift")

        count += 1

        # SALIR
        if key == 'enter':
            print(word)
            get_automaton_html(template, grammar_dict, grammar_name, word)
            break

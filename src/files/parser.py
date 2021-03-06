# IMPORTS
import re
import keyboard

# TOOLS
from tools.dictionaries import dict_to_json

# COLORES
from tools.colors import color


def parse_file(lines):
    """Convertir archivo glc a diccionario

    Args:
        lines (str): Contenido del archivo

    Returns:
        dict: Diccionario de gramática
    """
    # GLOBALES
    grammars_dict = {}
    grammars_names = []
    current_grammar_index = 0
    grammars_invalid_dict = {}
    is_context_free_grammar = False

    # RECORRER LINEAS
    for line in lines.split("\n"):
        # NOMBRES DE GRAMÁTICAS
        if re.match("^\s*\w{2,}\s*$", line):
            grammars_names.append(line.strip())

        # NO TERMINALES ; TERMINALES ; TERMINAL INICIAL
        if re.match("^\s*([^\s]+[,;]+)+\w*\s*$", line):
            symbols = line.split(";")

            # AGREGAR A DICCIONARIO
            grammars_dict[grammars_names[current_grammar_index]] = {
                "noTerminals": symbols[0].split(','),
                "terminals": symbols[1].split(','),
                "initialNoTerminal": symbols[2]
            }

        # PRODUCCIONES
        if re.match("^\s*[^\s]+\-\>([^\s]+\s*)+", line):
            order = line.split('->')
            current_name = grammars_names[current_grammar_index]

            # COPIA DE DICCIONARIO
            transitions = order[1].split(" ")
            productions = grammars_dict[current_name].get('productions', [])
            productions.append({"entry": order[0], "transitions": transitions})

            # VERIFICAR SI ES LIBRE DE CONTEXTO
            if len(transitions) >= 3:
                is_context_free_grammar = True

            # AGREGAR A DICCIONARIO
            grammars_dict[current_name]['productions'] = productions

        # FINAL DE GRAMÁTICA
        if re.match("^\s*\*\s*", line):
            # ELIMINAR SI NO ES LIBRE DE CONTEXTO
            if not is_context_free_grammar:
                # COPIAR
                grammar_name = grammars_names[current_grammar_index]
                grammars_invalid_dict[grammar_name] = grammars_dict[grammar_name]

                # BORRAR Y SALIDA
                del grammars_dict[grammar_name]

            # AUMENTAR POSICIÓN DE GRAMÁTICAS
            current_grammar_index += 1
            is_context_free_grammar = False

    # MENSAJE DE CARGA
    print(f'{color.BOLD}{color.GREEN}  ✔️  Gramática cargada correctamente.{color.END}')
    keyboard.read_key()

    # DICCIONARIO DE SALIDA
    return {
        "validGrammars": grammars_dict,
        "invalidGrammars": grammars_invalid_dict
    }

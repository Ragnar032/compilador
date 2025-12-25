import sys
import os
import pytest

# --- PASO 1: CONFIGURAR LA RUTA (ESTO VA PRIMERO) ---
# Obtenemos la ruta absoluta de la carpeta donde está este archivo (tests/)
test_dir = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel para llegar a la raíz del proyecto (compilador/)
project_root = os.path.dirname(test_dir)
# Agregamos la raíz al sistema de rutas de Python
sys.path.insert(0, project_root)

# --- PASO 2: AHORA SÍ IMPORTAMOS LOS MÓDULOS DE SRC ---
# Si intentas importar esto antes del paso 1, fallará.
from src.lexer.tokens import TOKENS
from src.lexer.errors import ERRORS

@pytest.fixture
def imprimir_test():
    def _imprimir(nombre, codigo, lista):
        print(f"\n\n{'='*80}\n PRUEBA: {nombre}\n{'='*80}")
        print(f"ENTRADA:\n{'-'*30}\n{codigo.strip()}\n{'-'*30}")
        print(f"\n{'LEXEMA':<25} | {'ID':<5} | {'RENGLON':<7} | {'DESCRIPCIÓN'}\n{'-'*80}")
        
        actual = lista
        while actual:
            desc = TOKENS.get(actual.token_id, ERRORS.get(actual.token_id, "DESCONOCIDO"))
            lex_visual = actual.lexema.replace('\n', '\\n')
            print(f"{lex_visual:<25} | {actual.token_id:<5} | {actual.renglon:<7} | {desc}")
            actual = actual.siguiente
        print(f"{'='*80}\n")
    return _imprimir
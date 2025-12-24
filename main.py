import os
from src.lexer.lexer import Lexer
from src.lexer.manager_lexer import ManagerLexer as FileManager

def main():
    ruta_input = os.path.join("input", "codigo.txt")
    ruta_output = os.path.join("output", "tokens.txt")

    codigo_fuente = FileManager.leer_archivo(ruta_input)
    
    if codigo_fuente is not None:
        lexer = Lexer(codigo_fuente)
        lista_tokens = lexer.run() 

        FileManager.exportar_reporte(lista_tokens, ruta_output)

if __name__ == "__main__":
    main()
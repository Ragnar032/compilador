import os
import json # Agregado para que el AST se vea bien en el txt
from src.lexer.lexer import Lexer
from src.lexer.manager_lexer import ManagerLexer as FileManager
from src.parser.parser import Sintactico 

def main():
    ruta_input = os.path.join("input", "codigo.txt")
    ruta_output = os.path.join("output", "lista_tokens.txt")
    ruta_ast_output = os.path.join("output", "ast.txt")

    codigo_fuente = FileManager.leer_archivo(ruta_input)
    
    if codigo_fuente is not None:
        try:
            lexer = Lexer(codigo_fuente)
            lista_tokens = lexer.run() 
            FileManager.exportar_reporte(lista_tokens, ruta_output)
            
            if lista_tokens:
                parser = Sintactico(lista_tokens)
                # Guardamos el resultado de las reglas corregidas (el diccionario del AST)
                resultado_ast = parser.programa() 
                
                with open(ruta_ast_output, 'w', encoding='utf-8') as f:
                    # Escribimos el JSON del AST primero
                    f.write(json.dumps(resultado_ast, indent=4, ensure_ascii=False))
                    f.write("\n\n¡Análisis Sintáctico Exitoso!\n")
                    f.write("El código cumple con todas las reglas gramaticales BNF.")
                
                print("Análisis sintáctico completado sin errores.")

        except Exception as e:
            print(e)
            with open(ruta_output, 'w', encoding='utf-8') as f:
                f.write(str(e))
            with open(ruta_ast_output, 'w', encoding='utf-8') as f:
                f.write("ERROR SINTÁCTICO ENCONTRADO:\n")
                f.write(str(e))

if __name__ == "__main__":
    main()
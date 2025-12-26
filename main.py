import os
import json 
from src.lexer.lexer import Lexer
from src.lexer.manager_lexer import ManagerLexer as FileManager
from src.parser.parser import Sintactico 
from src.parser.visualizador import generar_codigo_dot

def main():
    ruta_input = os.path.join("input", "codigo.txt")
    ruta_output = os.path.join("output", "lista_tokens.txt")
    ruta_ast_output = os.path.join("output", "ast.txt")
    ruta_grafo_output = os.path.join("output", "ast.dot")
    codigo_fuente = FileManager.leer_archivo(ruta_input)
    
    if codigo_fuente is not None:
        try:
            lexer = Lexer(codigo_fuente)
            lista_tokens = lexer.run() 
            FileManager.exportar_reporte(lista_tokens, ruta_output)
            
            if lista_tokens:
                parser = Sintactico(lista_tokens)
                resultado_ast = parser.programa() 
                
                with open(ruta_ast_output, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(resultado_ast, indent=4, ensure_ascii=False))
                    f.write("\n\n¡Análisis Sintáctico Exitoso!\n")
                    f.write("El código cumple con todas las reglas gramaticales BNF.")
                
                codigo_dot = generar_codigo_dot(resultado_ast)
                with open(ruta_grafo_output, 'w', encoding='utf-8') as f:
                    f.write(codigo_dot)
                
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
from src.lexer.lexer import Lexer
from src.semantic.semantic import AnalizadorSemantico

def probar_codigo(titulo, codigo_fuente):
    print(f"\n{'='*60}")
    print(f"PRUEBA: {titulo}")
    print(f"{'='*60}")
    print(f"Código fuente:\n{codigo_fuente.strip()}\n")
    print(">>> SALIDA DEL ANALIZADOR:")
    
    # 1. Ejecutar Lexer
    try:
        lexer = Lexer(codigo_fuente)
        tokens = lexer.run()
        
        # 2. Ejecutar Semántico
        semantico = AnalizadorSemantico(tokens)
        semantico.analizar()
        
    except Exception as e:
        print(f"Excepción inesperada: {e}")

# --- CASO 1: VARIABLE DUPLICADA ---
codigo_duplicado = """
int x = 10;
int x = 20; 
"""
probar_codigo("ERROR DE VARIABLE DUPLICADA", codigo_duplicado)

# --- CASO 2: VARIABLE NO DECLARADA ---
codigo_no_declarada = """
y = 50;
"""
probar_codigo("ERROR DE VARIABLE NO DECLARADA", codigo_no_declarada)

# --- CASO 3: TIPOS INCOMPATIBLES ---
codigo_tipos = """
int a = 10;
String b = "hola";
int c = a + b;
"""
probar_codigo("ERROR DE TIPOS INCOMPATIBLES", codigo_tipos)
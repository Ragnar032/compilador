import pytest
from src.lexer.lexer import Lexer

# -----------------------------------------------------------------------------
# 1. PRUEBAS ARITMÉTICAS Y MATEMÁTICAS
# -----------------------------------------------------------------------------
def test_aritmetica_completa(imprimir_test):
    # Prueba todos los operadores matemáticos definidos en la matriz
    codigo = "suma = a + b - c * d / e % f;"
    lexer = Lexer(codigo)
    lista = lexer.run()
    
    # Genera la tabla visual en la consola
    imprimir_test("Aritmética Completa", codigo, lista)
    
    # Verificamos la secuencia de operadores IDs: 121(=), 104(+), 105(-), 106(*), 107(/), 108(%)
    ops_esperados = [121, 104, 105, 106, 107, 108]
    ops_encontrados = []
    nodo = lista
    while nodo:
        if nodo.token_id in ops_esperados:
            ops_encontrados.append(nodo.token_id)
        nodo = nodo.siguiente
    assert ops_encontrados == ops_esperados

# -----------------------------------------------------------------------------
# 2. PRUEBAS LÓGICAS Y RELACIONALES
# -----------------------------------------------------------------------------
def test_logica_y_relacional(imprimir_test):
    # Prueba operadores compuestos (>=, !=) y palabras lógicas (and, not)
    codigo = """\
    if (a >= b and c != d) {
        res = not true;
    }
    """
    lexer = Lexer(codigo)
    lista = lexer.run()
    
    imprimir_test("Lógica y Relacionales", codigo, lista)
    
    # Validamos tokens clave según reserved.py y tokens.py
    n = lista
    while n:
        if n.lexema == ">=": assert n.token_id == 117
        if n.lexema == "!=": assert n.token_id == 116
        if n.lexema == "and": assert n.token_id == 205
        if n.lexema == "not": assert n.token_id == 207
        n = n.siguiente

# -----------------------------------------------------------------------------
# 3. PRUEBAS DE LIMPIEZA (Comentarios)
# -----------------------------------------------------------------------------
def test_comentarios_ignorados(imprimir_test):
    # Verifica que el lexer ignore comentarios de línea (//) y de bloque (/* */)
    codigo = """\
    x = 10 / 2; // División válida y comentario de linea
    /* Comentario de bloque
       que ocupa varias lineas
       y debe desaparecer */
    y = 5;
    """
    lexer = Lexer(codigo)
    lista = lexer.run()
    
    imprimir_test("Filtrado de Comentarios", codigo, lista)
    
    # Buscamos el primer punto y coma
    nodo = lista
    while nodo and nodo.lexema != ";":
        nodo = nodo.siguiente
    
    # El siguiente nodo debe ser 'y' (ID 100), saltándose los comentarios
    assert nodo.siguiente.lexema == "y"
    assert nodo.siguiente.token_id == 100

# -----------------------------------------------------------------------------
# 4. PRUEBA INTEGRAL (Estructura Java)
# -----------------------------------------------------------------------------
def test_estructura_java(imprimir_test):
    # Simulación de un programa estructurado con palabras reservadas y cadenas
    codigo = """\
    public class Test {
        public static void main() {
            String s = "Exito";
            print(s);
        }
    }
    """
    lexer = Lexer(codigo)
    lista = lexer.run()
    
    imprimir_test("Programa Completo (Java)", codigo, lista)
    
    # Verificación de tokens de inicio
    assert lista.token_id == 210 # public
    assert lista.siguiente.token_id == 209 # class
    assert lista.siguiente.siguiente.lexema == "Test"
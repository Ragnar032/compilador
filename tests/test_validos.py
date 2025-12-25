from src.lexer.lexer import Lexer

# -----------------------------------------------------------------------------
# 1. PRUEBAS ARITMÉTICAS Y MATEMÁTICAS
# -----------------------------------------------------------------------------
def test_aritmetica_completa(imprimir_test):
    # Prueba todos los operadores matemáticos
    codigo = "suma = a + b - c * d / e % f;"
    lexer = Lexer(codigo)
    lista = lexer.run()
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
    # Prueba operadores compuestos (<=, >=, ==, !=) y palabras lógicas (and, or, not)
    codigo = """\
    if (a >= b and c != d) {
        res = not true;
    }
    """
    lexer = Lexer(codigo)
    lista = lexer.run()
    imprimir_test("Lógica y Relacionales", codigo, lista)
    
    # Validamos tokens clave
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
    # PRUEBA CRÍTICA: El lexer debe distinguir '/' de '//' y '/*'
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
    
    # La lista debe ser: x, =, 10, /, 2, ;, y, =, 5, ;
    # NO debe haber nada entre el ';' de la primera linea y la 'y'
    nodo = lista
    while nodo.lexema != ";": # Primer punto y coma
        nodo = nodo.siguiente
    
    # El siguiente nodo DEBE ser 'y', saltándose todo el bloque /* ... */
    assert nodo.siguiente.lexema == "y"

# -----------------------------------------------------------------------------
# 4. PRUEBA INTEGRAL (Estructura Java)
# -----------------------------------------------------------------------------
def test_estructura_java(imprimir_test):
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
    
    assert lista.token_id == 210 # public
    assert lista.siguiente.token_id == 209 # class
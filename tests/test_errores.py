from src.lexer.lexer import Lexer

def test_error_500_caracter_invalido(imprimir_test):
    # Tu matriz Fila 0, Columna 2 (_) -> 500
    # Esto significa que un guion bajo al inicio es ilegal
    codigo = "_variable"
    lexer = Lexer(codigo)
    lista = lexer.run()
    imprimir_test("Error 500: Guion Bajo Inicial", codigo, lista)
    
    assert lista.token_id == 500

def test_error_502_exclamacion_sola(imprimir_test):
    # Tu matriz Fila 0 -> '!' va a Estado 10
    # Estado 10: Si recibe '=', va a 116 (!=)
    # Estado 10: Si recibe cualquier otra cosa -> 502
    codigo = "!true" 
    lexer = Lexer(codigo)
    lista = lexer.run()
    imprimir_test("Error 502: Exclamación sin igual", codigo, lista)
    
    # Debería detectar el error 502 al inicio
    assert lista.token_id == 502

def test_error_504_identificador_invalido(imprimir_test):
    # Tu matriz Fila 2 (Entero) -> Recibe Letra (Col 0) -> 504
    codigo = "123abcde"
    lexer = Lexer(codigo)
    lista = lexer.run()
    imprimir_test("Error 504: ID Inválido (Num+Letra)", codigo, lista)
    
    # 123 intenta ser entero, entra 'a', salta a 504
    # Dependiendo de la implementación del lexer, el error puede ser el siguiente nodo
    # o reemplazar el actual. Buscamos la presencia del 504.
    encontrado = False
    nodo = lista
    while nodo:
        if nodo.token_id == 504:
            encontrado = True
        nodo = nodo.siguiente
    assert encontrado

def test_error_501_numero_mal_formado(imprimir_test):
    # Tu matriz Fila 3 (Punto tras dígito) -> Recibe espacio/fin -> 501
    codigo = "10. "
    lexer = Lexer(codigo)
    lista = lexer.run()
    imprimir_test("Error 501: Real incompleto", codigo, lista)
    
    # Saltamos el posible token previo si lo separa, buscamos el error
    nodo = lista
    assert nodo.token_id == 501 or (nodo.siguiente and nodo.siguiente.token_id == 501)

def test_error_506_real_mal_formado(imprimir_test):
    # Tu matriz Fila 4 (Decimales) -> Recibe Letra -> 506
    codigo = "3.1416pi"
    lexer = Lexer(codigo)
    lista = lexer.run()
    imprimir_test("Error 506: Real con letras", codigo, lista)
    
    nodo = lista
    found = False
    while nodo:
        if nodo.token_id == 506: found = True
        nodo = nodo.siguiente
    assert found

def test_error_503_string_multilinea(imprimir_test):
    # Tu matriz Fila 5 (String) -> Recibe NL (Col 23) -> 503
    codigo = '"Hola \n Mundo"'
    lexer = Lexer(codigo)
    lista = lexer.run()
    imprimir_test("Error 503: String con salto de linea", codigo, lista)
    
    # El lexer debería cortar cuando ve el salto de linea y reportar error
    nodo = lista
    found = False
    while nodo:
        if nodo.token_id == 503: found = True
        nodo = nodo.siguiente
    assert found
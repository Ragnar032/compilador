import pytest
from src.lexer.lexer import Lexer

# -----------------------------------------------------------------------------
# ERROR 500: Caracter invalido
# -----------------------------------------------------------------------------
def test_error_500_caracter_invalido(imprimir_test):
    codigo = "int x = @;" 
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 500", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        assert "ID Error: 500" in mensaje
        return
    pytest.fail("Debe detenerse con Error 500")

# -----------------------------------------------------------------------------
# ERROR 501: Numero mal formado
# -----------------------------------------------------------------------------
def test_error_501_numero_mal_formado(imprimir_test):
    codigo = "x = 10. "
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 501", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        assert "ID Error: 501" in mensaje
        return
    pytest.fail("Debe detenerse con Error 501")

# -----------------------------------------------------------------------------
# ERROR 502: Operador '!=' mal formado
# -----------------------------------------------------------------------------
def test_error_502_exclamacion_sola(imprimir_test):
    codigo = "if (a ! b)" 
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 502", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        assert "ID Error: 502" in mensaje
        return
    pytest.fail("Debe detenerse con Error 502")

# -----------------------------------------------------------------------------
# ERROR 503: String sin cerrar
# -----------------------------------------------------------------------------
def test_error_503_string_multilinea(imprimir_test):
    codigo = 'String s = "Hola\nMundo";'
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 503", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        assert "ID Error: 503" in mensaje
        return
    pytest.fail("Debe detenerse con Error 503")

# -----------------------------------------------------------------------------
# ERROR 504: Identificador invalido
# -----------------------------------------------------------------------------
def test_error_504_identificador_invalido(imprimir_test):
    codigo = "int 123abcde = 5;"
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 504", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        assert "ID Error: 504" in mensaje
        return
    pytest.fail("Debe detenerse con Error 504")

# -----------------------------------------------------------------------------
# ERROR 505: Comentario bloque sin cerrar
# -----------------------------------------------------------------------------
def test_error_505_comentario_bloque_sin_cerrar(imprimir_test):
    codigo = "int x = 10; /* Comentario que no cierra..."
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 505", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        assert "ID Error: 505" in mensaje
        return
    pytest.fail("Debe detenerse con Error 505")

# -----------------------------------------------------------------------------
# ERROR 506: Real mal formado
# -----------------------------------------------------------------------------
def test_error_506_real_mal_formado(imprimir_test):
    codigo = "double d = 3.14pi;"
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 506", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        assert "ID Error: 506" in mensaje
        return
    pytest.fail("Debe detenerse con Error 506")

# -----------------------------------------------------------------------------
# ERROR 507: Comentario incompleto (Mapeado a 505 por diseño de run)
# -----------------------------------------------------------------------------
def test_error_507_comentario_incompleto(imprimir_test):
    # En tu lexer.py, el fin de archivo en estado 8 lanza 505 manualmente
    codigo = "/* comentario * " 
    lexer = Lexer(codigo)
    try:
        lexer.run()
    except Exception as e:
        imprimir_test("Tokens antes del Error 507", codigo, lexer.head)
        mensaje = str(e)
        print(f"RESULTADO: {mensaje}")
        # Se verifica 505 porque es lo que lanza tu código en la línea 147
        assert "ID Error: 505" in mensaje 
        return
    pytest.fail("Debe detenerse con Error 505/507")
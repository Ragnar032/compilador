import pytest
from src.lexer.lexer import Lexer

# Funcion auxiliar para convertir tu Lista Enlazada a Lista Python
# Esto permite hacer assertions faciles (ej: tokens[0])
def linked_list_to_list(head_node):
    result = []
    current = head_node
    while current:
        result.append(current)
        current = current.siguiente
    return result

# --- PRUEBAS ---

def test_enteros():
    lexer = Lexer("12345")
    head = lexer.run()          # Usamos TU metodo run()
    tokens = linked_list_to_list(head)
    
    assert len(tokens) == 1
    assert tokens[0].token_id == 101       # Verificamos token_id
    assert tokens[0].lexema == "12345"     # Verificamos lexema

def test_identificadores():
    lexer = Lexer("variable_1")
    head = lexer.run()
    tokens = linked_list_to_list(head)
    
    assert len(tokens) == 1
    assert tokens[0].token_id == 100
    assert tokens[0].lexema == "variable_1"

def test_operadores_y_puntuacion():
    # + (104) y ; (122)
    lexer = Lexer("+ ;") 
    head = lexer.run()
    tokens = linked_list_to_list(head)
    
    # Deberia haber 2 tokens
    assert len(tokens) == 2
    assert tokens[0].token_id == 104
    assert tokens[0].lexema == "+"
    assert tokens[1].token_id == 122
    assert tokens[1].lexema == ";"

def test_comentarios_bloque():
    # Tu codigo debe ignorar esto y no generar nodos, o manejarlo segun tu logica
    code = "/* test */"
    lexer = Lexer(code)
    head = lexer.run()
    tokens = linked_list_to_list(head)
    
    # Si la logica es ignorarlo, la lista debe estar vacia
    assert len(tokens) == 0

def test_error_comentario_incompleto():
    # Test para tu logica especifica de cortar mensaje a 15 chars
    code = "/* comentario muy largo sin cerrar"
    lexer = Lexer(code)
    head = lexer.run()
    tokens = linked_list_to_list(head)
    
    assert len(tokens) == 1
    # Error 507 es comentario incompleto en Fila 8 de la matriz
    assert tokens[0].token_id == 507 
    # Verificamos tu logica de recorte de mensaje
    assert "El bloque de comentario esta malformado" in tokens[0].lexema
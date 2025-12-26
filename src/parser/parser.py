# src/parser/parser.py
from src.lexer.tokens import TOKENS

class Sintactico:
    def __init__(self, lista_tokens):
        self.actual = lista_tokens
        self.hay_error = False

    # MÉTODOS AUXILIARES

    
    def reportar_error(self, esperado):
        self.hay_error = True
        lexema_encontrado = self.actual.lexema if self.actual else "EOF"
        linea = self.actual.renglon if self.actual else "Final"
        
        
        if isinstance(esperado, int):
            nombre_esperado = TOKENS.get(esperado, f"Token {esperado}")
        else:
            nombre_esperado = esperado
        
        sugerencia = ""
        if lexema_encontrado.lower() == str(nombre_esperado).lower():
            sugerencia = f"\n💡 Sugerencia: Revisa las mayúsculas. ¿Quisiste decir '{nombre_esperado}'?"

        raise Exception(f"\n>>> ERROR SINTÁCTICO <<<\n"
                        f"Línea: {linea}\n"
                        f"Se esperaba: {nombre_esperado}\n"
                        f"Se encontró: '{lexema_encontrado}'"
                        f"{sugerencia}")

    def match(self, id_esperado):
        if self.actual and self.actual.token_id == id_esperado:
            nodo_retorno = self.actual
            self.actual = self.actual.siguiente
            return nodo_retorno
        else:
            self.reportar_error(id_esperado)

    def peek(self):
        if self.actual:
            return self.actual.token_id
        return None

    # REGLAS GRAMATICALES 
    # <programa> ::= <clase_principal>
    def programa(self):
        return {
            "tipo": "Programa",
            "contenido": self.clase_principal()
        }

    # <clase_principal> ::= "public" "class" <identificador> "{" <cuerpo_clase> "}"
    def clase_principal(self):
        self.match(210) # public
        self.match(209) # class
        id_nodo = self.match(100) # ID
        self.match(111) # {
        cuerpo = self.cuerpo_clase()
        self.match(112) # }
        return {
            "tipo": "ClasePrincipal",
            "nombre": id_nodo.lexema,
            "cuerpo": cuerpo
        }

    # <cuerpo_clase> ::= <metodo_main> | <declaracion_var> <cuerpo_clase> | ε
    def cuerpo_clase(self):
        miembros = []
        while self.peek() != 112 and self.actual is not None:
            if self.peek() == 210: 
                miembros.append(self.metodo_main())
            else:
                miembros.append(self.declaracion_var())
        return miembros

    # <metodo_main> ::= "public" "static" "void" "main" "(" ")" "{" <lista_sentencias> "}"
    def metodo_main(self):
        self.match(210); self.match(212); self.match(204); self.match(213)
        self.match(109); self.match(110); self.match(111)
        sentencias = self.lista_sentencias()
        self.match(112)
        return {
            "tipo": "MetodoMain",
            "sentencias": sentencias
        }

    # <lista_sentencias> ::= <sentencia> <lista_sentencias> | ε
    def lista_sentencias(self):
        nodos = []
        while self.peek() != 112 and self.actual is not None:
            nodos.append(self.sentencia())
        return nodos

    # <sentencia> ::= <declaracion_var> | <if_stmt> | <while_stmt> | <asignacion> | <impresion>
    def sentencia(self):
        token = self.peek()
        if token in [200, 201, 202, 203]:
            return self.declaracion_var()
        elif token == 215:
            return self.if_stmt()
        elif token == 217:
            return self.while_stmt()
        elif token == 208:
            return self.impresion()
        elif token == 100:
            return self.asignacion()
        else:
            self.reportar_error("Sentencia válida")

    # <declaracion_var> ::= <tipo> <identificador> [ "=" <expresion> ] ";"
    def declaracion_var(self):
        tipo = self.actual.lexema
        self.actual = self.actual.siguiente
        nombre = self.match(100).lexema
        valor = None
        if self.peek() == 121:
            self.match(121)
            valor = self.expresion()
        self.match(122)
        return {"tipo": "Declaracion", "dt": tipo, "id": nombre, "valor": valor}

    # <impresion> ::= "print" "(" <expresion> ")" ";"
    def impresion(self):
        self.match(208)
        self.match(109)
        exp = self.expresion()
        self.match(110)
        self.match(122)
        return {"tipo": "Impresion", "argumento": exp}

    # <if_stmt> ::= "if" "(" <expresion> ")" "{" <lista_sentencias> "}" [ "else" "{" <lista_sentencias> "}" ]
    def if_stmt(self):
        self.match(215)
        self.match(109)
        cond = self.expresion()
        self.match(110); self.match(111)
        cuerpo_if = self.lista_sentencias()
        self.match(112)
        cuerpo_else = None
        if self.peek() == 216:
            self.match(216); self.match(111)
            cuerpo_else = self.lista_sentencias()
            self.match(112)
        return {"tipo": "If", "condicion": cond, "bloque_if": cuerpo_if, "bloque_else": cuerpo_else}

    # <while_stmt> ::= "while" "(" <expresion> ")" "{" <lista_sentencias> "}"
    def while_stmt(self):
        self.match(217)
        self.match(109)
        cond = self.expresion()
        self.match(110); self.match(111)
        cuerpo = self.lista_sentencias()
        self.match(112)
        return {"tipo": "While", "condicion": cond, "cuerpo": cuerpo}

    # <asignacion> ::= <identificador> "=" <expresion> ";"
    def asignacion(self):
        nombre = self.match(100).lexema
        self.match(121)
        val = self.expresion()
        self.match(122)
        return {"tipo": "Asignacion", "id": nombre, "valor": val}

    # <expresion> ::= <termino> { (OP_REL | "+" | "-") <termino> }
    def expresion(self):
        izq = self.termino()
        # IDs: +, -, ==, !=, <, >, <=, >=
        while self.peek() in [104, 105, 115, 116, 117, 118, 119, 120]:
            op = self.actual.lexema
            self.match(self.peek())
            der = self.termino()
            izq = {"tipo": "OperacionBinaria", "op": op, "izq": izq, "der": der}
        return izq

    # <termino> ::= <factor> { ("*" | "/" | "%") <factor> }
    def termino(self):
        izq = self.factor()
        while self.peek() in [106, 107, 108]:
            op = self.actual.lexema
            self.match(self.peek())
            der = self.factor()
            izq = {"tipo": "OperacionBinaria", "op": op, "izq": izq, "der": der}
        return izq

    # <factor> ::= <id> | <num> | <cadena> | "true" | "false" | "(" <expresion> ")"
    def factor(self):
        token_actual = self.peek()
        
        # Basado en tu archivo reserved.py:
        # 100: IDENTIFICADOR, 101: ENTERO, 102: REAL, 103: CADENA
        # 220: true, 221: false
        literales_validos = [100, 101, 102, 103, 220, 221]

        if token_actual in literales_validos:
            lex = self.actual.lexema
            self.match(token_actual)
            return {"tipo": "Literal", "valor": lex}
            
        elif token_actual == 109: # L_PAREN "("
            self.match(109)
            exp = self.expresion()
            self.match(110) # R_PAREN ")"
            return exp
            
        else:
            self.reportar_error("Valor (ID, Número, Cadena o Booleano)")
from src.lexer.tokens import TOKENS
from src.table_types.table_types import SEMANTIC_MATRIX, INT, DBL, BOL, STR 
from src.semantic.variable_list import ListaVariables
from src.semantic.postfix import PostfixConverter

class AnalizadorSemantico:
    def __init__(self, head_node):
        self.current = head_node
        self.lista_variables = ListaVariables()
        
        self.mapa_declaracion = { 
            200: INT, 201: DBL, 202: BOL, 203: STR, 
            204: "void" 
        }
        self.mapa_literales = { 101: INT, 102: DBL, 103: STR, 220: BOL, 221: BOL }

    def analizar(self):
        print("\n>>> INICIANDO ANÁLISIS SEMÁNTICO <<<")
        while self.current:
            token = self.current.token_id
            
            if token == 111: # {
                self.lista_variables.enter_scope()
                self.avanzar()
            elif token == 112: # }
                self.lista_variables.exit_scope()
                self.avanzar()

            elif token in [210, 211, 212]: 
                self.avanzar()
            elif token == 209: # class
                self.avanzar() 
                if self.current and self.current.token_id == 100:
                    self.lista_variables.add_variable(self.current.lexema, "class", self.current.renglon)
                    self.avanzar()

            elif token in [215, 217]: 
                self.procesar_condicion()
            
            elif token == 208: 
                self.procesar_print()

 
            elif token == 216: 
                self.avanzar() 
            
            
            elif token in self.mapa_declaracion:
                self.procesar_declaracion()

            
            elif token == 100: 
                if self.peek_token() == 121: 
                    print(f"--- Asignación (Línea {self.current.renglon}) ---")
                    self.convertir_y_evaluar(self.current, stop_tokens=[122])
                    if self.current and self.current.token_id == 122:
                        self.avanzar()
                else:
                    if self.current.siguiente and self.current.siguiente.token_id == 109:
                        self.avanzar() 
                    else:
                        tipo = self.lista_variables.get_variable_type(self.current.lexema)
                        if not tipo:
                            print(f"[ERROR SEMÁNTICO] Línea {self.current.renglon}: Variable '{self.current.lexema}' no ha sido declarada.")
                        self.avanzar()
            else:
                self.avanzar()

    def procesar_condicion(self):
        estructura = self.current.lexema
        renglon = self.current.renglon
        self.avanzar()
        
        if self.current.token_id == 109: 
            self.avanzar()
            print(f"--- Condición {estructura} (Línea {renglon}) ---")
            tipo_resultado = self.convertir_y_evaluar(self.current, stop_tokens=[110])
            
            if tipo_resultado != BOL and tipo_resultado != "error":
                print(f"[ERROR SEMÁNTICO] Línea {renglon}: La condición '{estructura}' espera boolean, recibió '{tipo_resultado}'.")
            
            if self.current and self.current.token_id == 110:
                self.avanzar() 
        else:
             print(f"[ERROR SEMÁNTICO] Línea {renglon}: Se esperaba '(' en {estructura}.")

    def procesar_print(self):
        renglon = self.current.renglon
        self.avanzar() # Consumir 'print'
        
        if self.current.token_id == 109: # (
            self.avanzar() # Consumir '('
            
            print(f"--- Expresión Print (Línea {renglon}) ---")
            
            converter = PostfixConverter(self.current)
            rpn, nodo_final = converter.convertir(stop_tokens=[110])
            
            lista_lexemas = [n.lexema.strip() for n in rpn]
            lista_lexemas.append("print") 
            print(lista_lexemas)
            
            self.evaluar_rpn(rpn)
            
            self.current = nodo_final
            
            if self.current and self.current.token_id == 110: # )
                self.avanzar() 
                if self.current and self.current.token_id == 122: # ;
                    self.avanzar() 
        else:
             print(f"[ERROR SEMÁNTICO] Línea {renglon}: Se esperaba '(' después de print.")

    def procesar_declaracion(self):
        tipo_decl = self.mapa_declaracion[self.current.token_id]
        self.avanzar() 
        
        if self.current and self.current.token_id == 100:
            nombre = self.current.lexema
            renglon = self.current.renglon
            
            try:
                self.lista_variables.add_variable(nombre, tipo_decl, renglon)
            except Exception as e:
                print(f"[ERROR SEMÁNTICO] {e}") 
            
            siguiente = self.peek_token()
            if siguiente == 109: # funcion
                self.avanzar() 
                while self.current and self.current.token_id != 110: 
                    self.avanzar()
                self.avanzar() 
                return 
            elif siguiente == 121: # asignacion
                print(f"--- Inicialización {nombre} (Línea {renglon}) ---")
                self.convertir_y_evaluar(self.current, stop_tokens=[122])
                if self.current and self.current.token_id == 122:
                    self.avanzar()
            else: # declaracion sola
                self.avanzar() 
                if self.current and self.current.token_id == 122:
                    self.avanzar()
        else:
            self.avanzar() 

    def convertir_y_evaluar(self, nodo_inicio, stop_tokens=[122]):
        converter = PostfixConverter(nodo_inicio)
        rpn, nodo_final = converter.convertir(stop_tokens)
        
        if rpn:
            lista_lexemas = [nodo.lexema.strip() for nodo in rpn]
            print(lista_lexemas)
        
        tipo = self.evaluar_rpn(rpn)
        self.current = nodo_final
        return tipo

    def evaluar_rpn(self, lista_rpn):
        pila = [] 
        for nodo in lista_rpn:
            tid = nodo.token_id
            
            if tid in self.mapa_literales:
                pila.append({"tipo": self.mapa_literales[tid], "modo": "VALOR", "lexema": nodo.lexema})
            elif tid == 100:
                tipo = self.lista_variables.get_variable_type(nodo.lexema)
                if not tipo:
                    print(f"[ERROR SEMÁNTICO] Línea {nodo.renglon}: Variable '{nodo.lexema}' no ha sido declarada.")
                    pila.append({"tipo": "error", "modo": "ID", "lexema": nodo.lexema})
                else:
                    pila.append({"tipo": tipo, "modo": "ID", "lexema": nodo.lexema})
            elif tid in SEMANTIC_MATRIX:
                if len(pila) < 2: return "error"
                der = pila.pop()
                izq = pila.pop()
                self.validar_y_operar(izq, tid, der, pila, nodo.renglon)
        
        if pila: return pila[0]["tipo"]
        return "void"

    def validar_y_operar(self, izq, op_id, der, pila, renglon):
        if izq["tipo"] == "error" or der["tipo"] == "error":
            pila.append({"tipo": "error", "modo": "VALOR"})
            return
        
        if op_id == 121 and izq["modo"] != "ID":
            print(f"[ERROR SEMÁNTICO] Línea {renglon}: No se puede asignar valor a una constante.")
            pila.append({"tipo": "error"})
            return
        
        try:
            resultado_tipo = SEMANTIC_MATRIX[op_id][izq["tipo"]][der["tipo"]]
        except KeyError:
            resultado_tipo = None 
            
        if not resultado_tipo:
            operador_str = "ASIGNACION" if op_id == 121 else "OPERACION"
            print(f"[ERROR SEMÁNTICO] Línea {renglon}: Tipos incompatibles en {operador_str}.")
            print(f"    No se puede operar '{izq['tipo']}' con '{der['tipo']}'.")
            pila.append({"tipo": "error", "modo": "VALOR"})
        else:
            pila.append({"tipo": resultado_tipo, "modo": "VALOR"})

    def avanzar(self):
        if self.current: self.current = self.current.siguiente
    
    def peek_token(self):
        return self.current.siguiente.token_id if self.current and self.current.siguiente else None
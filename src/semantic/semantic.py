# src/semantic/semantic.py
from src.table_types.table_types import INT, DBL, BOL, STR 
from src.semantic.variable_list import ListaVariables
from src.semantic.postfix import PostfixConverter
from src.semantic.type_evaluator import TypeEvaluator  

class AnalizadorSemantico:
    def __init__(self, head_node):
        self.current = head_node
        self.lista_variables = ListaVariables()
        self.evaluator = TypeEvaluator(self.lista_variables) 
        
        self.mapa_declaracion = { 
            200: INT, 201: DBL, 202: BOL, 203: STR, 
            204: "void" 
        }

    def analizar(self):
        while self.current:
            token = self.current.token_id
            
            if token == 111: 
                self.lista_variables.enter_scope()
                self.avanzar()
            elif token == 112: 
                self.lista_variables.exit_scope()
                self.avanzar()

            elif token in [210, 211, 212]: 
                self.avanzar()
            elif token == 209: 
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
                    self.convertir_y_evaluar(self.current, stop_tokens=[122])
                    if self.current and self.current.token_id == 122:
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
            tipo_resultado = self.convertir_y_evaluar(self.current, stop_tokens=[110])
            
            if tipo_resultado != BOL and tipo_resultado != "error":
                print(f"[ERROR SEMÁNTICO] Línea {renglon}: La condición '{estructura}' espera boolean, recibió '{tipo_resultado}'.")
            
            if self.current and self.current.token_id == 110:
                self.avanzar() 
        else:
             print(f"[ERROR SEMÁNTICO] Línea {renglon}: Se esperaba '(' en {estructura}.")

    def procesar_print(self):
        renglon = self.current.renglon
        self.avanzar() 
        
        if self.current.token_id == 109: 
            self.avanzar() 
            
            converter = PostfixConverter(self.current)
            rpn, nodo_final = converter.convertir(stop_tokens=[110])
            
            lista_lexemas = [n.lexema.strip() for n in rpn]
            lista_lexemas.append("print")  
            print(lista_lexemas)
            
            self.evaluator.evaluar(rpn) 
            
            
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
            if siguiente == 109: 
                self.avanzar() 
                while self.current and self.current.token_id != 110: 
                    self.avanzar()
                self.avanzar() 
                return 
            elif siguiente == 121: 
                self.convertir_y_evaluar(self.current, stop_tokens=[122])
                if self.current and self.current.token_id == 122:
                    self.avanzar()
            else: 
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
        
        tipo = self.evaluator.evaluar(rpn) 
        
        
        self.current = nodo_final
        return tipo

    def avanzar(self):
        if self.current: self.current = self.current.siguiente
    
    def peek_token(self):
        return self.current.siguiente.token_id if self.current and self.current.siguiente else None
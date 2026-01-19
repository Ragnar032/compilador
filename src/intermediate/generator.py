# src/intermediate/generator.py

from src.semantic.postfix import PostfixConverter 
from src.intermediate.tac_manager import TacManager
from src.intermediate.expr_gen import ExpressionGenerator

class IntermediateGenerator:
    def __init__(self, head_node):
        self.current = head_node
        self.tac = TacManager()
        self.expr_gen = ExpressionGenerator(self.tac)
        self.control_stack = [] 

    def generar(self):
        while self.current:
            tid = self.current.token_id

            if tid == 215: # IF
                self.procesar_if()
                
            elif tid == 216: # ELSE
                self.procesar_else()
                
            elif tid == 217: # WHILE
                self.procesar_while()
                
            elif tid == 112: # }
                self.cerrar_bloque()
                self.avanzar()

            elif tid == 100: # Identificador
                if self.peek_token() == 121: 
                    self.procesar_expresion(stop_tokens=[122]) 
                    if self.current and self.current.token_id == 122:
                        self.avanzar()
                    else:
                        print(f"Error: Se esperaba ';' en la línea {self.current.linea if self.current else '?'}")
                else:
                    self.avanzar()

            elif tid == 208: # print
                self.procesar_print()

            else:
                self.avanzar()
        
        self.tac.print_code()


    def procesar_if(self):
        self.avanzar() #  'if'
        self.avanzar() #  '('
        
        cond_temp = self.procesar_expresion(stop_tokens=[110])
        
        if self.current.token_id == 110: self.avanzar() #  ')'
        else:print(f"Error: Se esperaba ')' después de la condición en línea {self.current.linea if self.current else '?'}")
        
        L_false = self.tac.new_label()
        self.tac.emit("BrF", cond_temp, None, L_false)
        
        self.control_stack.append(("IF", L_false))

    def procesar_else(self):
        self.avanzar() # 'else'
        
        if self.control_stack:
            tipo, L_false = self.control_stack.pop()
            
 
            L_final = self.tac.new_label()
            self.tac.emit("Br", None, None, L_final)
            
            self.tac.emit_label(L_false)
            
            self.control_stack.append(("ELSE", L_final))

  
    def procesar_while(self):
        self.avanzar() #  'while'
        
        L_inicio = self.tac.new_label()
        self.tac.emit_label(L_inicio)
        
        self.avanzar() #  '('
        cond_temp = self.procesar_expresion(stop_tokens=[110])
        
        L_salida = self.tac.new_label()
        self.tac.emit("BrF", cond_temp, None, L_salida)
        
        if self.current.token_id == 110: self.avanzar() # ')'
        else: print(f"Error: Se esperaba ')' en el while en línea {self.current.linea if self.current else '?'}")
        
        self.control_stack.append(("WHILE", L_salida, L_inicio))

    def cerrar_bloque(self):
        if self.control_stack:
            datos = self.control_stack.pop()
            tipo = datos[0]
            
            if tipo == "IF":
                L_salida = datos[1]
                self.tac.emit_label(L_salida)
                
            elif tipo == "ELSE":
                L_final = datos[1]
                self.tac.emit_label(L_final)
                
            elif tipo == "WHILE":
                L_salida = datos[1]
                L_inicio = datos[2]
                self.tac.emit("Br", None, None, L_inicio)
                self.tac.emit_label(L_salida)

  
    def procesar_expresion(self, stop_tokens):
        converter = PostfixConverter(self.current)
        rpn_list, nodo_final = converter.convertir(stop_tokens)
        
        temporal_resultado = self.expr_gen.generar_desde_rpn(rpn_list)
        
        self.current = nodo_final
        return temporal_resultado

    def procesar_print(self):
        self.avanzar() # print
        self.avanzar() # (
        res = self.procesar_expresion(stop_tokens=[110])
        self.tac.emit("print", None, None, res)
        if self.current.token_id == 110: self.avanzar()
        if self.current.token_id == 122: self.avanzar()

    def avanzar(self):
        if self.current: self.current = self.current.siguiente

    def peek_token(self):
        return self.current.siguiente.token_id if self.current and self.current.siguiente else None
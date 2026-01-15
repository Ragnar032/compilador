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

            # --- ESTRUCTURAS DE CONTROL ---
            if tid == 215: # IF
                self.procesar_if()
                
            elif tid == 216: # ELSE
                self.procesar_else()
                
            elif tid == 217: # WHILE
                self.procesar_while()
                
            elif tid == 112: # } CIERRE DE BLOQUE
                self.cerrar_bloque()
                self.avanzar()

            # --- SENTENCIAS Y ASIGNACIONES ---
            elif tid == 100: # Variable (posible asignación)
                if self.peek_token() == 121: 
                    # Procesamos hasta encontrar el punto y coma (122)
                    self.procesar_expresion(stop_tokens=[122]) 
                    if self.current and self.current.token_id == 122:
                        self.avanzar()
                else:
                    self.avanzar()

            # --- PRINT ---
            elif tid == 208: 
                self.procesar_print()

            # --- OTROS (Saltar tipos de datos, comas, etc) ---
            else:
                self.avanzar()
        
        # Al final, imprimimos la tabla
        self.tac.print_code()

    # ---------------------------------------------------------
    # MANEJO DE IF / ELSE
    # ---------------------------------------------------------
    def procesar_if(self):
        self.avanzar() # Consumir 'if'
        self.avanzar() # Consumir '('
        
        # 1. Evaluar Condición: Genera T1
        cond_temp = self.procesar_expresion(stop_tokens=[110])
        
        if self.current.token_id == 110: self.avanzar() # Consumir ')'
        
        # 2. Generar Salto BrF hacia etiqueta A (L_false)
        L_false = self.tac.new_label()
        self.tac.emit("BrF", cond_temp, None, L_false)
        
        # 3. Guardar etiqueta A en pila
        self.control_stack.append(("IF", L_false))

    def procesar_else(self):
        self.avanzar() # Consumir 'else'
        
        # Recuperamos la etiqueta A (fin del IF verdadero)
        if self.control_stack:
            tipo, L_false = self.control_stack.pop()
            
            # 4. Generar Salto Incondicional Br hacia etiqueta B (L_final)
            # Esto evita que el bloque IF ejecute también el ELSE
            L_final = self.tac.new_label()
            self.tac.emit("Br", None, None, L_final)
            
            # 5. Colocar etiqueta A aquí (Inicio del ELSE)
            self.tac.emit_label(L_false)
            
            # 6. Guardar etiqueta B para el cierre
            self.control_stack.append(("ELSE", L_final))

    # ---------------------------------------------------------
    # MANEJO DE WHILE
    # ---------------------------------------------------------
    def procesar_while(self):
        self.avanzar() # Consumir 'while'
        
        # 1. Etiqueta de Inicio (Para regresar)
        L_inicio = self.tac.new_label()
        self.tac.emit_label(L_inicio)
        
        self.avanzar() # Consumir '('
        cond_temp = self.procesar_expresion(stop_tokens=[110])
        
        # 2. Etiqueta de Salida
        L_salida = self.tac.new_label()
        self.tac.emit("BrF", cond_temp, None, L_salida)
        
        if self.current.token_id == 110: self.avanzar() # Consumir ')'
        
        # Guardamos ambas etiquetas
        self.control_stack.append(("WHILE", L_salida, L_inicio))

    # ---------------------------------------------------------
    # CIERRE DE BLOQUES '}'
    # ---------------------------------------------------------
    def cerrar_bloque(self):
        if self.control_stack:
            datos = self.control_stack.pop()
            tipo = datos[0]
            
            if tipo == "IF":
                # Si solo era IF, aquí va la etiqueta A
                L_salida = datos[1]
                self.tac.emit_label(L_salida)
                
            elif tipo == "ELSE":
                # Si era ELSE, aquí va la etiqueta B (Fin total)
                L_final = datos[1]
                self.tac.emit_label(L_final)
                
            elif tipo == "WHILE":
                L_salida = datos[1]
                L_inicio = datos[2]
                # Salto para volver arriba
                self.tac.emit("Br", None, None, L_inicio)
                # Etiqueta de salida
                self.tac.emit_label(L_salida)

    # ---------------------------------------------------------
    # EXPRESIONES Y UTILIDADES
    # ---------------------------------------------------------
    def procesar_expresion(self, stop_tokens):
        # Usamos tu Postfix para ordenar
        converter = PostfixConverter(self.current)
        rpn_list, nodo_final = converter.convertir(stop_tokens)
        
        # Usamos el ExprGen para crear T1, T2...
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
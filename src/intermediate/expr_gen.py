# src/intermediate/expr_gen.py
from src.table_types.table_types import SEMANTIC_MATRIX

class ExpressionGenerator:
    def __init__(self, tac_manager):
        self.tac = tac_manager

    def generar_desde_rpn(self, lista_rpn):
        """
        Recibe: lista de nodos RPN
        Imprime: La reducción paso a paso (Postfijo -> Temporal)
        """
        pila = []
        
        # Tokens de VALOR (Operandos)
        tokens_valor = [100, 101, 102, 103, 220, 221]

        for nodo in lista_rpn:
            lexema = nodo.lexema
            tid = nodo.token_id

            # 1. SI ES OPERANDO (a, 5, 3.14), SOLO ENTRA A LA PILA
            if tid in tokens_valor:
                pila.append(lexema)
            
            # 2. SI ES OPERADOR, REDUCIMOS
            else:
                if not pila: break 

                # --- CASO ASIGNACIÓN (=) ---
                if tid == 121: 
                    if len(pila) < 2: break
                    val = pila.pop()      # Lo que asignamos
                    dest = pila.pop()     # La variable
                    
                    # VISUALIZACIÓN:
                    print(f"\t[ASIGNACIÓN]: {dest} {val} = ")
                    
                    self.tac.emit("=", val, None, dest)
                    pila.append(dest) 
                
                # --- OPERACIONES BINARIAS (+, -, *, >, AND, etc) ---
                else:
                    if len(pila) < 2: break
                    der = pila.pop()
                    izq = pila.pop()
                    
                    temporal = self.tac.new_temp()
                    
                    # VISUALIZACIÓN CLAVE:
                    # Muestra: 'a b +' --> 't0'
                    print(f"\t[REDUCCIÓN ]: {izq} {der} {lexema}  -->  {temporal}")
                    
                    self.tac.emit(lexema, izq, der, temporal)
                    pila.append(temporal)
        
        return pila[0] if pila else None
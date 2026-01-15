# src/intermediate/expr_gen.py
from src.table_types.table_types import SEMANTIC_MATRIX

class ExpressionGenerator:
    def __init__(self, tac_manager):
        self.tac = tac_manager

    def generar_desde_rpn(self, lista_rpn):

        pila = []
        
        tokens_valor = [100, 101, 102, 103, 220, 221]

        for nodo in lista_rpn:
            lexema = nodo.lexema
            tid = nodo.token_id

            if tid in tokens_valor:
                pila.append(lexema)
            
            else:
                if not pila: break 

                if tid == 121: 
                    if len(pila) < 2: break
                    val = pila.pop()      
                    dest = pila.pop()     
                    
                    print(f"\t[ASIGNACIÓN]: {dest} {val} = ")
                    
                    self.tac.emit("=", val, None, dest)
                    pila.append(dest) 
                
                else:
                    if len(pila) < 2: break
                    der = pila.pop()
                    izq = pila.pop()
                    
                    temporal = self.tac.new_temp()
                    
                    print(f"\t[REDUCCIÓN ]: {izq} {der} {lexema}  -->  {temporal}")
                    
                    self.tac.emit(lexema, izq, der, temporal)
                    pila.append(temporal)
        
        return pila[0] if pila else None
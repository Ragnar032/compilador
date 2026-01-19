# src/intermediate/expr_gen.py
from src.table_types.table_types import SEMANTIC_MATRIX

class ExpressionGenerator:
    def __init__(self, tac_manager):
        self.tac = tac_manager

    def _es_numero(self, valor):
        if isinstance(valor, (int, float)):
            return True
        if isinstance(valor, str):
            try:
                float(valor)
                return True
            except ValueError:
                return False
        return False

    def _obtener_valor(self, valor):
        return float(valor)

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

                if tid == 121: # Asignación (=)
                    if len(pila) < 2: break
                    val = pila.pop()      
                    dest = pila.pop()     
                    
                    print(f"\t[ASIGNACIÓN]: {dest} = {val}")
                    self.tac.emit("=", val, None, dest)
                    pila.append(dest) 
                
                else: 
                    if len(pila) < 2: break
                    der = pila.pop()
                    izq = pila.pop()
                    
                    if self._es_numero(izq) and self._es_numero(der):
                        try:
                            v_izq = self._obtener_valor(izq)
                            v_der = self._obtener_valor(der)
                            resultado = 0

                            if lexema == '+': resultado = v_izq + v_der
                            elif lexema == '-': resultado = v_izq - v_der
                            elif lexema == '*': resultado = v_izq * v_der
                            elif lexema == '/': 
                                if v_der == 0: raise ZeroDivisionError
                                resultado = v_izq / v_der
                            

                            if resultado.is_integer():
                                resultado = int(resultado)
                            
                            print(f"\t[OPTIMIZACIÓN]: {izq} {lexema} {der} se redujo a {resultado}")

                            pila.append(resultado)
                            continue 
                            
                        except ZeroDivisionError:
                            print(f"\t[ADVERTENCIA]: División por cero detectada en optimización.")
                        except Exception as e:
                            print(f"\t[DEBUG]: No se pudo plegar: {e}")

                    temporal = self.tac.new_temp()
                    
                    print(f"\t[REDUCCIÓN ]: {izq} {lexema} {der}  -->  {temporal}")
                    
                    self.tac.emit(lexema, izq, der, temporal)
                    pila.append(temporal)
        
        return pila[0] if pila else None
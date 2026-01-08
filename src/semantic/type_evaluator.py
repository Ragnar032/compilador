# UBICACIÓN: src/semantic/type_evaluator.py
from src.table_types.table_types import SEMANTIC_MATRIX, INT, DBL, BOL, STR

class TypeEvaluator:
    def __init__(self, lista_variables):
        self.variables = lista_variables
        self.mapa_literales = { 101: INT, 102: DBL, 103: STR, 220: BOL, 221: BOL }

    def evaluar(self, lista_rpn):
        pila = [] 
        
        for nodo in lista_rpn:
            tid = nodo.token_id
            
            if tid in self.mapa_literales:
                pila.append({"tipo": self.mapa_literales[tid], "modo": "VALOR", "lexema": nodo.lexema})
            
            elif tid == 100:
                tipo = self.variables.get_variable_type(nodo.lexema)
                if not tipo:
                    print(f"[ERROR SEMÁNTICO] Línea {nodo.renglon}: Variable '{nodo.lexema}' no ha sido declarada.")
                    pila.append({"tipo": "error", "modo": "ID", "lexema": nodo.lexema})
                else:
                    pila.append({"tipo": tipo, "modo": "ID", "lexema": nodo.lexema})
            
            elif tid in SEMANTIC_MATRIX:
                if len(pila) < 2: 
                    return "error"
                
                der = pila.pop()
                izq = pila.pop()
                
                self._validar_y_operar(izq, tid, der, pila, nodo.renglon)
        
        if pila: 
            return pila[0]["tipo"]
        return "void"

    def _validar_y_operar(self, izq, op_id, der, pila, renglon):
        if izq["tipo"] == "error" or der["tipo"] == "error":
            pila.append({"tipo": "error", "modo": "VALOR"})
            return
        

        if op_id == 121 and izq["modo"] != "ID":
            print(f"[ERROR SEMÁNTICO] Línea {renglon}: No se puede asignar valor a una constante o expresión.")
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
class TargetGenerator:
    def __init__(self, tac_code):
        self.tac_code = tac_code
        self.output_asm = []
        self.variables = set()

    def recolectar_variables(self):
        for op, arg1, arg2, res in self.tac_code:
            if self.es_variable(arg1): self.variables.add(arg1)
            if self.es_variable(arg2): self.variables.add(arg2)
            if self.es_variable(res) and op != "LABEL": self.variables.add(res)

    def es_variable(self, val):
        """Helper para saber si es una variable que debe declararse"""
        if not val: return False
        s_val = str(val)
        if s_val.startswith("'") or s_val.startswith('"'): return False # Es string
        if s_val.replace("-", "").isdigit(): return False # Es numero
        if s_val.startswith("L") and s_val[1:].isdigit(): return False # Es etiqueta
        return True

    def generar_asm(self):
        self.recolectar_variables()

        self.output_asm.append("; PROYECTO COMPILADOR - CODIGO GENERADO")
        self.output_asm.append(".MODEL SMALL")
        self.output_asm.append(".STACK 100H")
        self.output_asm.append(".DATA")
        
        self.output_asm.append("\n    ; --- Variables del Usuario y Temporales ---")
        for var in sorted(self.variables):
            self.output_asm.append(f"    {var} DW 0")

        self.output_asm.append("\n    ; --- Variables requeridas por TUS MACROS (ITOA/ATOI) ---")
        self.output_asm.append("    BUFFERTEMP  DB 10 DUP('$')")
        self.output_asm.append("    BLANCOS     DB '$$$$'")
        self.output_asm.append("    NEGATIVO    DB 0")
        self.output_asm.append("    COUNT       DW 0")
        self.output_asm.append("    MENOS       DB '-$'")
        self.output_asm.append("    MULT10      DW 1")      
        self.output_asm.append("    TOTCAR      DB 0")      
        self.output_asm.append("    BUF         DW 10")     


        self.output_asm.append("\n.CODE")
        self.output_asm.append("INCLUDE macros.inc") 
        
        self.output_asm.append("\nMAIN PROC")
        self.output_asm.append("    MOV AX, @DATA")
        self.output_asm.append("    MOV DS, AX")
        self.output_asm.append("    MOV ES, AX")
        self.output_asm.append("\n    ; --- INICIO DEL LOGICA ---")


        for op, arg1, arg2, res in self.tac_code:
            
            if op == "+":
                self.output_asm.append(f"    SUMAR {arg1}, {arg2}, {res}")
            elif op == "-":
                self.output_asm.append(f"    RESTA {arg1}, {arg2}, {res}")
            elif op == "*":
                self.output_asm.append(f"    MULTI {arg1}, {arg2}, {res}")
            elif op == "/":
                self.output_asm.append(f"    DIVIDE {arg1}, {arg2}, {res}")
            
            elif op == "=":

                self.output_asm.append(f"    I_ASIGNAR {res}, {arg1}")

            elif op == "<":
                self.output_asm.append(f"    I_MENOR {arg1}, {arg2}, {res}")
            elif op == ">":
                self.output_asm.append(f"    I_MAYOR {arg1}, {arg2}, {res}")
            elif op == "<=":
                self.output_asm.append(f"    I_MENORIGUAL {arg1}, {arg2}, {res}")
            elif op == ">=":
                self.output_asm.append(f"    I_MAYORIGUAL {arg1}, {arg2}, {res}")
            elif op == "==":
                self.output_asm.append(f"    I_IGUAL {arg1}, {arg2}, {res}")
            elif op == "!=":
                self.output_asm.append(f"    I_DIFERENTES {arg1}, {arg2}, {res}")

            elif op == "LABEL":
                self.output_asm.append(f"\n{res}:")
            
            elif op == "Br": 
                self.output_asm.append(f"    JMP {res}")
            
            elif op == "BrF": 
                self.output_asm.append(f"    JF {arg1}, {res}")

            elif op == "print":
                self.output_asm.append(f"    ; Imprimir {res}")
                self.output_asm.append(f"    ITOA BUFFERTEMP, {res}")
                self.output_asm.append(f"    WRITE BUFFERTEMP")
                self.output_asm.append(f"    WRITELN")


        self.output_asm.append("\n    ; Fin del programa")
        self.output_asm.append("    MOV AX, 4C00H")
        self.output_asm.append("    INT 21H")
        self.output_asm.append("MAIN ENDP")
        self.output_asm.append("END MAIN")
        
        return "\n".join(self.output_asm)
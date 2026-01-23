class TargetGenerator:
    def __init__(self, tac_code):
        self.tac_code = tac_code
        self.output_asm = []
        self.variables = set()

        self.MACROS_STR = r"""
WRITE   MACRO MESSAGE
        PUSH AX
        MOV AH, 09H
        LEA DX, MESSAGE
        INT 21H
        POP AX
    ENDM

WRITELN MACRO
        MOV AH, 2
        MOV DL, 0AH
        INT 21H
        MOV AH, 2
        MOV DL, 0DH
        INT 21H
    ENDM

SUMAR   MACRO OPERANDO1, OPERANDO2, RESULTADO
        PUSH AX
        MOV AX, OPERANDO1
        ADD AX, OPERANDO2
        MOV RESULTADO, AX
        POP AX
    ENDM

RESTA   MACRO OPERANDO1, OPERANDO2, RESULTADO
        PUSH AX
        MOV AX, OPERANDO1
        SUB AX, OPERANDO2
        MOV RESULTADO, AX
        POP AX
    ENDM

MULTI   MACRO OPERANDO1, OPERANDO2, RESULTADO
        PUSH AX
        PUSH BX
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        IMUL BX
        MOV RESULTADO, AX
        POP BX
        POP AX
    ENDM

DIVIDE  MACRO OPERANDO1, OPERANDO2, RESULTADO
        PUSH AX
        PUSH BX
        MOV DX, 0
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        IDIV BX
        MOV RESULTADO, AX
        POP BX
        POP AX
    ENDM

I_ASIGNAR MACRO OPERANDO1, OPERANDO2
        PUSH AX
        MOV AX, OPERANDO2
        MOV OPERANDO1, AX
        POP AX
    ENDM

I_MENOR MACRO OPERANDO1, OPERANDO2, RESULTADO
    LOCAL LABEL1, SALIR
        PUSH AX
        PUSH BX
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        CMP AX, BX
        JGE LABEL1
        MOV AX, 1
        MOV RESULTADO, AX
        JMP SALIR
    LABEL1:
        MOV AX, 0
        MOV RESULTADO, AX
    SALIR:
        POP BX
        POP AX
    ENDM

I_MENORIGUAL MACRO OPERANDO1, OPERANDO2, RESULTADO
    LOCAL LABEL1, SALIR
        PUSH AX
        PUSH BX
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        CMP AX, BX
        JG  LABEL1
        MOV AX, 1
        MOV RESULTADO, AX
        JMP SALIR
    LABEL1:
        MOV AX, 0
        MOV RESULTADO, AX
    SALIR:
        POP BX
        POP AX
    ENDM

I_IGUAL MACRO OPERANDO1, OPERANDO2, RESULTADO
    LOCAL LABEL1, SALIR
        PUSH AX
        PUSH BX
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        CMP AX, BX
        JNE LABEL1
        MOV AX, 1
        MOV RESULTADO, AX
        JMP SALIR
    LABEL1:
        MOV AX, 0
        MOV RESULTADO, AX
    SALIR:
        POP BX
        POP AX
    ENDM

I_DIFERENTES MACRO OPERANDO1, OPERANDO2, RESULTADO
    LOCAL LABEL1, SALIR
        PUSH AX
        PUSH BX
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        CMP AX, BX
        JE  LABEL1
        MOV AX, 1
        MOV RESULTADO, AX
        JMP SALIR
    LABEL1:
        MOV AX, 0
        MOV RESULTADO, AX
    SALIR:
        POP BX
        POP AX
    ENDM

I_MAYOR MACRO OPERANDO1, OPERANDO2, RESULTADO
    LOCAL LABEL1, SALIR
        PUSH AX
        PUSH BX
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        CMP AX, BX
        JLE LABEL1
        MOV AX, 1
        MOV RESULTADO, AX
        JMP SALIR
    LABEL1:
        MOV AX, 0
        MOV RESULTADO, AX
    SALIR:
        POP BX
        POP AX
    ENDM

I_MAYORIGUAL MACRO OPERANDO1, OPERANDO2, RESULTADO
    LOCAL LABEL1, SALIR
        PUSH AX
        PUSH BX
        MOV AX, OPERANDO1
        MOV BX, OPERANDO2
        CMP AX, BX
        JL  LABEL1
        MOV AX, 1
        MOV RESULTADO, AX
        JMP SALIR
    LABEL1:
        MOV AX, 0
        MOV RESULTADO, AX
    SALIR:
        POP BX
        POP AX
    ENDM

JF  MACRO VALOR1, DESTINO
    MOV AX, VALOR1
    CMP AX, 1
    JNE DESTINO
    ENDM

ITOA    MACRO BUFFER, NUMERO
    LOCAL C1, C2, C3, C4, L_CLR
        PUSH CX
        PUSH AX
        PUSH BX
        PUSH SI
        PUSH DI
        PUSH DX
        MOV CX, 10
        LEA SI, BUFFER
    L_CLR:
        MOV BYTE PTR [SI], '$' 
        INC SI
        LOOP L_CLR
        MOV COUNT, 0
        MOV CX, 10
        LEA SI, BUFFER
        MOV AX, NUMERO
        CMP AX, 0
        JNS C1
        NOT AX
        INC AX
        MOV NEGATIVO, 1
    C1:
        CMP AX, CX
        JB C2
        XOR DX, DX
        DIV CX
        OR  DL, 30H
        MOV [SI], DL
        INC SI
        INC COUNT
        JMP C1
    C2:
        OR AL, 30H
        MOV [SI], AL
        LEA SI, BUFFER
        LEA DI, BUFFERTEMP
        MOV BX, COUNT
        PUSH BX
    C3:
        MOV AL, [SI]
        MOV [BX+DI], AL
        INC SI
        CMP BX, 0
        DEC BX
        JG C3
        MOV AL, [SI]
        MOV [BX+DI], AL
        CMP NEGATIVO, 0
        JE  C4
        MOV AL, '-'
        MOV [BX+DI+1], AL
    C4:
        POP BX
        MOV AL, '$'
        MOV [BX+DI+1], AL 
        POP DX
        POP DI
        POP SI
        POP BX
        POP CX
        POP AX
    ENDM
"""

    def recolectar_variables(self):
        for op, arg1, arg2, res in self.tac_code:
            s_op = str(op).strip()
            if self.es_variable(arg1): self.variables.add(arg1)
            if self.es_variable(arg2): self.variables.add(arg2)
            if self.es_variable(res) and s_op != "LABEL": self.variables.add(res)

    def es_variable(self, val):
        if not val: return False
        s_val = str(val)
        if s_val.startswith('"'): return False
        if s_val.replace("-", "").isdigit(): return False
        if s_val.startswith("L") and s_val[1:].isdigit(): return False
        return True

    def generar_asm(self):
        self.recolectar_variables()
        
        self.output_asm.append(".MODEL SMALL")
        self.output_asm.append(".STACK 100H")
        self.output_asm.append(".DATA")
        
        for var in sorted(self.variables):
            self.output_asm.append(f"    {var} DW 0")

        self.output_asm.append("    BUFFERTEMP  DB 12 DUP('$')") 
        self.output_asm.append("    DIGITOS     DB 12 DUP('$')") 
        self.output_asm.append("    BLANCOS     DB '$$$$'")
        self.output_asm.append("    NEGATIVO    DB 0")
        self.output_asm.append("    COUNT       DW 0")
        self.output_asm.append("    MENOS       DB '-$'")
        self.output_asm.append("    MULT10      DW 1")
        self.output_asm.append("    TOTCAR      DB 0")
        self.output_asm.append("    BUF         DW 10") 

        self.output_asm.append("\n.CODE")
        self.output_asm.append(self.MACROS_STR) 
        
        self.output_asm.append("\nMAIN PROC")
        self.output_asm.append("    MOV AX, @DATA")
        self.output_asm.append("    MOV DS, AX")
        self.output_asm.append("    MOV ES, AX")
        
        print("\n[DEBUG] --- INICIANDO TRADUCCIÓN LÍNEA POR LÍNEA ---")
        
        for op, arg1, arg2, res in self.tac_code:
            original_op = op
            op = str(op).strip()
            
            print(f"[DEBUG] Procesando: '{original_op}' -> '{op}'")

            if op == "+": self.output_asm.append(f"    SUMAR {arg1}, {arg2}, {res}")
            elif op == "-": self.output_asm.append(f"    RESTA {arg1}, {arg2}, {res}")
            elif op == "*": self.output_asm.append(f"    MULTI {arg1}, {arg2}, {res}")
            elif op == "/": self.output_asm.append(f"    DIVIDE {arg1}, {arg2}, {res}")
            elif op == "=": self.output_asm.append(f"    I_ASIGNAR {res}, {arg1}")
            
            elif op == "<": self.output_asm.append(f"    I_MENOR {arg1}, {arg2}, {res}")
            elif op == ">": self.output_asm.append(f"    I_MAYOR {arg1}, {arg2}, {res}")
            elif op == "<=": self.output_asm.append(f"    I_MENORIGUAL {arg1}, {arg2}, {res}")
            elif op == ">=": self.output_asm.append(f"    I_MAYORIGUAL {arg1}, {arg2}, {res}")
            elif op == "==": self.output_asm.append(f"    I_IGUAL {arg1}, {arg2}, {res}")
            elif op == "!=": self.output_asm.append(f"    I_DIFERENTES {arg1}, {arg2}, {res}")            
            
            elif op == "LABEL": self.output_asm.append(f"\n{res}:")
            elif op == "Br": self.output_asm.append(f"    JMP {res}")
            elif op == "BrF": self.output_asm.append(f"    JF {arg1}, {res}")
            elif op == "print":
                self.output_asm.append(f"    ITOA DIGITOS, {res}")
                self.output_asm.append(f"    WRITE BUFFERTEMP")
                self.output_asm.append(f"    WRITELN")
            else:
                print(f"[ALERTA] Operador desconocido o ignorado: '{op}'")

        self.output_asm.append("\n    MOV AX, 4C00H")
        self.output_asm.append("    INT 21H")
        self.output_asm.append("MAIN ENDP")
        self.output_asm.append("END MAIN")
        
        return "\n".join(self.output_asm)
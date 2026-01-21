.MODEL SMALL
.STACK 100H
.DATA
    T1 DW 0
    T2 DW 0
    T3 DW 0
    T4 DW 0
    T5 DW 0
    a DW 0
    b DW 0
    resultado DW 0
    suma DW 0
    x DW 0
    BUFFERTEMP  DB 12 DUP('$')
    DIGITOS     DB 12 DUP('$')
    BLANCOS     DB '$$$$'
    NEGATIVO    DB 0
    COUNT       DW 0
    MENOS       DB '-$'
    MULT10      DW 1
    TOTCAR      DB 0
    BUF         DW 10

.CODE

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


MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX
    I_ASIGNAR a, 10
    I_ASIGNAR b, 10
    SUMAR a, b, T1
    I_ASIGNAR suma, T1
    ITOA DIGITOS, suma
    WRITE BUFFERTEMP
    WRITELN
    MULTI suma, 5, T2
    I_ASIGNAR resultado, T2
    ITOA DIGITOS, resultado
    WRITE BUFFERTEMP
    WRITELN
    I_MAYOR resultado, 54, T3
    JF T3, L0
    ITOA DIGITOS, 1111
    WRITE BUFFERTEMP
    WRITELN
    I_ASIGNAR x, 1

L1:
    I_MENOR x, 5, T4
    JF T4, L2
    SUMAR x, 1, T5
    I_ASIGNAR x, T5
    JMP L1

L2:
    I_ASIGNAR resultado, x
    JMP L3

L0:
    ITOA DIGITOS, 2222
    WRITE BUFFERTEMP
    WRITELN
    I_ASIGNAR resultado, 0

L3:
    ITOA DIGITOS, resultado
    WRITE BUFFERTEMP
    WRITELN

    MOV AX, 4C00H
    INT 21H
MAIN ENDP
END MAIN
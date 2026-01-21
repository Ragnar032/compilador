; PROYECTO COMPILADOR - CODIGO GENERADO
.MODEL SMALL
.STACK 100H
.DATA

    ; --- Variables del Usuario y Temporales ---
    T1 DW 0
    T2 DW 0
    T3 DW 0
    T4 DW 0
    T5 DW 0
    a DW 0
    b DW 0
    resultado DW 0
    variableGlobal DW 0
    x DW 0

    ; --- Variables requeridas por TUS MACROS (ITOA/ATOI) ---
    BUFFERTEMP  DB 10 DUP('$')
    BLANCOS     DB '$$$$'
    NEGATIVO    DB 0
    COUNT       DW 0
    MENOS       DB '-$'
    MULT10      DW 1
    TOTCAR      DB 0
    BUF         DW 10

.CODE
INCLUDE macros.inc

MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX

    ; --- INICIO DEL LOGICA ---
    I_ASIGNAR variableGlobal, 100
    I_ASIGNAR a, 10
    I_ASIGNAR b, 10
    SUMAR a, b, T1
    MULTI T1, 5, T2
    I_ASIGNAR resultado, T2
    JF T3, L0
    I_ASIGNAR x, 1

L1:
    JF T4, L2
    SUMAR x, 1, T5
    I_ASIGNAR x, T5
    JMP L1

L2:

L0:
    I_ASIGNAR resultado, 0
    ; Imprimir resultado
    ITOA BUFFERTEMP, resultado
    WRITE BUFFERTEMP
    WRITELN

    ; Fin del programa
    MOV AX, 4C00H
    INT 21H
MAIN ENDP
END MAIN
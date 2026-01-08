# table_type.py

INT, DBL, BOL, STR = "int", "double", "boolean", "String"


# Regla para +, -, *
OP_ARITMETICA = {
    INT: {INT: INT, DBL: DBL},
    DBL: {INT: DBL, DBL: DBL}
}

# Regla para /
OP_DIVISION = {
    INT: {INT: DBL, DBL: DBL},
    DBL: {INT: DBL, DBL: DBL}
}

# Regla para %
OP_MODULO = {
    INT: {INT: INT, DBL: INT},
    DBL: {INT: INT, DBL: INT}
}

# Regla para >, <, >=, <=
OP_COMP_NUM = {
    INT: {INT: BOL, DBL: BOL},
    DBL: {INT: BOL, DBL: BOL}
}

# Regla para ==, != 
OP_IGUALDAD = {
    **OP_COMP_NUM,           
    BOL: {BOL: BOL},
    STR: {STR: BOL}
}
SEMANTIC_MATRIX = {}

# Asignación de Aritméticos
SEMANTIC_MATRIX[104] = OP_ARITMETICA 
SEMANTIC_MATRIX[105] = OP_ARITMETICA 
SEMANTIC_MATRIX[106] = OP_ARITMETICA 
SEMANTIC_MATRIX[107] = OP_DIVISION   
SEMANTIC_MATRIX[108] = OP_MODULO     

# Asignación de Relacionales (>, <, >=, <=)
for op_id in [117, 118, 119, 120]:
    SEMANTIC_MATRIX[op_id] = OP_COMP_NUM

# Asignación de Igualdad (==, !=)
for op_id in [115, 116]:
    SEMANTIC_MATRIX[op_id] = OP_IGUALDAD

# Asignación de Lógicos
SEMANTIC_MATRIX[205] = {BOL: {BOL: BOL}} 
SEMANTIC_MATRIX[206] = {BOL: {BOL: BOL}} 
SEMANTIC_MATRIX[207] = {BOL: BOL}        

# Asignación (=)
SEMANTIC_MATRIX[121] = {
    INT: {INT: INT, INT: DBL, DBL: INT},
    DBL: {INT: DBL, DBL: DBL},
    BOL: {BOL: BOL},
    STR: {STR: STR}
}
class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        
        self.reserved_words = {
            "int": 200, "double": 201, "boolean": 202, "String": 203, "void": 204,
            "and": 205, "or": 206, "not": 207, "print": 208, "class": 209,
            "public": 210, "private": 211, "static": 212, "main": 213, "return": 214,
            "if": 215, "else": 216, "while": 217, "for": 218, "break": 219,
            "TRUE": 220, "FALSE": 221
        }
        self.token_names = {
            100: "IDENTIFICADOR", 
            101: "ENTERO", 
            102: "REAL", 
            103: "CADENA",
            104: "SUMA", 
            105: "RESTA", 
            106: "MULT", 
            107: "DIV", 
            108: "MODULO",
            109: "L_PAREN", 
            110: "R_PAREN", 
            111: "L_LLAVE", 
            112: "R_LLAVE",
            113: "L_CORCHETE", 
            114: "R_CORCHETE", 
            115: "IGUAL_QUE", 
            116: "DIFERENTE",
            117: "MAYOR_IGUAL", 
            118: "MENOR_IGUAL", 
            119: "MAYOR", 
            120: "MENOR",
            121: "ASIGNACION", 
            122: "PUNTO_COMA",
            123: "COMA",         
            124: "PUNTO",
            **{v: k for k, v in self.reserved_words.items()},
            500: "ERR_INVALIDO", 
            501: "ERR_NUMERO", 
            502: "ERR_OPERADOR", 
            503: "ERR_STRING"
        }
      
  
        self.matrix = [
            [1, 2, 500, 124, 123, 122, 5, 104, 105, 106, 6, 108, 11, 12, 10, 9, 109, 110, 111, 112, 113, 114, 0, 0, 0, 0, 500],
            [1, 1, 1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
            [101, 2, 101, 3, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101],
            [501, 4, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501, 501],
            [102, 4, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102],
            [5, 5, 5, 5, 5, 5, 103, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 503, 5, 5, 5],
            [107, 107, 107, 107, 107, 107, 107, 107, 107, 7, 0, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 115, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121],
            [502, 502, 502, 502, 121, 121, 502, 502, 502, 502, 502, 502, 502, 502, 502, 116, 502, 502, 502, 502, 502, 502, 502, 502, 502, 502, 502],
            [119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 117, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119],            
            [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 118, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
        ]

    def get_column(self, char):
        if char.isalpha(): return 0       # l
        if char.isdigit(): return 1       # d
        if char == '_': return 2          # _
        if char == '.': return 3          # .
        if char == ',': return 4          # ,
        if char == ';': return 5          # ; 
        if char == '"': return 6          # "
        if char == '+': return 7          # +
        if char == '-': return 8          # -
        if char == '*': return 9          # *
        if char == '/': return 10         # /
        if char == '%': return 11         # %
        if char == '>': return 12         # >
        if char == '<': return 13         # <
        if char == '!': return 14         # !
        if char == '=': return 15         # =
        if char == '(': return 16         # (
        if char == ')': return 17         # )
        if char == '{': return 18         # {
        if char == '}': return 19         # }
        if char == '[': return 20         # [
        if char == ']': return 21         # ]
        if char == ' ': return 22         # eb
        if char == '\n': return 23        # nl
        if char == '\t': return 24        # tab
        if char == '\0': return 25        # eof
        return 26                         # oc

    def get_next_token(self):
        state = 0
        lexeme = ""
        
        while self.pos < len(self.source) + 1:
            char = self.source[self.pos] if self.pos < len(self.source) else '\0'
            col = self.get_column(char)
            
            if state >= len(self.matrix): break
            
            if state == 6 and char == '/':
                 self.pos += 1 
                 while self.pos < len(self.source) and self.source[self.pos] != '\n':
                     self.pos += 1
                 state = 0
                 lexeme = ""
                 continue

            next_state = self.matrix[state][col]
            
            if next_state < 100:
                if state == 0 and next_state == 0:
                    self.pos += 1
                    continue
                state = next_state
                lexeme += char
                self.pos += 1
            else:
                final_token_id = next_state
                
                if next_state == 100:
                    if lexeme in self.reserved_words:
                        final_token_id = self.reserved_words[lexeme]

                token_name = self.token_names.get(final_token_id, "DESCONOCIDO")
                
                
                if state not in [0, 5, 6, 9, 10, 11, 12]:
                     return (final_token_id, token_name, lexeme)
                else:
                    lexeme += char
                    self.pos += 1
                    return (final_token_id, token_name, lexeme)
                    
        return None
# --- PRUEBA FINAL ---
codigo = """
    // Variables
    int x = 10;
    double y = 20.5;
    if (x!=y) {
    // Imprimir
    print("Hola Mundo");
    }
    """

lexer = Lexer(codigo)
print(f"{'token':<5} {'Des':<15} {'lexema'}")
print("-" * 40)

while True:
    token = lexer.get_next_token()
    if token:
        print(f"{token[0]:<5} {token[1]:<15} {token[2]}")
    else:
        break
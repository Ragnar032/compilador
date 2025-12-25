from src.lexer.matrix import MATRIX
from src.lexer.reserved import RESERVED_WORDS
from src.lexer.tokens import TOKENS
from src.lexer.node import Node
from src.lexer.errors import ERRORS

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        
        self.matrix = MATRIX
        self.reserved_words = RESERVED_WORDS
        self.tokens = TOKENS
        self.errors = ERRORS
        
        self.head = None
        self.tail = None

    def get_column(self, char):
        if char.isalpha(): return 0       
        if char.isdigit(): return 1       
        if char == '_': return 2          
        if char == '.': return 3          
        if char == ',': return 4          
        if char == ';': return 5          
        if char == '"': return 6          
        if char == '+': return 7          
        if char == '-': return 8          
        if char == '*': return 9          
        if char == '/': return 10         
        if char == '%': return 11         
        if char == '>': return 12         
        if char == '<': return 13         
        if char == '!': return 14         
        if char == '=': return 15         
        if char == '(': return 16         
        if char == ')': return 17         
        if char == '{': return 18         
        if char == '}': return 19         
        if char == '[': return 20         
        if char == ']': return 21         
        if char == ' ': return 22         
        if char == '\n': return 23        
        if char == '\t': return 24        
        if char == '\0': return 25        
        return 26    

    def agregar_nodo(self, lexema, token_id, renglon):
        nuevo = Node(lexema, token_id, renglon)
        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
        else:
            self.tail.siguiente = nuevo
            self.tail = nuevo

    def run(self):
        state = 0
        lexeme = ""
        start_line = self.line 
        
        while self.pos < len(self.source) + 1:
            char = self.source[self.pos] if self.pos < len(self.source) else '\0'
            col = self.get_column(char)
            
            if state >= len(self.matrix): break
            
            if state == 0 and char not in [' ', '\t', '\n']:
                start_line = self.line

            if state == 6 and char == '/':
                 self.pos += 1 
                 while self.pos < len(self.source) and self.source[self.pos] != '\n':
                     self.pos += 1
                 state = 0
                 lexeme = ""
                 continue

            next_state = self.matrix[state][col]
            
            if next_state < 100:
                
                if state == 8 and char == '/':
                    state = 0  
                    lexeme = ""     
                    self.pos += 1   
                    continue        

                if state == 0 and next_state == 0:
                    if char == '\n': self.line += 1
                    self.pos += 1
                    start_line = self.line 
                    continue
                
                state = next_state
                if char != '\0': lexeme += char
                if char == '\n': self.line += 1
                self.pos += 1
            else:
                final_token_id = next_state
                
                if next_state == 100:
                    if lexeme in self.reserved_words:
                        final_token_id = self.reserved_words[lexeme]

                nodo_lexema = lexeme
                nodo_linea = self.line

                if final_token_id in [505, 507]:
                    nodo_linea = start_line
                    nodo_lexema = (lexeme[:15] + '...') if len(lexeme) > 15 else lexeme

                if state not in [0, 5, 6, 9, 10, 11, 12] and final_token_id < 500:
                    nodo_linea = self.line 
                    self.agregar_nodo(nodo_lexema, final_token_id, nodo_linea)
                else:
                    if char != '\0': lexeme += char
                    if char == '\n': self.line += 1
                    self.pos += 1
                    nodo_lexema = lexeme
                    self.agregar_nodo(nodo_lexema, final_token_id, start_line)

                state = 0
                lexeme = ""
                start_line = self.line
        
        return self.head
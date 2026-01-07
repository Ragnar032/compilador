# src/semantic/postfix.py

class PostfixConverter:
    def __init__(self, start_node):
        self.current = start_node
        self.output_queue = []
        self.operator_stack = []
        
        self.precedencia = {
            106: 4, 107: 4, 108: 4, # * / %
            104: 3, 105: 3,         # + -
            117: 2, 118: 2, 119: 2, 120: 2, 115: 2, 116: 2, # > < >= <= == !=
            121: 1,                 # = 
            109: 0                  # (
        }

    def convertir(self, stop_tokens=[122]):
    
        while self.current and self.current.token_id not in stop_tokens:
            token = self.current
            tid = token.token_id
            
            
            if tid == 100 or tid in [101, 102, 103, 220, 221]:
                self.output_queue.append(token)
            
            elif tid == 109:
                self.operator_stack.append(token)
            
            elif tid == 110:
                while self.operator_stack and self.operator_stack[-1].token_id != 109:
                    self.output_queue.append(self.operator_stack.pop())
                if self.operator_stack:
                    self.operator_stack.pop() 
         
            elif tid in self.precedencia:
                curr_prec = self.precedencia[tid]
                while (self.operator_stack and 
                       self.operator_stack[-1].token_id in self.precedencia and
                       self.precedencia[self.operator_stack[-1].token_id] >= curr_prec):
                    self.output_queue.append(self.operator_stack.pop())
                self.operator_stack.append(token)
            
            self.current = self.current.siguiente

        while self.operator_stack:
            self.output_queue.append(self.operator_stack.pop())
            
        return self.output_queue, self.current
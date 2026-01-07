# src/semantic/variable_list.py

class ListaVariables:
    def __init__(self):
        self.scopes = [{}] 

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1: self.scopes.pop()

    def add_variable(self, name, type_str, line):
        current_scope = self.scopes[-1]
        
        if name in current_scope:
            raise Exception(f"Línea {line}: La variable '{name}' ya existe en este ámbito.")
        
        current_scope[name] = {"type": type_str, "line": line}

    def get_variable_type(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]["type"]
        return None
# src/intermediate/tac_manager.py

class TacManager:
    def __init__(self):
        self.code = []
        self.temp_count = 1  # Empezamos en T1
        self.label_count = 0

    def new_temp(self):
        """Genera T1, T2, T3..."""
        t = f"T{self.temp_count}"
        self.temp_count += 1
        return t

    def new_label(self):
        """Genera L0, L1, L2... (Equivalentes a tus A, B)"""
        l = f"L{self.label_count}"
        self.label_count += 1
        return l

    def emit(self, op, arg1=None, arg2=None, res=None):
        self.code.append((op, arg1, arg2, res))

    def emit_label(self, label):
        # Guardamos la etiqueta como una instrucción especial
        self.code.append(("LABEL", None, None, label))

    def print_code(self):
        print("\n" + "="*60)
        print(f"{'TABLA DE CUÁDRUPLOS':^60}")
        print("="*60)
        print(f"{'OP':<10} | {'OP1':<10} | {'OP2':<10} | {'RES':<10}")
        print("-" * 60)

        for op, arg1, arg2, res in self.code:
            if op == "LABEL":
                # Imprimimos la etiqueta sola (ej: "L0:")
                print(f"{res + ':':<10} | {'':<10} | {'':<10} | {'':<10}")
            else:
                s_op = str(op)
                s_a1 = str(arg1) if arg1 is not None else ""
                s_a2 = str(arg2) if arg2 is not None else ""
                s_res = str(res) if res is not None else ""
                
                print(f"{s_op:<10} | {s_a1:<10} | {s_a2:<10} | {s_res:<10}")
        
        print("="*60 + "\n")
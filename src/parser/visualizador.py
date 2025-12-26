# src/parser/visualizador.py

def generar_codigo_dot(ast):
    """
    Genera un grafo detallado donde el '=' es un nodo y se muestran todos los elementos.
    """
    lineas = []
    lineas.append("digraph AST {")
    lineas.append('  node [shape=box, style=filled, color="#E1F5FE", fontname="Arial", fontsize=11];')
    lineas.append('  edge [color="#546E7A", arrowsize=0.8];')
    lineas.append('  rankdir=TB;')

    def obtener_etiqueta(nodo):
        tipo = nodo.get("tipo", "")
        
        if tipo == "ClasePrincipal":
            return f"Clase: {nodo.get('nombre')}"
        if tipo == "MetodoMain":
            return "Metodo: main"
        if tipo == "Declaracion":
            # Si hay valor, el nodo principal es la declaración del tipo
            return f"Variable: {nodo.get('id')}\\n[{nodo.get('dt')}]"
        if tipo == "Asignacion":
            return "=" # El nodo es el operador de asignación
        if tipo == "Impresion":
            return "print"
        if tipo == "OperacionBinaria":
            return f"{nodo.get('op')}" # +, -, *, /, >, <, etc.
        if tipo == "Literal":
            return f"{nodo.get('valor')}"
        if tipo == "VariableUso": # Para cuando usas una variable en una expresión
            return f"{nodo.get('id')}"
        if tipo == "If":
            return "if"
        if tipo == "While":
            return "while"
        
        return tipo

    def recorrer(sub_nodo, id_padre=None):
        if not isinstance(sub_nodo, dict):
            return

        # Saltar nodo Programa para ir directo a la clase
        if sub_nodo.get("tipo") == "Programa":
            contenido = sub_nodo.get("contenido")
            if isinstance(contenido, dict):
                recorrer(contenido, id_padre)
            return

        id_actual = f"n{id(sub_nodo)}"
        etiqueta = obtener_etiqueta(sub_nodo)
        lineas.append(f'  {id_actual} [label="{etiqueta}"];')

        if id_padre:
            lineas.append(f'  {id_padre} -> {id_actual};')

        # Si es una asignación o declaración con valor, queremos ver el '=' explícito
        tipo = sub_nodo.get("tipo")
        
        # Lógica especial para mostrar el '=' en declaraciones
        if tipo == "Declaracion" and sub_nodo.get("valor"):
            id_igual = f"eq{id(sub_nodo)}"
            lineas.append(f'  {id_igual} [label="=", color="#FFF9C4"];')
            lineas.append(f'  {id_actual} -> {id_igual};')
            recorrer(sub_nodo.get("valor"), id_igual)
            return # Ya procesamos los hijos por esta vía especial

        # Definir qué campos explorar para buscar hijos en el resto de los casos
        claves_hijos = ["cuerpo", "sentencias", "bloque_if", "bloque_else", 
                        "valor", "argumento", "condicion", "izq", "der"]

        for clave in claves_hijos:
            hijo = sub_nodo.get(clave)
            if isinstance(hijo, list):
                for item in hijo:
                    recorrer(item, id_actual)
            elif isinstance(hijo, dict):
                recorrer(hijo, id_actual)

    recorrer(ast)
    lineas.append("}")
    return "\n".join(lineas)
import os

class ManagerLexer:
    
    @staticmethod
    def leer_archivo(ruta_entrada):
        if not os.path.exists(ruta_entrada):
            print(f"ERROR: No se encontró el archivo: {ruta_entrada}")
            return None
            
        try:
            with open(ruta_entrada, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error crítico leyendo archivo: {e}")
            return None

    @staticmethod
    def exportar_reporte(cabeza_lista, ruta_salida):
        # Crear carpeta si no existe
        carpeta = os.path.dirname(ruta_salida)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        try:
            with open(ruta_salida, "w", encoding="utf-8") as f:
                # Encabezados (3 columnas: Lexema, Token, Renglon)
                header = f"{'LEXEMA':<30} {'TOKEN':<10} {'RENGLON':<10}"
                linea_sep = "-" * 55 
                
                print(f"\n{header}")
                print(linea_sep)
                
                f.write(f"{header}\n{linea_sep}\n")

                actual = cabeza_lista
                
                while actual is not None:
                    # Imprimir datos
                    fila = f"{actual.lexema:<30} {actual.token_id:<10} {actual.renglon:<10}"
                    
                    print(fila)
                    f.write(fila + "\n")
                    
                    # Avanzar puntero
                    actual = actual.siguiente
            
            print(f"\n[EXITO] Reporte generado en: {ruta_salida}")
            
        except Exception as e:
            print(f"Error escribiendo reporte: {e}")
# tests/test_sintactico.py
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Sintactico

def analizar(codigo):
    lexer = Lexer(codigo)
    tokens = lexer.run()
    parser = Sintactico(tokens)
    return parser.programa()

# ==========================================================
# 1. PRUEBAS DE ÉXITO (Corregidas para ser consistentes)
# ==========================================================
class TestSintacticoExito:

    def test_exito_completo_1(self):
        codigo = """
        public class MiPrograma {
            public static void main() {
                int x = 10;
                double y = (x + 5) * 2.5;
                print(y);
            }
        }
        """
        assert analizar(codigo)["tipo"] == "Programa"

    def test_exito_asignaciones_multiples(self):
        codigo = """
        public class Datos {
            public static void main() {
                String msg = "hola";
                boolean flag = true;
                x = 100;
            }
        }
        """
        assert analizar(codigo) is not None

# ==========================================================
# 2. PRUEBAS DE ERROR Y SUGERENCIAS (Lo nuevo)
# ==========================================================
class TestSintacticoErrores:

    def test_verificar_sugerencia_mayusculas(self):
        """Prueba específica para ver si el compilador ayuda al usuario"""
        codigo = "Public class Test {}" # 'Public' con P mayúscula
        with pytest.raises(Exception) as e:
            analizar(codigo)
        
        mensaje = str(e.value)
        print(f"\nReporte generado: {mensaje}")
        assert "💡" in mensaje
        assert "public" in mensaje

    def test_error_punto_coma_faltante(self):
        codigo = "public class T { public static void main() { int x = 5 } }"
        with pytest.raises(Exception) as e: analizar(codigo)
        assert "PUNTO_COMA" in str(e.value)

    def test_error_main_incompleto(self):
        """Error: falta 'void'"""
        codigo = "public class T { public static main() { } }"
        with pytest.raises(Exception) as e: analizar(codigo)
        assert "void" in str(e.value)

    def test_error_expresion_sin_cerrar(self):
        codigo = "public class T { public static void main() { x = (5 + 2; } }"
        with pytest.raises(Exception) as e: analizar(codigo)
        assert "R_PAREN" in str(e.value)
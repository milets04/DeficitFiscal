# src/utils.py
import numpy as np

def limpiar_numero(x):
    """
    Convierte números con formato latino:
    '1.234,56' -> 1234.56
    '1234,56'  -> 1234.56
    """
    try:
        if isinstance(x, str):
            x = x.replace(".", "").replace(",", ".")
        return float(x)
    except:
        return 0.0


def proyeccion_estocastica(base, volatilidad):
    """
    Genera una proyección aleatoria con distribución normal.
    base: valor inicial
    volatilidad: desviación como porcentaje (0.1 = 10%)
    """
    try:
        shock = np.random.normal(1, volatilidad)
        resultado = base * shock
        return max(resultado, 0)  # evita valores negativos
    except:
        return base

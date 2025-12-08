import numpy as np


# ----------- SHOCKS TRIANGULARES Y NORMALES -------------


def shock_precio_gas(base):
    base = float(base)
    return np.random.triangular(0.8 * base, base, 1.2 * base)

def shock_precio_minerales(base):
    base = float(base)
    return np.random.triangular(0.75 * base, base, 1.25 * base)


def shock_remesas(base):
    base = float(base)
    return np.random.normal(base, 0.05 * base)


def shock_pib():
    return np.random.normal(0.03, 0.02)

def shock_riesgo_pais(base):
    base = float(base)
    return np.random.triangular(0.8 * base, base, 1.4 * base)

def shock_tipo_cambio(base):
    base = float(base)
    return np.random.triangular(0.95 * base, base, 1.10 * base)
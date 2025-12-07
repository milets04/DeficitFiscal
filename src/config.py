import numpy as np


# ------------------ CONFIGURACIÓN GENERAL ------------------
N_SIMULACIONES = 1000
ANIOS = [2020, 2021, 2022, 2023, 2024, 2025]


# ------------------ PARÁMETROS ESTRUCTURALES ------------------
PARAMETROS = {
    "presion_tributaria": 0.28,
    "propension_consumo": 0.75,
    "sensibilidad_inversion": 0.20,
    "participacion_gas": 0.45,
    "participacion_mineria": 0.35,
    "umbral_crisis": 0.80,
}


# ------------------ COLUMNAS ESPERADAS EN EL CSV ------------------
COLUMNAS = {
    "anio": "Año",
    "pib": "PIB",
    "gasto": "Gasto público",
    "recaudacion": "Recaudación tributaria",
    "precio_gas": "Precio gas",
    "precio_min": "Precio minerales",
    "deuda_int": "Deuda interna",
    "deuda_ext": "Deuda externa",
    "tc": "Tipo de cambio (bs/usd)",
    "remesas": "Remesas",
    "riesgo": "Riesgo país"
}
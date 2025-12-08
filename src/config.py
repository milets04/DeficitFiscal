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
# Las claves deben coincidir con los encabezados exactos del CSV (acentos y espacios)
COLUMNAS = {
    "anio": "Año",
    "pib": "PIB (Millones USD)",
    "crecimiento": "Crecimiento PIB (%)",
    "gasto": "Gasto Público (Millones USD)",
    "recaudacion": "Recaudación Tributaria (Millones USD)",

    "precio_gas": "Precio Gas (USD por 1000 pies cúbicos)",
    "cantidad_gas": "Exportación Gas (Millones pies cúbicos)",

    "precio_min": "Precio Oro (USD/Ton)",
    "cantidad_min": "Exp. Oro (Ton)",

    "deuda_int": "Deuda Interna (Millones USD)",
    "intereses_int": "Int. Deuda Interna (Millones USD)",

    "deuda_ext": "Deuda Externa (Millones USD)",
    "intereses_ext": "Int. Deuda Externa (Millones USD)",

    "tasa_int": "Tasa Int. Internacional (%)",

    "amort_int": "Amortización Deuda Interna (Millones USD)",
    "amort_ext": "Amortización Deuda Externa (Millones USD)",

    "tipo_cambio": "Tipo de Cambio (Bs/USD)",
    "remesas": "Remesas (Millones USD)",
    "subsidios": "Subsidios (Millones USD)",

    "riesgo": "Riesgo País (Puntos Básicos)",

    "exportaciones": "Exp. Totales (Millones USD)",
    "importaciones": "Imp. Totales (Millones USD)"
}


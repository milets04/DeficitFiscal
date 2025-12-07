import pandas as pd
import numpy as np
from src.config import N_SIMULACIONES, ANIOS, COLUMNAS
from src.shocks import *
from src.agentes import *

def ejecutar_simulacion(df):
    resultados = np.zeros((N_SIMULACIONES, len(ANIOS)))

    for i in range(N_SIMULACIONES):
        deuda_total = df[COLUMNAS["deuda_int"]].iloc[0] + df[COLUMNAS["deuda_ext"]].iloc[0]
        pib = df[COLUMNAS["pib"]].iloc[0]

    for t in range(len(ANIOS)):
        precio_gas = shock_precio_gas(df[COLUMNAS["precio_gas"]].iloc[t])
        precio_min = shock_precio_minerales(df[COLUMNAS["precio_min"]].iloc[t])
        remesas = shock_remesas(df[COLUMNAS["remesas"]].iloc[t])
        riesgo = shock_riesgo_pais(df[COLUMNAS["riesgo"]].iloc[t])
        tc = shock_tipo_cambio(df[COLUMNAS["tc"]].iloc[t])


    ingresos, deficit = gobierno(pib, df[COLUMNAS["gasto"]].iloc[t], precio_gas, precio_min, 1)
    ingreso_hog, consumo = hogares(pib, 0.1 * pib, remesas)
    tasa = sector_financiero(0.03, riesgo)
    inversion = empresas(pib, tasa)


    deuda_total += deficit
    pib = consumo + inversion + ingresos

    resultados[i, t] = deuda_total / pib
    return resultados
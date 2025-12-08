# src/simulador.py
import pandas as pd
import numpy as np
from src.agentes import gobierno
from src.utils import proyeccion_estocastica, limpiar_numero
from src.config import COLUMNAS

def ejecutar_simulacion(df, n_sim=200, years=[2024, 2025], vol_gas=0.15, vol_min=0.20, tax_override=None):
    """
    Devuelve DataFrame con columnas:
    Simulacion, Año, PIB, Deficit_Fiscal, Deuda_Publica, Deuda_PIB
    Usa COLUMNAS para leer correctamente el CSV.
    """
    # validación básica
    if df is None or df.shape[0] == 0:
        return pd.DataFrame(columns=["Simulacion","Año","PIB","Deficit_Fiscal","Deuda_Publica","Deuda_PIB"])

    base = df.iloc[-1]

    # leer valores base usando COLUMNAS (encabezados reales)
    def b(k, default=0.0):
        col = COLUMNAS.get(k)
        if col in base:
            return limpiar_numero(base[col])
        return default

    pib_base = b("pib", 40000.0)
    deuda_int_base = b("deuda_int", 10000.0)
    deuda_ext_base = b("deuda_ext", 10000.0)
    gasto_base = b("gasto", 25000.0)
    recaudacion_base = b("recaudacion", 3500.0)
    precio_gas_base = b("precio_gas", 4.0)
    precio_min_base = b("precio_min", 1700.0)
    tasa_int_base = b("tasa_int", 0.03)

    resultados = []

    for sim in range(int(n_sim)):
        pib = pib_base
        deuda_publica = deuda_int_base + deuda_ext_base
        gasto = gasto_base
        recaudacion = recaudacion_base

        for anio in years:
            # shocks
            precio_gas = proyeccion_estocastica(precio_gas_base, vol_gas)
            precio_min = proyeccion_estocastica(precio_min_base, vol_min)

            # opcional: si tax_override es negativo o None, usar recaudacion_base; si >=0 usar ese ratio sobre PIB
            tax = None
            if tax_override is not None and tax_override >= 0:
                tax = float(tax_override)

            # Llamada al agente (se espera que devuelva ingresos_totales, deficit)
            ingresos, deficit = gobierno(
                pib=pib,
                recaudacion_tributaria=recaudacion,
                gasto_publico=gasto,
                precio_gas=precio_gas,
                deuda_interna=deuda_int_base,
                deuda_externa=deuda_ext_base,
                tasa_int_internacional=tasa_int_base,
                tax_override=tax
            )

            # aumentar deuda por déficit (si deficit positivo -> deuda sube)
            deuda_publica = deuda_publica + deficit

            # calcular razón deuda/PIB (proteger división por cero)
            deuda_pib = float(deuda_publica) / float(pib) if pib != 0 else np.nan

            resultados.append({
                "Simulacion": sim,
                "Año": anio,
                "PIB": pib,
                "Deficit_Fiscal": float(deficit),
                "Deuda_Publica": float(deuda_publica),
                "Deuda_PIB": deuda_pib
            })

            # dinámica de variables: aplicar crecimiento aleatorio
            pib = pib * float(np.random.normal(1.02, 0.015))   # ~2% growth with variability
            gasto = gasto * float(np.random.normal(1.03, 0.02)) # gasto crece ~3% con ruido
            # recaudacion puede moverse con PIB (simple pass-through)
            recaudacion = max(0.0, 0.18 * pib)  # ejemplo: 18% presión tributaria base

    df_res = pd.DataFrame(resultados)
    # forzar dtypes
    for c in ["PIB","Deficit_Fiscal","Deuda_Publica","Deuda_PIB"]:
        if c in df_res.columns:
            df_res[c] = pd.to_numeric(df_res[c], errors="coerce").fillna(0.0)
    return df_res

import numpy as np

# Agente 1: Gobierno
def gobierno(pib, recaudacion_tributaria, gasto_publico, precio_gas,
             deuda_interna, deuda_externa, tasa_int_internacional,
             tax_override=None):
    
    # 1. INGRESOS
    # Si el usuario define presión tributaria en la web, la usamos
    if tax_override is not None and float(tax_override) > 0:
        recaudacion_final = float(pib) * float(tax_override)
    else:
        recaudacion_final = float(recaudacion_tributaria)

    # Ingreso por Gas (Factor ajustado para que sea visible en el gráfico)
    # Precio (~4.5) * Cantidad Exportada (~40) * Gobierno Take (~0.35)
    ingreso_gas = float(precio_gas) * 45.0 * 0.35 * 10 
    
    ingresos_totales = recaudacion_final + ingreso_gas

    # 2. GASTOS
    # Lógica de Subsidios: Si el precio del gas/petróleo sube, el gasto aumenta
    factor_subsidio = 1.0
    if float(precio_gas) > 5.0:
        factor_subsidio = 1.05 # +5% gasto
    
    gastos_totales = float(gasto_publico) * factor_subsidio

    # 3. DÉFICIT
    # Si Gastos > Ingresos, el déficit es positivo (malo)
    deficit = gastos_totales - ingresos_totales

    return ingresos_totales, deficit

# Agente 2: Hogares
def hogares(pib, remesas):
    consumo = (float(pib) * 0.60) + float(remesas)
    ahorro = (float(pib) * 0.20)
    return consumo, ahorro

# Agente 3: Empresas
def empresas(pib, precio_minerales, exp_oro):
    inversion = float(pib) * 0.15
    ingresos_mineria = float(precio_minerales) * float(exp_oro) * 0.1 
    return inversion, ingresos_mineria

# Agente 4: Sector Financiero
def sector_financiero(deuda_interna, riesgo_pais):
    tasa_base = 0.03 
    spread = float(riesgo_pais) / 10000.0 
    intereses = float(deuda_interna) * (tasa_base + spread)
    return intereses

# Agente 5: Sector Externo
def sector_externo(rin, exportaciones, importaciones):
    balance = float(exportaciones) - float(importaciones)
    nuevas_rin = float(rin) + balance
    return nuevas_rin
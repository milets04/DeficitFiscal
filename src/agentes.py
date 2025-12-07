from src.config import PARAMETROS


# ------------------ AGENTE GOBIERNO ------------------


def gobierno(pib, gasto, precio_gas, precio_min, eficiencia):
    impuestos = PARAMETROS["presion_tributaria"] * pib * eficiencia
    ingresos_rrnn = (precio_gas + precio_min) * 0.02 * pib
    ingresos_totales = impuestos + ingresos_rrnn
    deficit = gasto - ingresos_totales
    return ingresos_totales, deficit


# ------------------ AGENTE HOGARES ------------------


def hogares(pib, transferencias, remesas):
    ingreso_disponible = 0.6 * pib + transferencias + remesas
    consumo = PARAMETROS["propension_consumo"] * ingreso_disponible
    return ingreso_disponible, consumo


# ------------------ AGENTE EMPRESAS ------------------


def empresas(pib_anterior, costo_credito):
    inversion = PARAMETROS["sensibilidad_inversion"] * pib_anterior - 0.5 * costo_credito
    return max(inversion, 0)


# ------------------ SECTOR FINANCIERO ------------------


def sector_financiero(tasa_internacional, riesgo_pais):
    return tasa_internacional + riesgo_pais


# ------------------ SECTOR EXTERNO ------------------


def sector_externo(precio_gas, precio_min):
    exportaciones = precio_gas * 10 + precio_min * 8
    importaciones = 0.25 * exportaciones
    return exportaciones, importaciones
import numpy as np

def calcular_indicadores(deuda_pib):
    media = np.mean(deuda_pib, axis=0)
    p5 = np.percentile(deuda_pib, 5, axis=0)
    p95 = np.percentile(deuda_pib, 95, axis=0)
    prob_crisis = np.mean(deuda_pib[:, -1] > 0.8)
    return media, p5, p95, prob_crisis
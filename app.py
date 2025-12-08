# app.py (reactiva)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from src.simulador import ejecutar_simulacion
from src.config import COLUMNAS

st.set_page_config(page_title="Simulación Déficit Fiscal Bolivia", layout="wide")
st.title("🇧🇴 Simulación Estocástica del Déficit Fiscal y Deuda Pública")

# Sidebar: controles
st.sidebar.header("Parámetros de Simulación")

n_sim = st.sidebar.slider("Número de simulaciones", 50, 1000, 300, step=50)
vol_gas = st.sidebar.slider("Volatilidad Precio Gas (σ)", 0.00, 0.5, 0.15, step=0.01)
vol_min = st.sidebar.slider("Volatilidad Precio Oro (σ)", 0.00, 0.5, 0.20, step=0.01)
umbral_crisis = st.sidebar.slider("Umbral Crisis (Deuda/PIB)", 0.1, 2.0, 0.8, step=0.05)

# presión tributaria override: si se quiere usar, activar checkbox y definir valor; si no, dejamos -1
use_tax = st.sidebar.checkbox("Override presión tributaria?", value=False)
if use_tax:
    tax_override = st.sidebar.number_input("Presión tributaria (ej. 0.20 = 20%)", min_value=0.0, max_value=1.0, value=0.18, step=0.01)
else:
    tax_override = None

st.sidebar.markdown("---")
st.sidebar.markdown("**Configuración de años**")
years_input = st.sidebar.text_input("Años a proyectar (coma separados)", "2024,2025")
try:
    years = [int(x.strip()) for x in years_input.split(",") if x.strip()]
except:
    years = [2024, 2025]

# Cargar datos
try:
    df = pd.read_csv("data/datos.csv", sep=";", encoding="latin-1")
except FileNotFoundError:
    st.error("No se encontró data/datos.csv. Coloca tu CSV en la carpeta data/")
    st.stop()

# convertir sólo las columnas que existen en COLUMNAS a números (protección para locales)
for k, v in COLUMNAS.items():
    if v in df.columns and k in ["pib", "gasto", "recaudacion", "deuda_int", "deuda_ext",
                                 "precio_gas", "precio_min", "tasa_int", "remesas"]:
        df[v] = pd.to_numeric(df[v].astype(str).str.replace('.', '').str.replace(',', '.'), errors="coerce").fillna(0.0)

# Mostrar datos si se desea
if st.checkbox("Mostrar datos cargados (debug)"):
    st.dataframe(df)

# Cachear simulaciones según parámetros para rendimiento.
@st.cache_data(ttl=60)
def run_and_cache(df, n_sim, years, vol_gas, vol_min, tax_override):
    return ejecutar_simulacion(df, n_sim=n_sim, years=years, vol_gas=vol_gas, vol_min=vol_min, tax_override=(tax_override if tax_override is not None else -1))

with st.spinner("Corriendo simulaciones..."):
    results = run_and_cache(df, int(n_sim), years, float(vol_gas), float(vol_min), tax_override)

# Si no hay resultados, salir
if results is None or results.shape[0] == 0:
    st.warning("No se generaron resultados. Verifica el dataset.")
    st.stop()

# Calcular Debt/PIB si no existe
if "Deuda_PIB" not in results.columns:
    results["Deuda_PIB"] = results["Deuda_Publica"] / results["PIB"].replace({0:np.nan})

# --- Fan chart: percentiles por año ---
pct = results.groupby("Año")["Deuda_PIB"].agg(
    p5=lambda x: np.nanpercentile(x, 5),
    p25=lambda x: np.nanpercentile(x, 25),
    p50=lambda x: np.nanpercentile(x, 50),
    p75=lambda x: np.nanpercentile(x, 75),
    p95=lambda x: np.nanpercentile(x, 95)
).reset_index()

years_sorted = pct["Año"].tolist()
fig = go.Figure()
fig.add_trace(go.Scatter(x=years_sorted, y=pct["p95"], mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
fig.add_trace(go.Scatter(x=years_sorted, y=pct["p5"], mode='lines', fill='tonexty', fillcolor='rgba(173,216,230,0.2)', line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=years_sorted, y=pct["p75"], mode='lines', line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=years_sorted, y=pct["p25"], mode='lines', fill='tonexty', fillcolor='rgba(135,206,250,0.4)', line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=years_sorted, y=pct["p50"], mode='lines', name='Mediana', line=dict(color='blue', width=2)))
fig.update_layout(title="Fan Chart: Deuda Pública / PIB (percentiles)", xaxis_title="Año", yaxis_title="Deuda / PIB (razón)", template="plotly_white", height=480)
st.plotly_chart(fig, use_container_width=True)

# --- Déficit: mediana por año ---
deficit_med = results.groupby("Año")["Deficit_Fiscal"].median().reset_index()
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=deficit_med["Año"], y=deficit_med["Deficit_Fiscal"], marker_color='indianred', name="Déficit (mediana)"))
fig2.update_layout(title="Déficit Fiscal (Mediana por año)", xaxis_title="Año", yaxis_title="Millones USD", template="plotly_white", height=350)
st.plotly_chart(fig2, use_container_width=True)

# --- Histograma deuda/PIB al final ---
last_year = max(years)
final_df = results[results["Año"] == last_year].copy()
final_df = final_df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Deuda_PIB"])
fig3 = go.Figure()
fig3.add_trace(go.Histogram(x=final_df["Deuda_PIB"], nbinsx=40))
fig3.update_layout(title=f"Distribución Deuda/PIB en {last_year}", xaxis_title="Deuda/PIB", yaxis_title="Frecuencia", template="plotly_white", height=350)
st.plotly_chart(fig3, use_container_width=True)

# --- Probabilidad y métricas ---
prob = (final_df["Deuda_PIB"] > umbral_crisis).mean()
col1, col2, col3 = st.columns(3)
col1.metric("Probabilidad Deuda/PIB > " + str(umbral_crisis), f"{prob*100:.2f}%")
col2.metric("Deuda Promedio (último año)", f"{final_df['Deuda_Publica'].mean():,.2f} MM USD")
col3.metric("Déficit Mediano (último año)", f"{final_df['Deficit_Fiscal'].median():,.2f} MM USD")

# descarga
csv = results.to_csv(index=False).encode('utf-8')
st.download_button("Descargar resultados (CSV)", csv, file_name="sim_results.csv", mime="text/csv")

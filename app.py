import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.simulador import ejecutar_simulacion
from src.indicadores import calcular_indicadores


st.set_page_config(page_title="Modelo Déficit Fiscal", layout="wide")
st.title("Simulación Estocástica de Déficit Fiscal y Deuda Pública")


# ----------- CARGA DE DATOS -----------
df = pd.read_csv("data/datos2.csv")


# ----------- BOTÓN DE SIMULACIÓN -----------
if st.button("Ejecutar Simulación"):
    resultados = ejecutar_simulacion(df)
    media, p5, p95, prob_crisis = calcular_indicadores(resultados)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=media, name="Media Deuda/PIB"))
    fig.add_trace(go.Scatter(y=p5, name="Percentil 5%"))
    fig.add_trace(go.Scatter(y=p95, name="Percentil 95%"))

    st.plotly_chart(fig, use_container_width=True)
    st.metric("Probabilidad de Crisis Fiscal", f"{round(prob_crisis*100,2)} %")
# ============================================================
# 📌 graficos.py — Gráficos principales de la app
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# ============================================================
# 🌿 Top sectores
# ============================================================

def grafico_top_sectores(df):
    """Grafica los 10 sectores con más negocios verdes."""

    if df.empty or "SECTOR" not in df.columns:
        st.info("No hay datos válidos para mostrar sectores.")
        return

    top = df["SECTOR"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=top.values, y=top.index, palette="Greens_r", ax=ax)

    ax.set_title("Top 10 Sectores", fontsize=12)
    ax.set_xlabel("Cantidad")
    ax.set_ylabel("Sector")

    st.pyplot(fig)


# ============================================================
# 📈 Tendencia anual
# ============================================================

def grafico_tendencia(df):
    """Línea de tiempo: negocios registrados por año."""
    df_y = df.dropna(subset=["AÑO"])

    if df_y.empty:
        st.info("Sin datos de años válidos.")
        return

    conteo = df_y.groupby("AÑO").size()

    fig, ax = plt.subplots(figsize=(6, 3))
    sns.lineplot(x=conteo.index, y=conteo.values, marker="o", ax=ax)

    ax.set_title("Tendencia anual", fontsize=12)
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad")

    st.pyplot(fig)


# ============================================================
# ♻ Pie chart Basura Cero
# ============================================================

def grafico_relacion_pie(df):
    """Grafica proporción de iniciativas que tienen relación con Basura Cero."""

    tabla = (
        df["RELACIÓN BASURA CERO"]
        .fillna("No aplica")
        .apply(lambda v: "Alineada" if v.lower() != "no aplica" else "No alineada")
        .value_counts()
        .reset_index()
    )

    fig = px.pie(
        tabla,
        names="index",
        values="RELACIÓN BASURA CERO",
        color="index",
        color_discrete_map={"Alineada": "#1FA88E", "No alineada": "#C9B79C"},
        hole=0.3,
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 🗺️ Mapa interactivo por departamento
# ============================================================

def grafico_mapa(df):
    """Mapa basado en coordenadas de porcentaje Basura Cero por departamento."""

    if "COORDS" not in df.columns:
        st.warning("No se encontraron coordenadas para el mapa.")
        return

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size="TOTAL",
        color="PORCENTAJE",
        color_continuous_scale="Greens",
        mapbox_style="carto-positron",
        zoom=4.2,
        hover_name="DEPARTAMENTO",
    )

    st.plotly_chart(fig, use_container_width=True)

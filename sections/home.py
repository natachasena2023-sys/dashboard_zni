# ============================================================
# 📌 home.py — Página principal
# ============================================================

import streamlit as st
from graficos import (
    grafico_top_sectores,
    grafico_tendencia,
    grafico_relacion_pie
)


def render_home(df):

    st.title("🌿 Dashboard de Negocios Verdes")

    st.subheader("Resumen general")
    st.write(f"Total registros: **{len(df):,}**")

    st.markdown("---")
    st.subheader("📊 Sectores principales")
    grafico_top_sectores(df)

    st.markdown("---")
    st.subheader("📈 Tendencia anual")
    grafico_tendencia(df)

    st.markdown("---")
    st.subheader("♻ Iniciativas relacionadas con Basura Cero")
    grafico_relacion_pie(df)

# ============================================================
# 🌿 MAIN APP — Dashboard de Negocios Verdes y Basura Cero
# ============================================================

import streamlit as st
from config import *                   # Diccionarios globales
from data_loader import load_data      # Carga y limpieza de datos
from sections.home import render_home  # Sección Inicio
from sections.faq import render_faq    # Sección Preguntas
from sections.mapa import render_mapa  # Sección Mapa del sitio

# ============================================================
# 🔧 Configuración inicial de página
# ============================================================

st.set_page_config(
    page_title="EcoDash | Negocios Verdes",
    layout="wide",
    page_icon="♻️"
)

# ============================================================
# 🎨 Cargar CSS externo (estilos de la aplicación)
# ============================================================

def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠ No se encontró el archivo assets/styles.css")

load_css()

# ============================================================
# 📥 Cargar datos (con caché)
# ============================================================

df = load_data()

# ============================================================
# 🧭 Barra lateral de navegación
# ============================================================

st.sidebar.title("Navegación")
section = st.sidebar.radio(
    "Selecciona una sección",
    ("Inicio", "Mapa del sitio", "Preguntas frecuentes"),
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("Proyecto académico — Economía Circular y Negocios Verdes")

# ============================================================
# 🧱 Renderizado de secciones
# ============================================================

if section == "Inicio":
    render_home(df)

elif section == "Mapa del sitio":
    render_mapa()

elif section == "Preguntas frecuentes":
    render_faq()

# ============================================================
# 🏁 Footer
# ============================================================

st.markdown(
    """
    <hr>
    <div style="text-align:center; color:#4A6C59;">
        💚 <b>Dashboard desarrollado con Streamlit — Proyecto Basura Cero</b> 💚
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 📌 faq.py — Preguntas frecuentes
# ============================================================

import streamlit as st

def render_faq():

    st.title("❓ Preguntas frecuentes")

    with st.expander("¿De dónde provienen los datos?"):
        st.write("De la Superintendencia de Servicios Públicos y MinAmbiente.")

    with st.expander("¿Cada cuánto se actualiza?"):
        st.write("Puede reemplazarse fácilmente la URL del CSV.")

    with st.expander("¿Cómo se realiza la limpieza?"):
        st.write("Mediante normalización, estandarización y enriquecimiento.")

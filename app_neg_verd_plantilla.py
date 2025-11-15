# ============================================================
# 🌿 Proyecto: Dashboard de Negocios Ecológicos
# Autor: Natacha Ochoa
# Descripción:
#   Esta aplicación muestra una plantilla base en Streamlit con
#   estilo ecológico, integrando un banner, información general,
#   y una visualización de datos limpia y moderna.
# ============================================================

import streamlit as st
import base64
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 🌿 Función: Convertir imagen a base64 para usar en el banner
# ------------------------------------------------------------
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode()
    return b64_data

# Ruta del banner principal
img_path = "img/verde2.png"
img_base64 = img_to_base64(img_path)

# ------------------------------------------------------------
# 🌍 Configuración general de la página Streamlit
# ------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Negocios Ecológicos", page_icon="🌿")

# ------------------------------------------------------------
# 🎨 CSS personalizado (paleta inspirada en tonos verdes suaves)
# ------------------------------------------------------------
st.markdown(f"""
<style>
    /* ======== ENCABEZADO ======== */
    [data-testid="stHeader"] {{
        background-color: #88C999 !important;  /* Verde aguamarina */
    }}
    [data-testid="stHeader"] * {{
        color: #1C3B2F !important; /* Texto oscuro para contraste */
    }}

    /* ======== FONDO GENERAL ======== */
    [data-testid="stAppViewContainer"], body {{
        background-color: #E6FFF7 !important;  /* Fondo claro verde-agua */
    }}

    /* ======== TEXTOS ======== */
    .stTitle {{
        color: #1C7C54;
        font-weight: bold;
    }}
    .stText, .stMarkdown {{
        color: #3C3C3C;
    }}

    /* ======== BANNER PRINCIPAL ======== */
    .banner {{
        position: relative;
        width: 100%;
        height: 250px;
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2em;
        font-weight: bold;
        color: white;
        border-bottom: 2px solid #C9B79C;
        padding: 20px;
        text-shadow:
           -2px -2px 0 #000,
            2px -2px 0 #000,
           -2px  2px 0 #000,
            2px  2px 0 #000;
    }}
    .banner::before {{
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.2);
        z-index: 0;
    }}
    .banner > * {{
        position: relative;
        z-index: 1;
    }}

    /* ======== BOTONES ======== */
    button {{
        background-color: #A8E55A;
        color: #1C3B2F;
        border: none;
        padding: 10px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 6px;
    }}
    button:hover {{
        background-color: #9CD25B;
        color: #0F261D;
    }}

    /* ======== ADAPTACIÓN MÓVIL ======== */
    @media (max-width: 768px) {{
        .banner {{
            height: 150px;
            font-size: 1.4em;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🖼️ Banner con imagen y texto superpuesto
# ------------------------------------------------------------
st.markdown("""
<div class="banner">
    🌿 Negocios Ecológicos: Sostenibilidad y Crecimiento 🌿
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 📖 Sección informativa
# ------------------------------------------------------------
st.title("Página Base para Negocios Ecológicos")

col1, col2 = st.columns([1, 2])

with col1:
    st.image('img/bb.jpg', caption="Imagen ecológica de ejemplo", use_container_width=True)

with col2:
    st.markdown("""
    Bienvenido a tu **app base para negocios ecológicos**.  
    Aquí puedes promover productos sostenibles, compartir historias de impacto ambiental
    o conectar con clientes verdes 🌱.
    
    **Principios clave del proyecto:**
    - ♻️ **Sostenibilidad:** Promover prácticas amigables con el planeta.  
    - 💡 **Innovación:** Fomentar tecnologías limpias.  
    - 🌍 **Comunidad:** Conectar emprendedores y consumidores verdes.  
    
    Esta página se adapta a PC y celular, maximizando el espacio visual.  
    ¡Personalízala para tus proyectos o emprendimientos sostenibles!
    """)
    if st.button("¡Explora Más!"):
        st.success("¡Gracias por interesarte en negocios ecológicos!")

st.markdown("---")

# ------------------------------------------------------------
# 📊 Carga y limpieza del dataset
# ------------------------------------------------------------
url = "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/Listado_de_Negocios_Verdes_20251025.csv"
df = pd.read_csv(url)

# Limpieza de nombres de columnas
renames = {col: col.split('\n')[0].strip() for col in df.columns if '\n' in col}
df = df.rename(columns=renames)
df.columns = df.columns.str.upper()

# Limpieza y conversión de columna "AÑO"
if 'AÑO' in df.columns:
    df['AÑO'] = df['AÑO'].astype(str).str.replace(',', '', regex=False)
    df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').astype('Int64')

# ------------------------------------------------------------
# 🌱 Visualización: Top 10 Sectores con más negocios verdes
# ------------------------------------------------------------
st.markdown("### 🌿 Top 10 Sectores con más Negocios Verdes")

# Paleta ecológica moderna
custom_palette = ["#E6FFF7", "#B2F2E8", "#66D1BA", "#1FA88E", "#0B5C4A"]

# Cálculo del top 10
top_sectores = df['SECTOR'].value_counts().head(10)

# Crear figura más compacta y proporcionada
plt.figure(figsize=(6, 4))
sns.barplot(
    x=top_sectores.values,
    y=top_sectores.index,
    palette=custom_palette,
    edgecolor="#0B5C4A"
)

plt.title("Top 10 Sectores con más Negocios Verdes", fontsize=10, weight='bold', color="#0B5C4A", pad=8)
plt.xlabel("Número de Negocios", fontsize=9, color="#0B5C4A")
plt.ylabel("Sector", fontsize=9, color="#0B5C4A")
sns.despine(left=True, bottom=True)
plt.tight_layout()

# Mostrar gráfica en Streamlit
st.pyplot(plt)

# ------------------------------------------------------------
# 🪴 Pie de página
# ------------------------------------------------------------
st.markdown("---")
st.markdown("💚 *Proyecto académico realizado con Streamlit - Inspirado en la sostenibilidad y el diseño ecológico.*")
# ============================================================
# 🌿 Proyecto: Dashboard de Negocios Ecológicos
# Autor: Natacha Ochoa
# Descripción:
#   Esta aplicación muestra una plantilla base en Streamlit con
#   estilo ecológico, integrando un banner, información general,
#   métricas rápidas, y una visualización de datos limpia y moderna.
#   El enfoque es promover la sostenibilidad a través de datos y diseño.
#
# Notas para el lector (Profesor/Compañeros):
#   - Este script está estructurado en secciones lógicas para facilitar la comprensión.
#   - Cada función tiene un docstring explicativo.
#   - Los estilos CSS usan una paleta ecológica (verdes suaves) para coherencia visual.
#   - La limpieza de datos asegura integridad; la visualización es accesible y moderna.
#   - Si ejecutas esto, asegúrate de que las imágenes en 'img/' existan o usa URLs públicas.
# ============================================================

import streamlit as st
import base64
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re  # Importar re para expresiones regulares
from io import BytesIO  # Para manejo de imágenes en caso de error

# ------------------------------------------------------------
# 🌿 Función: Convertir imagen a base64 para usar en el banner
# ------------------------------------------------------------
def img_to_base64(img_path):
    try:
        with open(img_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode()
        return b64_data
    except FileNotFoundError:
        st.warning(f"Imagen no encontrada en {img_path}. Usando placeholder.")
        return None

# ------------------------------------------------------------
# 📊 Función: Cargar y limpiar dataset de negocios verdes
# ------------------------------------------------------------
@st.cache_data  # Cachea los datos para evitar recargas innecesarias
def load_and_clean_data(url):
    """
    Carga un dataset CSV desde una URL, lo limpia y prepara para análisis.
    
    Parámetros:
    - url (str): URL del archivo CSV.
    
    Retorno:
    - pd.DataFrame: DataFrame limpio con columnas en mayúsculas y tipos corregidos.
    
    Notas:
    - Limpia nombres de columnas (elimina saltos de línea).
    - Convierte 'AÑO' a numérico, manejando errores.
    - Si falla la carga, muestra error y retorna DataFrame vacío.
    """
    try:
        df = pd.read_csv(url)
        # Limpieza de nombres de columnas
        renames = {col: col.split('\n')[0].strip() for col in df.columns if '\n' in col}
        df = df.rename(columns=renames)
        df.columns = df.columns.str.upper()
        # Convertir a mayúsculas la columna PRODUCTO PRINCIPAL
        df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].str.upper()

        # Luego, elimina todos los puntos '.' que aparezcan en los nombres de productos
        df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].str.replace('.', '', regex=False)

        # Reemplazar 'MIEL' por 'MIEL DE ABEJAS'
        df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].replace("MIEL", "MIEL DE ABEJAS")
        # Limpieza y conversión de columna "AÑO"

        # Diccionario para corregir regiones según autoridad ambiental
        mapeo_region = {
            "AMVA": "ANDINA",
            "CAM": "ANDINA",
            "CAR": "ANDINA",
            "CARDER": "ANDINA",
            "CARDIQUE": "CARIBE",
            "CARSUCRE": "CARIBE",
            "CAS": "ANDINA",
            "CDA": "AMAZONÍA",
            "CDMB": "ANDINA",
            "CODECHOCÓ": "PACÍFICA",
            "CORALINA": "INSULAR",
            "CORANTIOQUIA": "ANDINA",
            "CORMACARENA": "ORINOQUÍA",
            "CORNARE": "ANDINA",
            "CORPAMAG": "CARIBE",
            "CORPOAMAZONÍA": "AMAZONÍA",
            "CORPOBOYACÁ": "ANDINA",
            "CORPOCALDAS": "ANDINA",
            "CORPOCESAR": "CARIBE",
            "CORPOCHIVOR": "ANDINA",
            "CORPOGUAJIRA": "CARIBE",
            "CORPOGUAVIO": "ANDINA",
            "CORPOMOJANA": "CARIBE",
            "CORPONARIÑO": "PACÍFICA",
            "CORPONOR": "CARIBE",
            "CORPORINOQUÍA": "ORINOQUÍA",
            "CORPOURABÁ": "PACÍFICA",
            "CORTOLIMA": "ANDINA",
            "CRA": "CARIBE",
            "CRC": "PACÍFICA",
            "CRQ": "ANDINA",
            "CSB": "CARIBE",
            "CVC": "PACÍFICA",
            "CVS": "CARIBE",
            "DADSA": "ANDINA",
            "DAGMA": "ANDINA",
            "EPA Barranquilla Verde": "CARIBE",
            "EPA Buenaventura": "PACÍFICA",
            "EPA Cartagena": "CARIBE",
            "SDA": "ANDINA"
        }

        # Limpiar y asignar correctamente regiones, reemplazando "No registra"
        # Primero se asegura que no haya espacios extras
        df['AUTORIDAD AMBIENTAL'] = df['AUTORIDAD AMBIENTAL'].str.strip()
        df['REGIÓN'] = df['REGIÓN'].str.strip()

        def asignar_region(row):
            if pd.isna(row['REGIÓN']) or row['REGIÓN'].lower() == "no registra":
                return mapeo_region.get(row['AUTORIDAD AMBIENTAL'], row['REGIÓN'])
            else:
                return row['REGIÓN']

        df['REGIÓN'] = df.apply(asignar_region, axis=1)

        # Función para quitar prefijos numéricos del tipo "1. ", "2.3. ", etc.
        def limpiar_numeros(texto):
            if pd.isna(texto):
                return texto
            return re.sub(r'^\s*[\d\.]+\s*', '', texto)

        # Aplicar limpieza en 'CATEGORÍA' y 'SECTOR' si existen
        if 'CATEGORÍA' in df.columns:
            df['CATEGORÍA'] = df['CATEGORÍA'].apply(limpiar_numeros)

        if 'SECTOR' in df.columns:
            df['SECTOR'] = df['SECTOR'].apply(limpiar_numeros)

        if 'SUBSECTOR' in df.columns:
            df['SUBSECTOR'] = df['SUBSECTOR'].apply(limpiar_numeros)

        if 'AÑO' in df.columns:
            df['AÑO'] = df['AÑO'].astype(str).str.replace(',', '', regex=False)
            df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').astype('Int64')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}. Verifica la URL.")
        return pd.DataFrame()  # Retorna vacío en caso de error

# ------------------------------------------------------------
# 🌍 Configuración general de la página Streamlit
# ------------------------------------------------------------
st.set_page_config(
    layout="wide", 
    page_title="Basura Cero | Economía Circular", 
    page_icon="♻️",
    initial_sidebar_state="expanded"  # Sidebar para futuras expansiones
)

# ------------------------------------------------------------
# 🎨 CSS personalizado (paleta inspirada en tonos verdes suaves y modernos)
# ------------------------------------------------------------
# Ruta del banner principal (con fallback)
banner_image_path = "img/verde2.png"
banner_base64 = img_to_base64(banner_image_path)

# Ruta del banner inferior (con fallback)
banner_inferior_image_path = "img/verde.png"  
banner_inferior_base64 = img_to_base64(banner_inferior_image_path)

# Ruta del banner inferior (con fallback)
img_col1_image_path = "img/baner_l.png"  
img_col1_base64 = img_to_base64(img_col1_image_path)

# CSS mejorado: más elegante, con sombras, transiciones y mejor responsividad
st.markdown(f"""
<style>
    /* ======== ENCABEZADO ======== */
    [data-testid="stHeader"] {{
        background: linear-gradient(90deg, #88C999, #A8E55A) !important;  /* Gradiente suave */
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    [data-testid="stHeader"] * {{
        color: #1C3B2F !important; /* Texto oscuro para contraste */
    }}

    /* ======== FONDO GENERAL ======== */
    [data-testid="stAppViewContainer"], body {{
        background-color: #E6FFF7 !important;  /* Fondo claro verde-agua */
        font-family: 'Arial', sans-serif;  /* Fuente legible */
    }}

    /* ======== TEXTOS ======== */
    .stTitle {{
        color: #1C7C54;
        font-weight: bold;
        text-align: center;
    }}
    .stText, .stMarkdown {{
        color: #3C3C3C;
        line-height: 1.6;
    }}

    /* ======== BANNER PRINCIPAL ======== */
    .banner {{
        position: relative;
        width: 100%;
        height: 250px;
        background-image: url("data:image/jpg;base64,{banner_base64 if banner_base64 else ''}");
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2em;
        font-weight: bold;
        color: white;
        border-bottom: 3px solid #C9B79C;
        padding: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-radius: 8px;
        overflow: hidden;
    }}
    .banner::before {{
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(0,0,0,0.3), rgba(0,0,0,0.1));
        z-index: 0;
    }}
    .banner > * {{
        position: relative;
        z-index: 1;
    }}

    /* ======== BANNER INFERIOR ======== */
    .banner-inferior {{
        position: relative;
        width: 100%;
        height: 200px;  /* Altura ajustable */
        background-image: url("data:image/jpg;base64,{banner_inferior_base64 if banner_inferior_base64 else ''}");
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5em;
        font-weight: bold;
        color: white;
        border-top: 3px solid #C9B79C;
        padding: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-radius: 8px;
        overflow: hidden;
        margin-top: 20px;
    }}
    .banner-inferior::before {{
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(0,0,0,0.3), rgba(0,0,0,0.1));
        z-index: 0;
    }}
    .banner-inferior > * {{
        position: relative;
        z-index: 1;
    }}
    /* ======== IMAGEN CON TEXTO SUPERPUESTO ======== */
       .imagen-con-texto {{
           position: relative;
           width: 100%;
           height: 300px;  /* Ajusta según la imagen */
           background-image: url("data:image/jpg;base64,{img_col1_base64 if img_col1_base64 else ''}");
           background-size: cover;
           background-position: center;
           border-radius: 8px;
           overflow: hidden;
           box-shadow: 0 2px 4px rgba(0,0,0,0.1);
       }}
        .texto-superpuesto {{
           position: absolute;
           top: 50%;
           left: 50%;
           transform: translate(-50%, -50%);
           color: white;
           font-size: 1.2em;
           font-weight: bold;
           text-align: center;
           text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
           z-index: 1;
       }}
       .imagen-con-texto::before {{
           content: "";
           position: absolute;
           top: 0; left: 0;
           width: 100%; height: 100%;
           background: linear-gradient(45deg, rgba(0,0,0,0.3), rgba(0,0,0,0.1));
           z-index: 0;
       }}

    /* ======== BOTONES ======== */
    button {{
        background: linear-gradient(45deg, #A8E55A, #88C999);
        color: #1C3B2F;
        border: none;
        padding: 12px 20px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    button:hover {{
        background: linear-gradient(45deg, #9CD25B, #7BBF8A);
        color: #0F261D;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}

    /* ======== MÉTRICAS ======== */
    .metric {{
        background: #F0FFF4;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #A8E55A;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }}

    /* ======== ADAPTACIÓN MÓVIL ======== */
    @media (max-width: 768px) {{
        .banner {{
            height: 150px;
            font-size: 1.4em;
        }}
        .metric {{
            padding: 10px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🖼️ Banner con imagen y texto superpuesto
# ------------------------------------------------------------
st.markdown("""
<div class="banner">
    🌿 Residuos con propósito: Colombia hacia la Economía Circular 🌿
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 📖 Sección informativa con métricas rápidas
# ------------------------------------------------------------
st.title("Integrando datos de Negocios Verdes, aprovechamiento y Ciencia, Tecnología e Innovación♻️")

st.markdown('''
            ¡Bienvenidos! 🌱  
    Este espacio presenta, de forma interactiva, cómo Colombia avanza hacia el objetivo **Basura Cero**, 
    transformando los residuos en oportunidades sostenibles.  

    Explora los mapas y gráficos para conocer los **proyectos activos**, las **inversiones por región** 
    y las **iniciativas empresariales verdes** que promueven una gestión responsable del ambiente.
     
            ''')

st.markdown('')

# Cargar datos (con cache y manejo de errores)
data_url = "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/Listado_de_Negocios_Verdes_20251025.csv"
df = load_and_clean_data(data_url)

# Sección descriptiva
col1, col2 = st.columns([1, 2])

with col1:
    
    # Imagen con fallback
    try:
        st.image('img/mapa_basura_cero.jpg', caption="Fuente: Datos abiertos del Gobierno de Colombia (SSPD y MinVivienda, 2023–2024", use_container_width=True)
        st.markdown("""
       <div class="imagen-con-texto">
           <div class="texto-superpuesto">
               🌱 Principios clave del proyecto:<br>
               <strong>Impulsando el Futuro Sostenible</strong>
           </div>
       </div>
       """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.image("https://via.placeholder.com/300x200?text=Imagen+Ecológica", caption="Placeholder ecológico")

with col2:
    st.markdown("""
    
    El mapa muestra la **distribución geográfica de 12 proyectos del Programa Basura Cero**, 
    con una inversión total aproximada de **$119.212 millones de pesos**.  
    Estas iniciativas están orientadas a la **gestión integral de residuos**, el **aprovechamiento de materiales reciclables** y el **cierre progresivo de botaderos**.

    Explora el mapa para conocer en qué departamentos se están desarrollando los proyectos, su inversión y fase de avance. 
              
    """)
    if st.button("¡Explora Más!"):
        st.success("¡Gracias por interesarte en negocios ecológicos! 🌿")

    st.markdown('------')
    st.markdown(''' 
            **Principios clave del proyecto:**
        - ♻️ **Sostenibilidad:** Promover prácticas amigables con el planeta.  
        - 💡 **Innovación:** Fomentar tecnologías limpias.  
        - 🌍 **Comunidad:** Conectar emprendedores y consumidores verdes. 
        ''')
st.markdown("---")

# Mostrar métricas rápidas si los datos se cargaron correctamente

if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric"><h3>📊 Total Negocios</h3><p>{len(df)}</p></div>', unsafe_allow_html=True)
    with col2:
        top_sector = df['SECTOR'].value_counts().idxmax() if 'SECTOR' in df.columns and not df['SECTOR'].isna().all() else "N/A"
        st.markdown(f'<div class="metric"><h3>🏆 Sector Líder</h3><p>{top_sector}</p></div>', unsafe_allow_html=True)
    with col3:
        top_product = df['PRODUCTO PRINCIPAL'].value_counts().idxmax() if 'PRODUCTO PRINCIPAL' in df.columns and not df['PRODUCTO PRINCIPAL'].isna().all() else "N/A"
        st.markdown(f'<div class="metric"><h3>🌟 Producto Líder</h3><p>{top_product}</p></div>', unsafe_allow_html=True)

st.markdown('')
# ------------------------------------------------------------
# 🌱 Visualización: Top 10 Sectores con más negocios verdes
# ------------------------------------------------------------
if not df.empty and 'SECTOR' in df.columns and not df['SECTOR'].isna().all():
    st.markdown("### 🌿 Top 10 Sectores con más Negocios Verdes")
    
    # Paleta ecológica moderna y vibrante
    custom_palette = ["#E6FFF7", "#B2F2E8", "#66D1BA", "#1FA88E", "#0B5C4A", "#A8E55A", "#88C999", "#C9B79C", "#7BBF8A", "#9CD25B"]
    
    # Cálculo del top 10
    top_sectores = df['SECTOR'].value_counts().head(10)
    
    # Configurar matplotlib una vez
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'Arial'
    
    # Crear figura compacta y centrada
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x=top_sectores.values,
        y=top_sectores.index,
        palette=custom_palette[:len(top_sectores)],
        edgecolor="#0B5C4A",
        ax=ax
    )
    
    # Añadir etiquetas con los valores al final de las barras usando ax.text para mayor control
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', padding=3, fontsize=9, color="#0B5C4A")

    ax.set_title("Top 10 Sectores con más Negocios Verdes", fontsize=12, weight='bold', color="#0B5C4A", pad=10)
    ax.set_xlabel("Número de Negocios", fontsize=10, color="#0B5C4A")
    ax.set_ylabel("Sector", fontsize=10, color="#0B5C4A")
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    
    # Mostrar gráfica centrada
    st.pyplot(fig)
else:
    st.warning("La columna 'SECTOR' no está presente, está vacía o no contiene datos válidos. No se puede generar la visualización. Verifica el dataset y la limpieza aplicada.")

# Mostrar tabla con el resultado de la limpieza de la base de datos
# Mostrar contenedor expandible con la base de datos
if not df.empty:
    with st.expander("📋 Ver Base de Datos Normalizada Completa"):
        st.dataframe(df)  # Muestra el dataframe completo
        # Opción para descargar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Base de Datos en CSV",
            data=csv,
            file_name='negocios_verdes_normalizados.csv',
            mime='text/csv'
        )
else:
    st.warning("No se pudieron cargar los datos. Verifica la URL o la conexión a internet.")

# ------------------------------------------------------------
# 🖼️ Banner inferior con imagen y texto superpuesto
# ------------------------------------------------------------
st.markdown("""
<div class="banner-inferior">
    🌿 Gracias por apoyar los Negocios Ecológicos 🌿
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🪴 Pie de página
# ------------------------------------------------------------
st.markdown("---")
st.markdown("""
💚 *Proyecto académico realizado con Streamlit - Inspirado en la sostenibilidad y el diseño ecológico.*  
[Visita nuestro sitio web](https://example.com) para más información.
""")
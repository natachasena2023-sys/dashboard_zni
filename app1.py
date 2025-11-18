# Aplicación Streamlit para explorar negocios verdes en Colombia.
# ============================================================
# 🌿 Proyecto: Dashboard de Negocios Ecológicos
# Autor: Angie Ruiz
#        Natacha Ochoa
#        Paulina Noreña
#        Juan Ignacio García
#        Thomas Medina
# Descripción:
#   Esta aplicación muestra una plantilla base en Streamlit con
#   estilo ecológico, integrando un banner, información general,
#   y una visualización de datos limpia y moderna.
# ============================================================

# ============================================================
# Notas de la versión
# ==============================================================================
# En esta version se realizo notas aclaratorias en la mayoria de las lineas 
# varias lineas
# ==============================================================================
# Librerías
# ============================================================

from __future__ import annotations  # Permite usar anotaciones de tipos más modernas.

from typing import Callable, Optional  # Tipos auxiliares para anotación.
from typing import Optional  # (repetido pero no afecta funcionalidad)

import re          # Expresiones regulares para limpieza de texto.
import textwrap    # Manejo de bloques de texto multilínea.
import base64      # Permite convertir imágenes a texto base64.

import matplotlib.pyplot as plt  # Graficación principal.
import pandas as pd              # Manejo de datos tabulares.
import seaborn as sns            # Gráficos estadísticos.
import streamlit as st           # Framework de interfaz web.


# ============================================================
# 1️⃣ Cargar el dataset
# ============================================================

# URL remota donde está almacenado el archivo CSV con los negocios verdes.
DATA_URL = (
    "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/"
    "Listado_de_Negocios_Verdes_20251025.csv"
)

# ============================================================
# Diccionario de normalización de nombres de departamentos
# ============================================================

# Mapea múltiples variaciones del mismo departamento hacia una forma canónica.
DEPARTMENT_CANONICAL = {
   # (Lista extensa de equivalencias normalizadas) ...
    "AMAZONAS": "AMAZONAS",
    "ANTIOQUIA": "ANTIOQUIA",
    "ARAUCA": "ARAUCA",
    "ATLANTICO": "ATLÁNTICO",
    "ATLÁNTICO": "ATLÁNTICO",
    "BOGOTA": "BOGOTÁ, D.C.",
    "BOGOTA DC": "BOGOTÁ, D.C.",
    "BOGOTA D C": "BOGOTÁ, D.C.",
    "BOGOTA D.C": "BOGOTÁ, D.C.",
    "BOGOTÁ": "BOGOTÁ, D.C.",
    "BOLIVAR": "BOLÍVAR",
    "BOLÍVAR": "BOLÍVAR",
    "BOYACA": "BOYACÁ",
    "BOYACÁ": "BOYACÁ",
    "CALDAS": "CALDAS",
    "CAQUETA": "CAQUETÁ",
    "CAQUETÁ": "CAQUETÁ",
    "CASANARE": "CASANARE",
    "CAUCA": "CAUCA",
    "CESAR": "CESAR",
    "CHOCO": "CHOCÓ",
    "CHOCÓ": "CHOCÓ",
    "CORDOBA": "CÓRDOBA",
    "CÓRDOBA": "CÓRDOBA",
    "CUNDINAMARCA": "CUNDINAMARCA",
    "GUAINIA": "GUAINÍA",
    "GUAINÍA": "GUAINÍA",
    "GUAJIRA": "LA GUAJIRA",
    "LA GUAJIRA": "LA GUAJIRA",
    "GUAVIARE": "GUAVIARE",
    "HUILA": "HUILA",
    "MAGDALENA": "MAGDALENA",
    "META": "META",
    "NARINO": "NARIÑO",
    "NARIÑO": "NARIÑO",
    "NORTE DE SANTANDER": "NORTE DE SANTANDER",
    "PUTUMAYO": "PUTUMAYO",
    "QUINDIO": "QUINDÍO",
    "QUINDÍO": "QUINDÍO",
    "RISARALDA": "RISARALDA",
    "SAN ANDRES": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
    "SAN ANDRÉS": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
    "SAN ANDRES Y PROVIDENCIA": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
    "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
    "SANTANDER": "SANTANDER",
    "SUCRE": "SUCRE",
    "TOLIMA": "TOLIMA",
    "VALLE": "VALLE DEL CAUCA",
    "VALLE DEL CAUCA": "VALLE DEL CAUCA",
    "VAUPES": "VAUPÉS",
    "VAUPÉS": "VAUPÉS",
    "VICHADA": "VICHADA",
}

# ============================================================
# Funciones de normalización de campos
# ============================================================

def normalizar_region(valor: Optional[str]) -> Optional[str]:
    """Homologa la etiqueta de región, especialmente la variación de PACÍFICA."""

    if pd.isna(valor):  # Si el valor es nulo → devuelve NA
        return pd.NA

    texto = str(valor).strip().upper()  # Convierte a mayúsculas y elimina espacios
    sin_tildes = texto.translate(str.maketrans("ÁÉÍÓÚ", "AEIOU"))  # Quita tildes

    # Corrige variaciones frecuentes de “PACÍFICA”
    if sin_tildes in {"PACIFICO", "PACIFICA"}:
        return "PACÍFICA"

    return texto


def normalizar_departamento(valor: Optional[str]) -> Optional[str]:
    """Devuelve el nombre canónico del departamento si es posible."""

    if pd.isna(valor):  # Maneja valores faltantes
        return pd.NA

    texto = str(valor).strip().upper()  # Limpia texto
    texto = texto.replace(".", " ").replace(",", " ")  # Elimina signos
    texto = re.sub(r"\s+", " ", texto)  # Unifica espacios
    sin_tildes = texto.translate(str.maketrans("ÁÉÍÓÚÜ", "AEIOUU"))  # Sin tildes

    # Retorna nombre corregido si existe en el diccionario
    return DEPARTMENT_CANONICAL.get(sin_tildes, texto)

# ============================================================
# Función principal para cargar y limpiar datos
# ============================================================

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Descarga, limpia y regresa el dataset ya procesado."""

    df = pd.read_csv(DATA_URL)  # Carga del CSV remoto

    # Limpia nombres de columnas que vienen con saltos de línea
    renames = {}
    for col in df.columns:
        if "\n" in col:
            renames[col] = col.split("\n")[0].strip()
    df = df.rename(columns=renames)

    df.columns = df.columns.str.upper().str.strip()  # Unifica a mayúsculas

    # --- Limpieza de PRODUCTO PRINCIPAL ---
    if "PRODUCTO PRINCIPAL" in df.columns:
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].astype(str).str.upper()
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].str.replace(".", "")
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].replace("MIEL", "MIEL DE ABEJAS")

    # --- Limpieza de AÑO ---
    if "AÑO" in df.columns:
        df["AÑO"] = df["AÑO"].astype(str).str.replace(",", "")
        df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce").astype("Int64")

    # --- Diccionario para inferir región desde autoridad ambiental ---
    mapeo_region = {
        # (Lista con decenas de entidades → región asignada)
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
        "EPA BARRANQUILLA VERDE": "CARIBE",
        "EPA BUENAVENTURA": "PACÍFICA",
        "EPA CARTAGENA": "CARIBE",
        "SDA": "ANDINA",
    }

    # Normalización de autoridad ambiental
    if "AUTORIDAD AMBIENTAL" in df.columns:
        df["AUTORIDAD AMBIENTAL"] = df["AUTORIDAD AMBIENTAL"].astype("string").str.strip().str.upper()

    # Normaliza región si ya existe
    if "REGIÓN" in df.columns:
        df["REGIÓN"] = df["REGIÓN"].astype("string").map(normalizar_region)

    # Función interna que asigna región si falta
    def asignar_region(row):
        region = row["REGIÓN"]

        # Si está vacío o dice "no registra", intenta usar autoridad ambiental
        if pd.isna(region) or str(region).lower() == "no registra":
            autoridad = row["AUTORIDAD AMBIENTAL"]
            return mapeo_region.get(autoridad, region)

        return region

    # Aplica lógica de asignación
    df["REGIÓN"] = df.apply(asignar_region, axis=1)
    df["REGIÓN"] = df["REGIÓN"].map(normalizar_region)

    # Normalización de departamento
    if "DEPARTAMENTO" in df.columns:
        df["DEPARTAMENTO"] = df["DEPARTAMENTO"].astype("string").map(normalizar_departamento)

    # --- Limpia numeración tipo "1.1.2." ---
    def limpiar_numeros(texto):
        if pd.isna(texto):
            return texto
        return re.sub(r"^\s*[\d\.]+\s*", "", str(texto))

    for col in ["CATEGORÍA", "SECTOR", "SUBSECTOR"]:
        if col in df.columns:
            df[col] = df[col].apply(limpiar_numeros)

    return df

# ============================================================
# Clasificación BASURA CERO
# ============================================================

# Diccionario de categorías y palabras clave detectables
categorias_basura_cero = {
    "Reciclaje/Reutilización": ["recicl", "reutiliz", "reuso", "aprovech"],
    "Compostaje/Biomasa": ["compost", "orgánic", "biomasa", "abono"],
    "Producción limpia": ["producción limpia", "transformación sostenible", "ecodiseño", "eficiencia"],
    "Economía circular": ["economía circular", "ciclo cerrado", "remanufactura"],
    "Bioinsumos/Bioproductos": ["bioinsumo", "biodegrad", "biofertiliz", "bioproduct"],
    "Energía renovable": ["energía solar", "energía renovable", "biogás", "panel solar", "fotovoltaic"],
    "Agroecología/Sostenibilidad rural": ["agroecolog", "agroindustria sostenible", "sostenible", "ecológica"],
}


def tipo_relacion_basura_cero(fila):
    """Detecta palabras clave y asigna categoría de economía circular."""
    texto = f"{fila['DESCRIPCIÓN']} {fila['SECTOR']} {fila['SUBSECTOR']}".lower()
    tipos = []

    # Revisa coincidencias con cada categoría
    for categoria, palabras in categorias_basura_cero.items():
        if any(p in texto for p in palabras):
            tipos.append(categoria)

    return ", ".join(tipos) if tipos else "No aplica"

# ============================================================
# Manejo de imágenes y estilos
# ============================================================

def img_to_base64(img_path):
    """Convierte una imagen local en base64 para usarla como fondo."""
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        # Solo muestra la advertencia una vez
        if not st.session_state.get("_banner_warning_shown", False):
            st.warning(f"Imagen no encontrada: {img_path}")
            st.session_state["_banner_warning_shown"] = True
        return None

# ============================================================
# Render del encabezado visual
# ============================================================

def render_header(df):
    """Dibuja banner, CSS y métricas del dataset."""

    banner_base64 = img_to_base64("img/verde2.png")
    # Si la imagen existe, configura CSS para usarla
    if banner_base64:
        background_css = (f'background-image: url("data:image/png;base64,{banner_base64}");')

    # Inserta estilos personalizados
    st.markdown(
        f"""
        <style>
        /* muchos estilos CSS (encabezado, métricas, banner, botones) */
                [data-testid="stHeader"] {{
            background: linear-gradient(90deg, #88C999, #A8E55A) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        [data-testid="stHeader"] * {{
            color: #1C3B2F !important;
        }}
        [data-testid="stAppViewContainer"], body {{
            background-color: #E6FFF7 !important;
            font-family: 'Arial', sans-serif;
            }}
        div[data-testid="stMetric"] {{
                background: rgba(255, 255, 255, 0.9);
                padding: 0.5rem 3rem;
                border-radius: 0.75rem;
                border: 2px solid rgba(74, 154, 135, 0.6);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                margin: 0.01rem auto;
                max-width: 200px;
                border: 2px solid rgba(74, 154, 135, 0.6);
            }}

            .metric {{
                background: #F0FFF4;
                padding: 15px;
                border-radius: 8px;
                border-left: 5px solid #A8E55A;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .banner-container {{
                position: relative;
                width: 100%;
                height: 220px;
                {background_css}
                background-size: cover;
                background-position: center;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 10px;
                border-bottom: 3px solid #c9b79c;
                margin-bottom: 1.5rem;
                overflow: hidden;
            }}
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
            .banner-container::before {{
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(45deg, rgba(0,0,0,0.45), rgba(0,0,0,0.15));
            }}
            .banner-container h1 {{
                position: relative;
                color: #ffffff;
                font-size: 2.2rem;
                text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.4);
                margin: 0;
                padding: 0 1rem;
                text-align: center;
            }}
        </style>
        <div class="banner-container">
            <h1>Basura Cero | Economía Circular</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Texto introductorio
    st.caption("Análisis exploratorio del registro nacional de negocios verdes.")

    # Métricas básicas
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros", f"{len(df):,}")
    col2.metric("Columnas", df.shape[1])
    col3.metric("Departamentos", df["DEPARTAMENTO"].nunique())

# ============================================================
# Resumen textual automático
# ============================================================

@st.cache_data(show_spinner=False)
def resumen_texto(df):
    """Genera texto resumen según los datos filtrados."""

    if df.empty:
        return "**No hay datos para mostrar.**"

    top_dep = df["DEPARTAMENTO"].value_counts().idxmax()
    top_sector = df["SECTOR"].value_counts().idxmax()
    year_min, year_max = df["AÑO"].min(), df["AÑO"].max()

    return textwrap.dedent(f"""
        **Resumen del subconjunto activo**

        * Departamento con más negocios: **{top_dep}**
        * Sector predominante: **{top_sector}**
        * Años cubiertos: **{year_min} – {year_max}**
    """)

# ============================================================
# Función auxiliar para evitar errores con df vacío
# ============================================================

def plot_if_not_empty(func, df):
    if df.empty:
        st.info("No hay datos con los filtros seleccionados.")
        return
    func(df)

# ============================================================
# Funciones de graficado
# ============================================================

def plot_top_departamentos(df):
    """Gráfico: Top 10 departamentos."""
    top = df["DEPARTAMENTO"].value_counts().head(10).sort_values()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top.values, y=top.index, palette="crest", ax=ax)
    ax.set_title("Top 10 Departamentos por número de negocios")
    st.pyplot(fig)

def plot_categoria_sector(df):
    """Gráfico: Categoría vs Sector."""
    data = df.groupby(["CATEGORÍA", "SECTOR"]).size().reset_index(name="Cantidad")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x="Cantidad", y="CATEGORÍA", hue="SECTOR", palette="Set2", ax=ax)
    st.pyplot(fig)

def plot_heatmap(df):
    """Mapa de calor Región vs Categoría."""
    matriz = pd.crosstab(df["REGIÓN"], df["CATEGORÍA"])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(matriz, cmap="YlGnBu", annot=True, fmt="d", linewidths=0.5, ax=ax)
    st.pyplot(fig)

def plot_tendencia_anual(df):
    """Línea de tiempo: negocios por año."""
    conteo = df.groupby("AÑO").size()

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.lineplot(x=conteo.index, y=conteo.values, marker="o", color="#4E7F96", ax=ax)
    st.pyplot(fig)

# ============================================================
# Función principal de la app
# ============================================================

def main():
    """Controlador principal de la aplicación Streamlit."""

    # Configura la página web
    st.set_page_config(
        page_title="Basura Cero | Economía Circular",
        layout="centered",
        page_icon="♻️",
    )

    # Ancho máximo del contenido
    st.markdown(
        "<style>.block-container {max-width: 900px;}</style>",
        unsafe_allow_html=True,
    )

    # Cargar datos
    df = load_data()

    # Clasificación Basura Cero
    df["Tipo_Relacion_Basura_Cero"] = df.apply(tipo_relacion_basura_cero, axis=1)
    df["Relacion_Basura_Cero"] = df["Tipo_Relacion_Basura_Cero"].apply(
        lambda x: "Sí" if x != "No aplica" else "No"
    )

    # ---------------------------------------------------------
    # 📌 Filtros en la barra lateral
    # ---------------------------------------------------------

    st.sidebar.header("Filtros")

    regiones = sorted(df["REGIÓN"].unique())
    departamentos = sorted(df["DEPARTAMENTO"].unique())
    categorias = sorted(df["CATEGORÍA"].unique())

    regiones_sel = st.sidebar.multiselect("Región", regiones, default=regiones)
    deptos_sel = st.sidebar.multiselect("Departamento", departamentos)
    categorias_sel = st.sidebar.multiselect("Categoría", categorias)

    # Aplicar filtros
    df_filtered = df[df["REGIÓN"].isin(regiones_sel)]

    if deptos_sel:
        df_filtered = df_filtered[df_filtered["DEPARTAMENTO"].isin(deptos_sel)]

    if categorias_sel:
        df_filtered = df_filtered[df_filtered["CATEGORÍA"].isin(categorias_sel)]

    # ---------------------------------------------------------
    # Render de encabezado y resumen
    # ---------------------------------------------------------
    render_header(df_filtered)

    st.markdown(resumen_texto(df_filtered))

    # Mostrar tabla filtrada
    with st.expander("Ver datos filtrados"):
        st.dataframe(df_filtered)

    # ---------------------------------------------------------
    # Graficación
    # ---------------------------------------------------------
    st.subheader("Exploración visual")

    plot_if_not_empty(plot_top_departamentos, df_filtered)
    plot_if_not_empty(plot_categoria_sector, df_filtered)
    plot_if_not_empty(plot_heatmap, df_filtered)
    plot_if_not_empty(plot_tendencia_anual, df_filtered)

    st.markdown("")

    col1, col2 = st.columns([1, 2])

    with col1:
        try:
            st.image(
                "img/mapa_basura_cero.jpg",
                caption="Fuente: Datos abiertos del Gobierno de Colombia (SSPD y MinVivienda, 2023–2024)",
                use_container_width=True,
            )

        except FileNotFoundError:
            st.image(
                "https://via.placeholder.com/300x200?text=Imagen+Ecológica",
                caption="Placeholder ecológico",
            )

    with col2:
        st.markdown(
            """
        El mapa muestra la **distribución geográfica de 12 proyectos del Programa Basura Cero**, 
        con una inversión total aproximada de **$119.212 millones de pesos**.  
        Estas iniciativas están orientadas a la **gestión integral de residuos**, el **aprovechamiento de materiales reciclables** y el **cierre progresivo de botaderos**.

    Explora el mapa para conocer en qué departamentos se están desarrollando los proyectos, su inversión y fase de avance. 
    """
        )
    # Pie de página
    st.caption("Fuente de datos: Ministerio de Ambiente y Desarrollo Sostenible.")

# ============================================================
# Ejecutar aplicación
# ============================================================

if __name__ == "__main__":
    main()
# Aplicación Streamlit para explorar negocios verdes en Colombia.
# ==============================================================
# 🌿 Proyecto: Dashboard de Negocios Ecológicos
# Autor: Angie Ruiz
#        Natacha Ochoa
#        Paulina Noreña
#        Juan Ignacio García
#        Thomas Medina
# Descripción:
#   Esta aplicación muestra una aplicacion en Streamlit con
#   estilo ecológico, una visualización de datos limpia y moderna,
#   integrando banner superior e inferior, información general,.
# ==============================================================

# ==============================================================
#                      --- Notas de la versión ---
# ==============================================================
# En esta version se realizo notas aclaratorias en la mayoria de
# las lineas y se organizo en secciones
# ==============================================================
#                      --- Librerías ---
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
import plotly.express as px
import streamlit as st           # Framework de interfaz web.

# ============================================================
# --- Cargar el dataset desde desde GitHub --- 
# ============================================================

# URL del archivo CSV que contiene el listado de Negocios Verdes.
# Se descarga directamente desde un repositorio de GitHub.
DATA_URL = (
    "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/"
    "Listado_de_Negocios_Verdes_20251025.csv"
)

# ==============================================================
# --- 🌈 Diccionarios globales (colores, coordenadas, etc.) ---
# ==============================================================

# ---Diccionario canonico por departamento---
DEPARTMENT_CANONICAL = {
    "AMAZONAS":"AMAZONAS","ANTIOQUIA":"ANTIOQUIA","ARAUCA":"ARAUCA","ATLANTICO":"ATLÁNTICO","ATLÁNTICO":"ATLÁNTICO","BOLIVAR":"BOLÍVAR","BOLÍVAR":"BOLÍVAR","BOGOTA":"BOGOTÁ, D.C.","BOGOTA DC":"BOGOTÁ, D.C.","BOGOTA D C":"BOGOTÁ, D.C.","BOGOTA D.C":"BOGOTÁ, D.C.","BOGOTÁ":"BOGOTÁ, D.C.","BOGOTÁ D.C.":"BOGOTÁ, D.C.","BOYACA":"BOYACÁ","BOYACÁ":"BOYACÁ","CALDAS":"CALDAS","CAQUETA":"CAQUETÁ","CAQUETÁ":"CAQUETÁ","CASANARE":"CASANARE","CAUCA":"CAUCA","CESAR":"CESAR","CHOCO":"CHOCÓ","CHOCÓ":"CHOCÓ","CORDOBA":"CÓRDOBA","CÓRDOBA":"CÓRDOBA","CUNDINAMARCA":"CUNDINAMARCA",
    "GUAINIA":"GUAINÍA","GUAINÍA":"GUAINÍA","GUAJIRA":"LA GUAJIRA","LA GUAJIRA":"LA GUAJIRA","GUAVIARE":"GUAVIARE","HUILA":"HUILA","MAGDALENA":"MAGDALENA","META":"META","NARINO":"NARIÑO","NARIÑO":"NARIÑO","NORTE DE SANTANDER":"NORTE DE SANTANDER","PUTUMAYO":"PUTUMAYO","QUINDIO":"QUINDÍO","QUINDÍO":"QUINDÍO","RISARALDA":"RISARALDA",
    "SAN ANDRES": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA", "SAN ANDRÉS": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA", "SAN ANDRES Y PROVIDENCIA": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA", "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
    "ARCHIPIÉLAGO DE SAN ANDRÉS PROVIDENCIA Y SANTA CATALINA": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA", "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA", "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA": "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA", "SANTANDER":"SANTANDER","SUCRE":"SUCRE","TOLIMA":"TOLIMA","VALLE":"VALLE DEL CAUCA","VALLE DEL CAUCA":"VALLE DEL CAUCA","VAUPES":"VAUPÉS","VAUPÉS":"VAUPÉS","VICHADA":"VICHADA"
}
# Diccionario que almacena las coordenadas geográficas (latitud y longitud) 
DEPARTMENT_COORDS = {
    "AMAZONAS": {"lat": -1.566, "lon": -72.640}, "ANTIOQUIA": {"lat": 7.1986, "lon": -75.3412}, "ARAUCA": {"lat": 6.5519, "lon": -70.9410}, "ATLÁNTICO": {"lat": 10.6966, "lon": -74.8741}, "BOGOTÁ, D.C.": {"lat": 4.6097, "lon": -74.0817}, "BOLÍVAR": {"lat": 9.1938, "lon": -74.9120}, "BOYACÁ": {"lat": 5.5450, "lon": -73.3678}, "CALDAS": {"lat": 5.2983, "lon": -75.2479}, "CAQUETÁ": {"lat": 0.8699, "lon": -73.8419}, "CASANARE": {"lat": 5.7589, "lon": -71.5724}, "CAUCA": {"lat": 2.4068, "lon": -76.7250},
    "CESAR": {"lat": 9.3373, "lon": -73.6536}, "CHOCÓ": {"lat": 5.6947, "lon": -76.6583}, "CÓRDOBA": {"lat": 8.7496, "lon": -75.8735}, "CUNDINAMARCA": {"lat": 4.8143, "lon": -74.3540}, "GUAINÍA": {"lat": 2.5658, "lon": -68.5247}, "LA GUAJIRA": {"lat": 11.3548, "lon": -72.5205}, "GUAVIARE": {"lat": 1.8537, "lon": -72.9087}, "HUILA": {"lat": 2.9273, "lon": -75.2819}, "MAGDALENA": {"lat": 10.2373, "lon": -74.2064}, "META": {"lat": 3.4760, "lon": -73.7517}, "NARIÑO": {"lat": 1.2894, "lon": -77.3570},
    "NORTE DE SANTANDER": {"lat": 7.9463, "lon": -72.8988}, "PUTUMAYO": {"lat": 0.4416, "lon": -76.6270}, "QUINDÍO": {"lat": 4.4610, "lon": -75.6674}, "RISARALDA": {"lat": 4.9820, "lon": -75.6039}, "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA": {"lat": 12.5589, "lon": -81.7188}, "SANTANDER": {"lat": 6.6437, "lon": -73.6531}, "SUCRE": {"lat": 9.3164, "lon": -75.3972}, "TOLIMA": {"lat": 4.0925, "lon": -75.1545}, "VALLE DEL CAUCA": {"lat": 3.5297, "lon": -76.3035}, "VAUPÉS": {"lat": 0.8554, "lon": -70.8110}, "VICHADA": {"lat": 4.4234, "lon": -69.2878},
}

#---Diccionario de colores por departamento---
DEPARTMENT_COLORS = {
    "AMAZONAS": "#A6CEE3", "ANTIOQUIA": "#1F78B4", "ARAUCA": "#B2DF8A", "ATLÁNTICO": "#33A02C", "BOLÍVAR": "#FB9A99", "BOYACÁ": "#E31A1C", "CALDAS": "#FDBF6F", "CAQUETÁ": "#FF7F00", "CASANARE": "#CAB2D6", "CAUCA": "#6A3D9A", "CESAR": "#FFFF99", "CHOCÓ": "#B15928",
    "CÓRDOBA": "#8DD3C7", "CUNDINAMARCA": "#FFFFB3", "GUAINÍA": "#BEBADA", "GUAVIARE": "#FB8072", "HUILA": "#80B1D3", "LA GUAJIRA": "#FDB462", "MAGDALENA": "#B3DE69", "META": "#FCCDE5", "NARIÑO": "#D9D9D9", "NORTE DE SANTANDER": "#BC80BD", "PUTUMAYO": "#CCEBC5",
    "QUINDÍO": "#FFED6F", "RISARALDA": "#1B9E77", "SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA": "#D95F02", "SANTANDER": "#7570B3", "SUCRE": "#E7298A", "TOLIMA": "#66A61E", "VALLE DEL CAUCA": "#E6AB02", "VAUPÉS": "#A6761D", "VICHADA": "#666666",
}

#---Diccionario de colores por región---
REGION_COLORS = {
    "CARIBE": "#FFD92F", "ANDINA": "#1F78B4", "PACÍFICO": "#33A02C", "ORINOQUÍA": "#FB9A99", "AMAZONÍA": "#B2DF8A",
}

# --- Diccionario para inferir región desde autoridad ambiental ---
MAPEO_REGION = {
        "AMVA": "ANDINA", "CAM": "ANDINA", "CAR": "ANDINA", "CARDER": "ANDINA", "CARDIQUE": "CARIBE", "CARSUCRE": "CARIBE", "CAS": "ANDINA", "CDA": "AMAZONÍA", "CDMB": "ANDINA", "CODECHOCÓ": "PACÍFICO", "CORALINA": "INSULAR", "CORANTIOQUIA": "ANDINA",
        "CORMACARENA": "ORINOQUÍA", "CORNARE": "ANDINA", "CORPAMAG": "CARIBE", "CORPOAMAZONÍA": "AMAZONÍA", "CORPOBOYACÁ": "ANDINA", "CORPOCALDAS": "ANDINA", "CORPOCESAR": "CARIBE", "CORPOCHIVOR": "ANDINA", "CORPOGUAJIRA": "CARIBE", "CORPOGUAVIO": "ANDINA", "CORPOMOJANA": "CARIBE",
        "CORPONARIÑO": "PACÍFICO", "CORPONOR": "CARIBE", "CORPORINOQUÍA": "ORINOQUÍA", "CORPOURABÁ": "PACÍFICO", "CORTOLIMA": "ANDINA", "CRA": "CARIBE", "CRC": "PACÍFICO", "CRQ": "ANDINA", "CSB": "CARIBE", "CVC": "PACÍFICO", "CVS": "CARIBE",
        "DADSA": "ANDINA", "DAGMA": "ANDINA", "EPA BARRANQUILLA VERDE": "CARIBE", "EPA BUENAVENTURA": "PACÍFICO", "EPA CARTAGENA": "CARIBE", "SDA": "ANDINA",
    }

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

# ============================================================
#               --- Funciones auxiliares--- 
# ============================================================

def normalizar_region(region: str) -> Optional[str]:
    """Normaliza el nombre de una región a su forma estandarizada."""
    if pd.isna(region):
        return None
    region = str(region).strip().upper()
    reemplazos = {
        "CARIBE": "CARIBE",
        "ANDINA": "ANDINA",
        "PACIFICO": "PACÍFICO",
        "PACÍFICO": "PACÍFICO",
        "ORINOQUIA": "ORINOQUÍA",
        "ORINOQUÍA": "ORINOQUÍA",
        "AMAZONIA": "AMAZONÍA",
        "AMAZONÍA": "AMAZONÍA",
    }
    return reemplazos.get(region, region)

def normalizar_departamento(valor: Optional[str]) -> Optional[str]:
    """Normaliza el nombre de un departamento y devuelve su forma canónica."""
    if pd.isna(valor):
        return pd.NA

    texto = str(valor).strip().upper()
    texto = texto.replace(".", " ").replace(",", " ")
    texto = re.sub(r"\s+", " ", texto)

    # → Si no existe en el diccionario, devolver texto limpio (tu elección)
    return DEPARTMENT_CANONICAL.get(texto, texto)

def coordenadas_departamento(nombre: Optional[str]):
    """Obtiene las coordenadas del departamento con base en su nombre canónico."""

    if pd.isna(nombre):
        return None

    clave = DEPARTMENT_CANONICAL.get(str(nombre).strip().upper(), None)
    if clave is None:
        return None
    return DEPARTMENT_COORDS.get(clave)

def limpiar_numeros(texto: str) -> str:
    """Elimina prefijos numéricos tipo '1.2.3. ' al inicio del texto."""
    if pd.isna(texto):
        return texto
    return re.sub(r"^\s*[\d\.]+\s*", "", str(texto))

def tipo_relacion_basura_cero(fila):
    """Detecta palabras clave y asigna categoría de economía circular."""
    texto = f"{fila['DESCRIPCIÓN']} {fila['SECTOR']} {fila['SUBSECTOR']}".lower()
    tipos = []

    # Revisa coincidencias con cada categoría
    for categoria, palabras in categorias_basura_cero.items():
        if any(p in texto for p in palabras):
            tipos.append(categoria)

    return ", ".join(tipos) if tipos else "No aplica"

def tiene_relacion_basura_cero(valor):
    if pd.isna(valor):
        return False
    valor = str(valor).strip().lower()
    return valor not in ["", "no aplica", "no disponible"]
def plot_tendencia_anual(df):
    """Línea de tiempo: negocios registrados por año."""
    df_anual = df.dropna(subset=["AÑO"])

    if df_anual.empty:
        st.info("No hay datos válidos de 'AÑO' para mostrar la tendencia anual.")
        return

    conteo = df_anual.groupby("AÑO").size()

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.lineplot(x=conteo.index, y=conteo.values, marker="o", color="#4E7F96", ax=ax)

    ax.set_title("Tendencia anual de negocios verdes", fontsize=12, weight="bold")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de registros")

    st.pyplot(fig)


# ============================================================
# Función auxiliar para evitar errores con df vacío
# ============================================================

def plot_if_not_empty(func, df):
    if df.empty:
        st.info("No hay datos con los filtros seleccionados.")
        return
    func(df)
# ============================================================
#     --- Función principal de carga y limpieza --- 
# ============================================================
@st.cache_data(show_spinner=False)
def load_data(dummy: int = 1) -> pd.DataFrame:
    """Carga el dataset desde GitHub, lo limpia y devuelve un DataFrame listo para usar."""
    df = pd.read_csv(DATA_URL)

    # Limpieza de columnas con saltos
    renames = {col: col.split("\n")[0] for col in df.columns if "\n" in col}
    df = df.rename(columns=renames)
    df.columns = df.columns.str.upper().str.strip()

    # Limpieza de AÑO
    if "AÑO" in df.columns:
        df["AÑO"] = df["AÑO"].astype(str).str.replace(",", "")
        df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce").astype("Int64")

    # Normalizar AUTORIDAD AMBIENTAL
    if "AUTORIDAD AMBIENTAL" in df.columns:
        df["AUTORIDAD AMBIENTAL"] = df["AUTORIDAD AMBIENTAL"].astype("string").str.strip().str.upper()

    # Normalizar REGIÓN
    if "REGIÓN" in df.columns:
        df["REGIÓN"] = df["REGIÓN"].astype("string").map(normalizar_region)

        # Asignar región faltante
        def asignar_region(row):
            region = row["REGIÓN"]
            if pd.isna(region) or str(region).lower() == "no registra":
                return MAPEO_REGION.get(row["AUTORIDAD AMBIENTAL"], region)
            return region

        df["REGIÓN"] = df.apply(asignar_region, axis=1)
        df["REGIÓN"] = df["REGIÓN"].map(normalizar_region)

    # Normalizar DEPARTAMENTO
    if "DEPARTAMENTO" in df.columns:
        df["DEPARTAMENTO"] = df["DEPARTAMENTO"].astype("string").map(normalizar_departamento)

    # Limpiar numeración en categorías
    for col in ["CATEGORÍA", "SECTOR", "SUBSECTOR"]:
        if col in df.columns:
            df[col] = df[col].apply(limpiar_numeros)

    # Limpieza de PRODUCTO PRINCIPAL
    if "PRODUCTO PRINCIPAL" in df.columns:
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].astype(str).str.upper()
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].str.replace(".", "", regex=False)
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].replace({"MIEL": "MIEL DE ABEJAS"})

    # Clasificación BASURA CERO : Crear nueva columna: clasificación BASURA CERO
    if all(col in df.columns for col in ["DESCRIPCIÓN", "SECTOR", "SUBSECTOR"]):
        df["RELACIÓN BASURA CERO"] = df.apply(tipo_relacion_basura_cero, axis=1)

    # Crear columna BASURA 0 (Sí / No)
    if "RELACIÓN BASURA CERO" in df.columns:
        df["BASURA 0"] = df["RELACIÓN BASURA CERO"].apply(
            lambda x: "Sí" if pd.notna(x) and str(x).strip() != "" and str(x).lower() != "no aplica" else "No"
        )
    #Entrego el DataFrame ya limpio
    return df
#Cargar DataFrame
df = load_data()

# ------------------------------------------------------------
# 🌿 Función: Convertir imagen a base64 para usar en el banner
# ------------------------------------------------------------
def img_to_base64(img_path: str) -> Optional[str]:
    """Convierte una imagen local en una cadena base64.

    Si la imagen no existe, se devuelve ``None`` y se muestra
    una advertencia en la interfaz.
    """

    try:
        with open(img_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode()
        return b64_data
    except FileNotFoundError:
        st.warning(f"Imagen no encontrada en {img_path}. Usando placeholder.")
        return None

# ------------------------------------------------------------
# 🛠️ Funciones de renderizado por sección
# ------------------------------------------------------------
def render_home(df: pd.DataFrame) -> None:
    """Muestra la pantalla principal con el banner superior."""
    st.markdown("""
        <div class="banner">
            🌿 Residuos con propósito: Colombia hacia la Economía Circular 🌿
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## Bienvenido al Dashboard de Negocios Verdes en Colombia")
    st.write("Este panel permite explorar información limpia, estandarizada y enriquecida con indicadores de Economía Circular.")
    
    # Texto introductorio
    st.caption("Análisis exploratorio del registro nacional de negocios verdes.")
    st.markdown(resumen_texto(df))
    # Métricas básicas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📄</div>
                <div class="metric-content">
                    <div class="metric-label">Registros</div>
                    <div class="metric-value">{len(df):,}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-content">
                    <div class="metric-label">Columnas</div>
                    <div class="metric-value">{df.shape[1]}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🗺️</div>
                <div class="metric-content">
                    <div class="metric-label">Departamentos</div>
                    <div class="metric-value">{df["DEPARTAMENTO"].nunique()}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
   
    st.markdown("")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            "img/mapa_basura_cero.jpg",
            caption="Fuente: Datos abiertos del Gobierno de Colombia (SSPD y MinVivienda, 2023–2024)",
            use_container_width=True,
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

@st.cache_data(show_spinner=False)
def obtener_opciones_filtros(df: pd.DataFrame):
    """Precalcula y cachea las opciones únicas para los filtros del expander."""
    # Opciones de REGIÓN
    if "REGIÓN" in df.columns:
        regiones = sorted(
            region
            for region in df["REGIÓN"].dropna().unique().tolist()
            if str(region).strip()
        )
    else:
        regiones = []

    # Opciones de SECTOR
    if "SECTOR" in df.columns:
        sectores = sorted(
            sector
            for sector in df["SECTOR"].dropna().unique().tolist()
            if str(sector).strip()
        )
    else:
        sectores = []

    # Opciones de RELACIÓN BASURA CERO
    if "RELACIÓN BASURA CERO" in df.columns:
        categorias_relacion = sorted(
            {
                categoria.strip()
                for valor in df["RELACIÓN BASURA CERO"].dropna()
                for categoria in str(valor).split(",")
                if categoria.strip()
                and categoria.strip().lower()
                not in {"no aplica", "no disponible"}
            }
        )
    else:
        categorias_relacion = []

    return regiones, sectores, categorias_relacion

# ============================================================
#                     --- APP UI ---
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
    st.sidebar.header("Navegación")
    section = st.sidebar.radio(
        "Selecciona una sección",
        ("Inicio", "Mapa del sitio", "Preguntas frecuentes"),
        index=0,
    )

    st.sidebar.markdown(
        """
        ---
        **Tip:** Desde la sección Inicio puedes descargar la base normalizada 
        y acceder a la visualización de sectores líderes.
        """
    )

    if section == "Inicio":
        render_home(df)
        # ============================================================
        # 2️⃣ Mostrar el DataFrame en un contenedor expandible
        # ============================================================
        # Se usa un expander para no ocupar demasiado espacio visual,
        # permitiendo al usuario desplegar o contraer la vista del DataFrame.
        
        if not df.empty and {"DEPARTAMENTO", "RELACIÓN BASURA CERO"}.issubset(df.columns):
            mapa_df = df.copy()
            relacion_normalizada = (
                mapa_df["RELACIÓN BASURA CERO"].fillna("").astype(str).str.strip().str.lower()
            )
            mapa_df["TIENE_RELACION"] = ~relacion_normalizada.isin(
                {"", "no aplica", "no disponible"}
            )

            resumen_departamentos = (
                mapa_df.groupby("DEPARTAMENTO")
                .agg(TOTAL=("DEPARTAMENTO", "size"), ALINEADOS=("TIENE_RELACION", "sum"))
                .reset_index()
            )
            resumen_departamentos["ALINEADOS"] = resumen_departamentos["ALINEADOS"].astype(int)
            resumen_departamentos["PORCENTAJE"] = (
                resumen_departamentos["ALINEADOS"] / resumen_departamentos["TOTAL"]
            ) * 100
            resumen_departamentos["PORCENTAJE"] = resumen_departamentos["PORCENTAJE"].round(1)
            resumen_departamentos["COORDS"] = resumen_departamentos["DEPARTAMENTO"].apply(
                coordenadas_departamento
            )
            resumen_departamentos = resumen_departamentos.dropna(subset=["COORDS"])

            if not resumen_departamentos.empty:
                resumen_departamentos["lat"] = resumen_departamentos["COORDS"].apply(
                    lambda item: item["lat"]
                )
                resumen_departamentos["lon"] = resumen_departamentos["COORDS"].apply(
                    lambda item: item["lon"]
                )

                st.markdown("### 🗺️ Mapa interactivo: intensidad Basura Cero por departamento")
                fig_map = px.scatter_mapbox(
                    resumen_departamentos,
                    lat="lat",
                    lon="lon",
                    size="TOTAL",
                    size_max=45,
                    color="PORCENTAJE",
                    color_continuous_scale="Greens",
                    hover_name="DEPARTAMENTO",
                    hover_data={
                        "TOTAL": True,
                        "ALINEADOS": True,
                        "PORCENTAJE": ":.1f",
                        "lat": False,
                        "lon": False,
                    },
                    zoom=4.2,
                    center={"lat": 4.5, "lon": -74.1},
                    mapbox_style="carto-positron",
                )
                fig_map.update_layout(
                    margin={"l": 0, "r": 0, "t": 0, "b": 0},
                    coloraxis_colorbar={"title": "% alineadas"},
                )
                st.plotly_chart(fig_map, use_container_width=True)
                st.caption(
                    "El tamaño del marcador refleja el total de negocios verdes en el departamento "
                    "y el color indica el porcentaje con relación identificada al programa Basura Cero."
                )

        st.markdown("")

        if not df.empty and "SECTOR" in df.columns and not df["SECTOR"].isna().all():
            st.markdown("### 🌿 Top 10 Sectores con más Negocios Verdes")

            custom_palette = [
                "#E6FFF7",
                "#B2F2E8",
                "#66D1BA",
                "#1FA88E",
                "#0B5C4A",
                "#A8E55A",
                "#88C999",
                "#C9B79C",
                "#7BBF8A",
                "#9CD25B",
            ]

            top_sectores = df["SECTOR"].value_counts().head(10)

            sns.set_style("whitegrid")
            plt.rcParams["font.family"] = "Arial"

            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(
                x=top_sectores.values,
                y=top_sectores.index,
                palette=custom_palette[: len(top_sectores)],
                edgecolor="#0B5C4A",
                ax=ax,
            )

            for container in ax.containers:
                ax.bar_label(container, fmt="%d", padding=3, fontsize=9, color="#0B5C4A")

            ax.set_title(
                "Top 10 Sectores con más Negocios Verdes",
                fontsize=12,
                weight="bold",
                color="#0B5C4A",
                pad=10,
            )
            ax.set_xlabel("Número de Negocios", fontsize=10, color="#0B5C4A")
            ax.set_ylabel("Sector", fontsize=10, color="#0B5C4A")
            sns.despine(left=True, bottom=True)
            plt.tight_layout()

            st.pyplot(fig)
        else:
            st.warning(
                "La columna 'SECTOR' no está presente, está vacía o no contiene datos válidos. "
                "No se puede generar la visualización. Verifica el dataset y la limpieza aplicada."
            )

        # 📈 -----------------------------------------------------------
        # TENDENCIA ANUAL
        # --------------------------------------------------------------
        st.markdown("### 📈 Tendencia anual de negocios verdes")
        plot_tendencia_anual(df)
        st.markdown("")  # Espacio visual

        if (
            not df.empty
            and "RELACIÓN BASURA CERO" in df.columns
            and not df["RELACIÓN BASURA CERO"].isna().all()
        ):
            st.markdown("### ♻️ Relación con el programa Basura Cero")
            st.markdown(
                """
                La siguiente clasificación busca identificar cómo cada iniciativa se conecta con los pilares del
                programa **Basura Cero**. Se analizan palabras clave en la descripción, sector y subsector para
                agrupar los proyectos según su enfoque.
                """
            )

            resumen_relacion = (
                df["RELACIÓN BASURA CERO"]
                .fillna("No aplica")
                .apply(
                    lambda valor: (
                        "Iniciativas alineadas"
                        if str(valor).strip().lower()
                        not in {"no aplica", "no disponible", ""}
                        else "Sin relación identificada"
                    )
                )
                .value_counts()
                .rename_axis("Relación")
                .reset_index(name="Total")
            )

            if not resumen_relacion.empty:
                fig_relacion = px.pie(
                    resumen_relacion,
                    names="Relación",
                    values="Total",
                    color="Relación",
                    color_discrete_map={
                        "Iniciativas alineadas": "#1FA88E",
                        "Sin relación identificada": "#C9B79C",
                    },
                    hole=0.35,
                )
                fig_relacion.update_traces(
                    hovertemplate=(
                        "<b>%{label}</b><br>Participación: %{percent}" "<br>Cantidad: %{value}<extra></extra>"
                    ),
                    textinfo="percent+label",
                    textposition="inside",
                )
                fig_relacion.update_layout(margin=dict(l=0, r=0, t=30, b=0))

                st.plotly_chart(fig_relacion, use_container_width=True)
            else:
                st.info(
                    "No se pudo calcular la proporción de iniciativas alineadas con el programa Basura Cero."
                )

            relacion_series = (
                df["RELACIÓN BASURA CERO"]
                .fillna("No aplica")
                .str.get_dummies(sep=", ")
                .sum()
                .sort_values(ascending=False)
            )

            if not relacion_series.empty:
                st.markdown("#### Distribución general por categoría")
                fig_rel, ax_rel = plt.subplots(figsize=(7, 4))
                sns.barplot(
                    x=relacion_series.values,
                    y=relacion_series.index,
                    palette="Greens",
                    edgecolor="#0B5C4A",
                    ax=ax_rel,
                )
                ax_rel.set_xlabel("Número de iniciativas", fontsize=10, color="#0B5C4A")
                ax_rel.set_ylabel("Categoría Basura Cero", fontsize=10, color="#0B5C4A")
                ax_rel.set_title(
                    "Iniciativas clasificadas por su relación con Basura Cero",
                    fontsize=12,
                    weight="bold",
                    color="#0B5C4A",
                )
                for container in ax_rel.containers:
                    ax_rel.bar_label(
                        container,
                        fmt="%d",
                        padding=3,
                        fontsize=9,
                        color="#0B5C4A",
                    )
                sns.despine(left=True, bottom=True)
                plt.tight_layout()
                st.pyplot(fig_rel)

            if "REGIÓN" in df.columns:
                relacion_exploded = (
                    df.assign(
                        **{
                            "RELACIÓN BASURA CERO": df["RELACIÓN BASURA CERO"]
                            .fillna("No aplica")
                            .str.split(", ")
                        }
                    )
                    .explode("RELACIÓN BASURA CERO")
                )
                relacion_exploded["RELACIÓN BASURA CERO"] = (
                    relacion_exploded["RELACIÓN BASURA CERO"].astype(str).str.strip()
                )
                relacion_exploded = relacion_exploded[
                    relacion_exploded["RELACIÓN BASURA CERO"].str.lower() != "no aplica"
                ]

                if not relacion_exploded.empty:
                    relacion_por_region = (
                        relacion_exploded.groupby(["REGIÓN", "RELACIÓN BASURA CERO"])
                        .size()
                        .reset_index(name="TOTAL")
                    )

                    if not relacion_por_region.empty:
                        st.markdown("#### Intensidad de categorías por región")
                        pivot = relacion_por_region.pivot(
                            index="REGIÓN",
                            columns="RELACIÓN BASURA CERO",
                            values="TOTAL",
                        ).fillna(0)

                        fig_heat, ax_heat = plt.subplots(
                            figsize=(8, max(3, 0.5 * len(pivot.index)))
                        )
                        sns.heatmap(
                            pivot,
                            cmap="Greens",
                            annot=True,
                            fmt=".0f",
                            linewidths=0.5,
                            cbar_kws={"label": "Número de iniciativas"},
                            ax=ax_heat,
                        )
                        ax_heat.set_xlabel("Categoría Basura Cero", color="#0B5C4A", fontsize=10)
                        ax_heat.set_ylabel("Región", color="#0B5C4A", fontsize=10)
                        ax_heat.set_title(
                            "Mapa de calor: enfoques Basura Cero por región",
                            color="#0B5C4A",
                            fontsize=12,
                            weight="bold",
                            pad=10,
                        )
                        plt.tight_layout()
                        st.pyplot(fig_heat)

        if (
            "AUTORIDAD AMBIENTAL" in df.columns
            and not df["AUTORIDAD AMBIENTAL"].isna().all()
        ):
            st.markdown("### 🏛️ Autoridades ambientales y Basura Cero")
            st.markdown(
                """
    Conoce qué tan activa está cada autoridad ambiental en el programa y cómo se distribuyen
    las iniciativas con relación identificada a **Basura Cero**.
    """
            )

            autoridades_norm = (
                df["AUTORIDAD AMBIENTAL"]
                .fillna("No registra")
                .astype(str)
                .str.strip()
                .replace("", "No registra")
            )

            top_autoridades = (
                autoridades_norm.value_counts()
                .head(15)
                .reset_index(name="Total")
                .rename(columns={"index": "AUTORIDAD AMBIENTAL"})
                .sort_values("Total")
            )

            if not top_autoridades.empty:
                fig_aut = px.bar(
                    top_autoridades,
                    x="Total",
                    y="AUTORIDAD AMBIENTAL",
                    orientation="h",
                    color="Total",
                    color_continuous_scale="Greens",
                    text="Total",
                )
                fig_aut.update_traces(
                    hovertemplate=(
                        "<b>%{y}</b><br>Total de iniciativas: %{x}<extra></extra>"
                    ),
                    textposition="outside",
                )
                fig_aut.update_layout(
                    coloraxis_showscale=False,
                    xaxis_title="Número de iniciativas registradas",
                    yaxis_title="Autoridad ambiental",
                    margin=dict(l=0, r=30, t=30, b=0),
                )
                st.plotly_chart(fig_aut, use_container_width=True)
                st.caption(
                    "Las barras muestran las autoridades con mayor número de registros en el dataset."
                )

            autoridades_df = df.assign(
                AUTORIDAD_NORMALIZADA=autoridades_norm,
                ESTADO_ALINEACIÓN=df["RELACIÓN BASURA CERO"].apply(
                    lambda valor: (
                        "Iniciativas alineadas"
                        if tiene_relacion_basura_cero(valor)
                        else "Sin relación identificada"
                    )
                ),
            )

            principales_autoridades = top_autoridades["AUTORIDAD AMBIENTAL"].tolist()

            distribucion_autoridad = (
                autoridades_df[autoridades_df["AUTORIDAD_NORMALIZADA"].isin(principales_autoridades)]
                .groupby(["AUTORIDAD_NORMALIZADA", "ESTADO_ALINEACIÓN"])
                .size()
                .reset_index(name="Total")
            )

            if not distribucion_autoridad.empty:
                distribucion_autoridad["Porcentaje"] = (
                    distribucion_autoridad["Total"]
                    / distribucion_autoridad.groupby("AUTORIDAD_NORMALIZADA")["Total"].transform("sum")
                    * 100
                )
                orden_autoridades = (
                    top_autoridades.sort_values("Total", ascending=False)["AUTORIDAD AMBIENTAL"].tolist()
                )
                fig_aut_stack = px.bar(
                    distribucion_autoridad,
                    x="Total",
                    y="AUTORIDAD_NORMALIZADA",
                    color="ESTADO_ALINEACIÓN",
                    orientation="h",
                    category_orders={"AUTORIDAD_NORMALIZADA": orden_autoridades},
                    color_discrete_map={
                        "Iniciativas alineadas": "#1FA88E",
                        "Sin relación identificada": "#C9B79C",
                    },
                    custom_data=["Porcentaje"],
                )
                fig_aut_stack.update_traces(
                    hovertemplate=(
                        "<b>%{y}</b><br>%{color}<br>Total: %{x}<br>Participación: %{customdata[0]:.1f}%<extra></extra>"
                    )
                )
                fig_aut_stack.update_layout(
                    barmode="stack",
                    xaxis_title="Número de iniciativas",
                    yaxis_title="Autoridad ambiental",
                    legend_title="Estado de la relación",
                    margin=dict(l=0, r=30, t=30, b=0),
                )
                st.plotly_chart(fig_aut_stack, use_container_width=True)
                st.caption(
                    "El gráfico apilado indica cuántas iniciativas de cada autoridad tienen relación identificada"
                    " con Basura Cero frente a las que aún no muestran esa alineación."
                )

                    # Precalcular y cachear opciones de filtros para mejorar rendimiento
            regiones_op, sectores_op, categorias_relacion_op = obtener_opciones_filtros(df)

            if not df.empty:
                with st.expander("📊 Ver Listado_de_Negocios_Verdes"):
                    
                    st.caption(
                        "La descarga incluye la base completa normalizada, independientemente de los filtros aplicados."
                    )
                    csv_full = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Descargar Base de Datos en CSV",
                        data=csv_full,
                        file_name="negocios_verdes_normalizados.csv",
                        mime="text/csv",
                    )
                    filtered_df = df.copy()

                    if "REGIÓN" in df.columns and regiones_op:
                            seleccion_regiones = st.multiselect(
                                "Selecciona regiones",
                                regiones_op,
                                help="Elige una o más regiones para focalizar la vista de la tabla.",
                            )
                            if seleccion_regiones:
                                filtered_df = filtered_df[
                                    filtered_df["REGIÓN"].isin(seleccion_regiones)]

                    if "SECTOR" in df.columns and sectores_op:
                        seleccion_sectores = st.multiselect(
                            "Selecciona sectores",
                            sectores_op,
                            help="Delimita la tabla a los sectores de tu interés.",
                        )
                        if seleccion_sectores:
                            filtered_df = filtered_df[
                                filtered_df["SECTOR"].isin(seleccion_sectores)]
                            
                    if "RELACIÓN BASURA CERO" in df.columns and categorias_relacion_op:
                        seleccion_relacion = st.multiselect(
                            "Categorías Basura Cero",
                            categorias_relacion_op,
                            help=(
                                "Filtra iniciativas que mencionen explícitamente las categorías "
                                "asociadas al programa Basura Cero."
                            ),
                        )
                        if seleccion_relacion:
                            # Construir un patrón de búsqueda eficiente
                            import re as _re

                            patron = "|".join(
                                _re.escape(cat) for cat in seleccion_relacion
                            )
                            series_rel = (
                                filtered_df["RELACIÓN BASURA CERO"]
                                .fillna("")
                                .astype(str)
                            )
                            mask_relacion = series_rel.str.contains(
                                patron, regex=True
                            )
                            filtered_df = filtered_df[mask_relacion]

                    st.dataframe(filtered_df, use_container_width=True)
    
        
        st.markdown(
            """
            <div class="banner-inferior"; style="text-align: center; font-size: 14px;">
                <strong>🌿 autores: 🌿 </strong><br>
                Paulina Noreña · pnorena@unal.edu.co<br>
                Thomas Medina · thomasmedina519@gmail.com<br>
                Angie Ruiz · angiecarorumer333@gmail.com<br>
                Natacha Ochoa · ochoa0917@hotmail.com<br>
                Juan Ignacio García · juanignaciogarcia7@gmail.com
            </div>
            """,
                    unsafe_allow_html=True,
                )
        st.markdown(
                    """
            💚 *Proyecto académico realizado con Streamlit - Inspirado en la sostenibilidad y el diseño ecológico.*  
            """
                )

    elif section == "Mapa del sitio":
        render_sitemap()
    else:
        render_faq()

    # ------------------------------------------------------------
    # 🎨 CSS personalizado + carga de imágenes para banners
    # ------------------------------------------------------------
    banner_image_path = "img/verde2.png"
    banner_inferior_image_path = "img/verde.png"
    img_col1_image_path = "img/baner_l.png"

    banner_base64 = img_to_base64(banner_image_path)
    banner_inferior_base64 = img_to_base64(banner_inferior_image_path)
    img_col1_base64 = img_to_base64(img_col1_image_path)

    st.markdown(
        f"""
    <style>
        /* ----------- HEADER ----------- */
        [data-testid="stHeader"] {{
            background: linear-gradient(90deg, #88C999, #A8E55A) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        [data-testid="stHeader"] * {{
            color: #1C3B2F !important;
        }}

        /* ----------- FONDO DE APP ----------- */
        [data-testid="stAppViewContainer"], body {{
            background-color: #E6FFF7 !important;
            font-family: 'Arial', sans-serif;
        }}
        /* ----------- BOTON Deply ----------- */
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
        /* ----------- BANNER SUPERIOR ----------- */
        .banner {{
            position: relative;
            width: 100%;
            height: 250px;
            background-image: url("data:image/jpg;base64,{banner_base64}");
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
        /* ----------- BANNER SUPERIOR ----------- */
        .banner-inferior {{
            position: relative;
            width: 100%;
            height: 200px;
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
        /* ----------- MÉTRICAS PERSONALIZADAS ----------- */
        .metric-card {{
            background: linear-gradient(135deg, #E4F7EC, #C2E8D0);
            padding: 18px 22px;
            border-radius: 14px;
            border: 1px solid #A5D6BE;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.25s ease;
            margin-bottom: 12px;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        .metric-icon {{
            font-size: 2.4rem;
            color: #1C7C54;
            flex-shrink: 0;
        }}
        .metric-content {{
            display: flex;
            flex-direction: column;
        }}
        .metric-label {{
            font-size: 0.95rem;
            color: #2E4F3D;
            font-weight: 600;
        }}
        .metric-value {{
            font-size: 1.8rem;
            color: #125C3B;
            font-weight: bold;
            margin-top: -4px;
        }}

    </style>
    """,
        unsafe_allow_html=True
    )
    
    
def render_sitemap() -> None:
    """Presenta una guía visual rápida de la aplicación."""

    st.title("Mapa del sitio")
    st.markdown(
        """
        Conoce la estructura general del dashboard para navegar con facilidad.  
        Cada sección está pensada para que encuentres la información clave sobre la estrategia **Basura Cero**.
        """
    )

    st.markdown("---")
    st.subheader("Secciones principales")
    st.markdown(
        """
        - **Inicio:** Panorama general, métricas clave y visualizaciones de los negocios verdes.  
        - **Mapa del sitio:** Esta guía rápida con accesos y descripción de cada módulo.  
        - **Preguntas frecuentes:** Respuestas a dudas comunes sobre el proyecto y los datos.  
        - **Descargas:** En la sección de Inicio puedes descargar la base de datos normalizada.  
        """
    )

    st.subheader("Próximas incorporaciones")
    st.markdown(
        """
    - Paneles interactivos por región.  
    - Seguimiento a indicadores de aprovechamiento y economía circular.  
    - Integración con historias de éxito de emprendimientos verdes.  
    """
    )

    st.info(
        "Sugerencia: Usa el menú lateral para moverte entre secciones o desplegar la base de datos completa"
    )


def render_faq() -> None:
    """Muestra un listado de preguntas frecuentes con respuestas."""

    st.title("Preguntas frecuentes")
    st.markdown(
        """
    Aquí encontrarás respuestas rápidas sobre el origen de la información, cómo se procesan los datos
    y cómo puedes aprovechar el tablero en tus proyectos.
    """
    )

    faq_items = [
        (
            "¿De dónde provienen los datos?",
            "Los datos se descargan de fuentes oficiales como la Superintendencia de Servicios Públicos "
            "Domiciliarios y MinVivienda, además del listado nacional de Negocios Verdes disponible "
            "en datos abiertos.",
        ),
        (
            "¿Cada cuánto se actualiza la información?",
            "Puedes reemplazar el enlace del CSV por la versión más reciente publicada en GitHub u otra fuente. "
            "La función de carga está cacheada para optimizar el rendimiento.",
        ),
        (
            "¿Cómo se realizó la limpieza de los datos?",
            "Se estandarizaron nombres de columnas, se normalizaron productos y sectores, y se completaron "
            "las regiones basadas en la autoridad ambiental correspondiente.",
        ),
        (
            "¿Puedo descargar la base de datos filtrada?",
            "Sí. En la sección de Inicio encontrarás un botón para descargar el CSV con la versión normalizada "
            "del dataset.",
        ),
        (
            "¿Qué puedo hacer si falta una imagen del banner?",
            "La aplicación mostrará una advertencia y utilizará un marcador de posición, por lo que puedes "
            "subir tus propias imágenes a la carpeta `img/` para personalizarlo.",
        ),
    ]

    for question, answer in faq_items:
        with st.expander(question):
            st.write(answer)

    st.success("¿Tienes otra pregunta? ¡Añádela en el repositorio o compártela con el equipo!")


# ============================================================
# Ejecutar aplicación
# ============================================================

if __name__ == "__main__":
    main()
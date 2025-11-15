"""Aplicación Streamlit para explorar negocios verdes en Colombia."""
# ============================================================
# Librerias
# ============================================================
from __future__ import annotations

from typing import Callable, Optional
from typing import Optional

import re
import textwrap
import base64

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


# ============================================================
# 1️⃣ Cargar el dataset
# ============================================================

DATA_URL = (
    "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/"
    "Listado_de_Negocios_Verdes_20251025.csv"
)

# ============================================================
# Limpiar el dataset
# ============================================================

DEPARTMENT_CANONICAL = {
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

def normalizar_region(valor: Optional[str]) -> Optional[str]:
    """Homologa la etiqueta de región, asegurando el uso de PACÍFICA."""

    if pd.isna(valor):
        return pd.NA

    texto = str(valor).strip().upper()
    sin_tildes = texto.translate(str.maketrans("ÁÉÍÓÚ", "AEIOU"))

    if sin_tildes in {"PACIFICO", "PACIFICA"}:
        return "PACÍFICA"

    return texto

def normalizar_departamento(valor: Optional[str]) -> Optional[str]:
    """Devuelve el nombre canónico del departamento si es posible."""

    if pd.isna(valor):
        return pd.NA

    texto = str(valor).strip().upper()
    texto = texto.replace(".", " ").replace(",", " ")
    texto = re.sub(r"\s+", " ", texto)
    sin_tildes = texto.translate(str.maketrans("ÁÉÍÓÚÜ", "AEIOUU"))

    return DEPARTMENT_CANONICAL.get(sin_tildes, texto)

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Devuelve el conjunto de datos limpio cargado desde el archivo CSV remoto."""
    df = pd.read_csv(DATA_URL)

    # Simplifica los nombres de las columnas manteniendo el descriptor antes del salto
    # de línea y los coloca en mayúscula.
    renames: dict[str, str] = {}
    for col in df.columns:
        if "\n" in col:
            new_name = col.split("\n")[0].strip()
            renames[col] = new_name
    df = df.rename(columns=renames)
    df.columns = df.columns.str.upper().str.strip()

    # --- Limpieza de la columna PRODUCTO PRINCIPAL ---
    if "PRODUCTO PRINCIPAL" in df.columns:
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].astype(str).str.upper()
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].str.replace(
            ".", "", regex=False
        )
        df["PRODUCTO PRINCIPAL"] = df["PRODUCTO PRINCIPAL"].replace(
            "MIEL", "MIEL DE ABEJAS"
        )

    # --- Limpiar columna AÑO ---
    if "AÑO" in df.columns:
        df["AÑO"] = df["AÑO"].astype(str).str.replace(",", "", regex=False)
        df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce").astype("Int64")

    # --- Mapeo de autoridades a regiones ---
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
        "EPA BARRANQUILLA VERDE": "CARIBE",
        "EPA BUENAVENTURA": "PACÍFICA",
        "EPA CARTAGENA": "CARIBE",
        "SDA": "ANDINA",
    }

    if "AUTORIDAD AMBIENTAL" in df.columns:
        df["AUTORIDAD AMBIENTAL"] = (
            df["AUTORIDAD AMBIENTAL"].astype("string").str.strip().str.upper()
        )

    if "REGIÓN" in df.columns:
        df["REGIÓN"] = df["REGIÓN"].astype("string").map(normalizar_region)

    def asignar_region(row: pd.Series) -> Optional[str]:
        region = row.get("REGIÓN")
        if pd.isna(region) or str(region).lower() == "no registra":
            autoridad = row.get("AUTORIDAD AMBIENTAL")
            return mapeo_region.get(autoridad, region)
        return region

    df["REGIÓN"] = df.apply(asignar_region, axis=1)
    df["REGIÓN"] = df["REGIÓN"].map(normalizar_region)

    if "DEPARTAMENTO" in df.columns:
        df["DEPARTAMENTO"] = (
            df["DEPARTAMENTO"].astype("string").map(normalizar_departamento)
        )

    # --- Quitar numeraciones tipo "1.1.2." en CATEGORÍA, SECTOR y SUBSECTOR ---
    def limpiar_numeros(texto: str | float | None) -> str | float | None:
        if pd.isna(texto):
            return texto
        return re.sub(r"^\s*[\d\.]+\s*", "", str(texto))

    for col in ["CATEGORÍA", "SECTOR", "SUBSECTOR"]:
        if col in df.columns:
            df[col] = df[col].apply(limpiar_numeros)

    return df

# ============================================================
# Clasificación: Relación con BASURA CERO
# ============================================================

categorias_basura_cero = {
    "Reciclaje/Reutilización": ["recicl", "reutiliz", "reuso", "aprovech"],
    "Compostaje/Biomasa": ["compost", "orgánic", "biomasa", "abono"],
    "Producción limpia": [
        "producción limpia",
        "transformación sostenible",
        "ecodiseño",
        "eficiencia",
    ],
    "Economía circular": ["economía circular", "ciclo cerrado", "remanufactura"],
    "Bioinsumos/Bioproductos": [
        "bioinsumo",
        "biodegrad",
        "biofertiliz",
        "bioproduct",
    ],
    "Energía renovable": [
        "energía solar",
        "energía renovable",
        "biogás",
        "panel solar",
        "fotovoltaic",
    ],
    "Agroecología/Sostenibilidad rural": [
        "agroecolog",
        "agroindustria sostenible",
        "sostenible",
        "ecológica",
    ],
}

def tipo_relacion_basura_cero(fila: pd.Series) -> str:
    texto = f"{fila['DESCRIPCIÓN']} {fila['SECTOR']} {fila['SUBSECTOR']}".lower()
    tipos_detectados: list[str] = []
    for categoria, palabras in categorias_basura_cero.items():
        if any(palabra in texto for palabra in palabras):
            tipos_detectados.append(categoria)
    if tipos_detectados:
        return ", ".join(tipos_detectados)
    return "No aplica"

# ------------------------------------------------------------
# 🌍 Configuración general de la página Streamlit
# ------------------------------------------------------------
def img_to_base64(img_path: str) -> Optional[str]:
    """Convierte una imagen local en una cadena base64 para usar en estilos inline."""

    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        if not st.session_state.get("_banner_warning_shown", False):
            st.warning(
                f"Imagen no encontrada en {img_path}. Se usará un fondo de color."
            )
            st.session_state["_banner_warning_shown"] = True
        return None


def render_header(df: pd.DataFrame) -> None:
    """Mostrar el banner principal, descripción y métricas resumidas."""

    banner_base64 = img_to_base64("img/verde2.png")
    if banner_base64:
        background_css = (
            f'background-image: url("data:image/png;base64,{banner_base64}");'
        )

    st.markdown(
        f"""
        <style>
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

    st.caption(
        "Análisis exploratorio guiado sobre el registro nacional de negocios verdes."
    )

    total_rows = len(df)
    total_columns = df.shape[1]
    departamentos = df["DEPARTAMENTO"].nunique()

    col1, col2, col3 = st.columns(3, gap="large")
    col1.metric("Registros", f"{total_rows:,}",)
    col2.metric("Columnas", total_columns)
    col3.metric("Departamentos", departamentos)
    


@st.cache_data(show_spinner=False)
def resumen_texto(df: pd.DataFrame) -> str:
    """Genera un resumen breve del conjunto de datos filtrado."""
    if df.empty:
        return "**No hay registros que cumplan las condiciones seleccionadas.**"

    top_dep = df["DEPARTAMENTO"].value_counts().idxmax()
    top_sector = df["SECTOR"].value_counts().idxmax()
    year_span = (df["AÑO"].min(), df["AÑO"].max())

    template = textwrap.dedent(
        """
        **Resumen del subconjunto activo**

        * El departamento con más negocios es **{dep}**.
        * El sector predominante es **{sector}**.
        * Los registros abarcan desde **{min_year}** hasta **{max_year}**.
        """
    )
    return template.format(
        dep=top_dep, sector=top_sector, min_year=year_span[0], max_year=year_span[1]
    )


def plot_if_not_empty(func: Callable[[pd.DataFrame], None], df: pd.DataFrame) -> None:
    """Ejecuta una función de graficado solo cuando hay datos disponibles."""
    if df.empty:
        st.info("No hay datos para mostrar con los filtros aplicados.")
        return
    func(df)



def plot_top_departamentos(df: pd.DataFrame) -> None:
    """Muestra un gráfico de barras horizontal con los departamentos líderes."""
    top_departamentos = df["DEPARTAMENTO"].value_counts().head(10).sort_values()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(
        x=top_departamentos.values,
        y=top_departamentos.index,
        palette="crest",
        ax=ax,
    )
    ax.set_title("Top 10 Departamentos por número de negocios")
    ax.set_xlabel("Número de negocios")
    ax.set_ylabel("Departamento")
    st.pyplot(fig)



def plot_categoria_sector(df: pd.DataFrame) -> None:
    """Muestra un gráfico de barras agrupadas por categoría y sector."""
    categoria_sector = (
        df.groupby(["CATEGORÍA", "SECTOR"]).size().reset_index(name="Cantidad")
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=categoria_sector,
        x="Cantidad",
        y="CATEGORÍA",
        hue="SECTOR",
        palette="Set2",
        ax=ax,
    )
    ax.set_title("Distribución de Negocios por Categoría y Sector")
    ax.set_xlabel("Cantidad de negocios")
    ax.set_ylabel("Categoría")
    ax.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)



def plot_heatmap(df: pd.DataFrame) -> None:
    """Muestra un mapa de calor con la relación Región vs. Categoría."""
    matriz = pd.crosstab(df["REGIÓN"], df["CATEGORÍA"])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(matriz, cmap="YlGnBu", linewidths=0.5, annot=True, fmt="d", ax=ax)
    ax.set_title("Relación entre Región y Categoría")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Región")
    st.pyplot(fig)



def plot_tendencia_anual(df: pd.DataFrame) -> None:
    """Muestra el número de negocios por año."""
    conteo = df.groupby("AÑO").size()

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.lineplot(x=conteo.index, y=conteo.values, marker="o", ax=ax, color="#4E7F96")
    ax.set_title("Negocios verdes registrados por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de registros")
    ax.grid(True, linestyle="--", alpha=0.4)
    st.pyplot(fig)



def main() -> None:
    st.set_page_config(
        page_title="Basura Cero | Economía Circular",
        layout="centered",
        page_icon="♻️",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 900px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    df["Tipo_Relacion_Basura_Cero"] = df.apply(tipo_relacion_basura_cero, axis=1)
    df["Relacion_Basura_Cero"] = df["Tipo_Relacion_Basura_Cero"].apply(
        lambda x: "Sí" if x != "No aplica" else "No"
    )

    st.sidebar.header("Filtros")
    regiones = sorted(df["REGIÓN"].unique())
    departamentos = sorted(df["DEPARTAMENTO"].unique())
    categorias = sorted(df["CATEGORÍA"].unique())

    regiones_sel = st.sidebar.multiselect("Región", regiones, default=regiones)
    deptos_sel = st.sidebar.multiselect("Departamento", departamentos)
    categorias_sel = st.sidebar.multiselect("Categoría", categorias)

    df_filtered = df[df["REGIÓN"].isin(regiones_sel)]

    if deptos_sel:
        df_filtered = df_filtered[df_filtered["DEPARTAMENTO"].isin(deptos_sel)]

    if categorias_sel:
        df_filtered = df_filtered[df_filtered["CATEGORÍA"].isin(categorias_sel)]

    render_header(df_filtered)

    st.markdown(resumen_texto(df_filtered))

    with st.expander("Ver datos filtrados"):
        st.dataframe(df_filtered)

    st.subheader("Exploración visual")
    plot_if_not_empty(plot_top_departamentos, df_filtered)
    plot_if_not_empty(plot_categoria_sector, df_filtered)
    plot_if_not_empty(plot_heatmap, df_filtered)
    plot_if_not_empty(plot_tendencia_anual, df_filtered)

    st.caption(
        "Fuente de datos: Listado de Negocios Verdes (Ministerio de Ambiente y Desarrollo Sostenible)."
    )


if __name__ == "__main__":
    main()
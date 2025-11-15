"""Streamlit dashboard for exploring the Negocios Verdes dataset."""
from __future__ import annotations

import textwrap
from typing import Callable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

DATA_URL = (
    "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/"
    "Listado_de_Negocios_Verdes_20251025.csv"
)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Return the cleaned dataset loaded from the remote CSV file."""
    df = pd.read_csv(DATA_URL)

    # Simplify column names by keeping the descriptor before the newline.
    df.columns = [col.split("\n")[0].strip() for col in df.columns]

    # Normalise text fields and clean numeric strings.
    df["AÑO"] = df["AÑO"].str.replace(",", "", regex=False).astype(int)

    text_columns = [
        "AUTORIDAD AMBIENTAL",
        "REGIÓN",
        "DEPARTAMENTO",
        "MUNICIPIO",
        "RAZÓN SOCIAL",
        "Descripción",
        "CATEGORÍA",
        "SECTOR",
        "SUBSECTOR",
        "Producto Principal",
        "CATEGORÍA COMERCIAL",
        "NOMBRE REPRESENTANTE",
    ]

    for column in text_columns:
        df[column] = df[column].fillna("Sin dato").str.strip()

    return df


def render_header(df: pd.DataFrame) -> None:
    """Display the main title and dataset summary metrics."""
    st.title("Explorador de Negocios Verdes en Colombia")
    st.caption(
        "Análisis exploratorio guiado sobre el registro nacional de negocios verdes."
    )

    total_rows = len(df)
    total_columns = df.shape[1]
    departamentos = df["DEPARTAMENTO"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Registros", f"{total_rows:,}")
    col2.metric("Columnas", total_columns)
    col3.metric("Departamentos", departamentos)


@st.cache_data(show_spinner=False)
def resumen_texto(df: pd.DataFrame) -> str:
    """Generate a short textual summary about the filtered dataset."""
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
    """Helper that only executes the plotting function when data is available."""
    if df.empty:
        st.info("No hay datos para mostrar con los filtros aplicados.")
        return
    func(df)


def plot_top_departamentos(df: pd.DataFrame) -> None:
    """Display a horizontal bar chart with the leading departments."""
    top_departamentos = df["DEPARTAMENTO"].value_counts().head(10).sort_values()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top_departamentos.values, y=top_departamentos.index, palette="crest", ax=ax)
    ax.set_title("Top 10 Departamentos por número de negocios")
    ax.set_xlabel("Número de negocios")
    ax.set_ylabel("Departamento")
    st.pyplot(fig)


def plot_categoria_sector(df: pd.DataFrame) -> None:
    """Display a grouped count plot for categoría y sector."""
    categoria_sector = df.groupby(["CATEGORÍA", "SECTOR"]).size().reset_index(name="Cantidad")

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
    """Display a heatmap showing la relación Región vs Categoría."""
    matriz = pd.crosstab(df["REGIÓN"], df["CATEGORÍA"])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(matriz, cmap="YlGnBu", linewidths=0.5, annot=True, fmt="d", ax=ax)
    ax.set_title("Relación entre Región y Categoría")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Región")
    st.pyplot(fig)


def plot_tendencia_anual(df: pd.DataFrame) -> None:
    """Display el número de negocios por año."""
    conteo = df.groupby("AÑO").size()

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.lineplot(x=conteo.index, y=conteo.values, marker="o", ax=ax, color="#4E7F96")
    ax.set_title("Negocios verdes registrados por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de registros")
    ax.grid(True, linestyle="--", alpha=0.4)
    st.pyplot(fig)


if __name__ == "__main__":
    st.set_page_config(page_title="Negocios Verdes", layout="centered")

    df = load_data()

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
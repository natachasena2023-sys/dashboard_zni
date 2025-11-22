# ============================================================
# 📌 data_loader.py — Carga y limpieza del dataset
# ============================================================

import pandas as pd
import streamlit as st
from utils import (
    normalizar_region,
    normalizar_departamento,
    limpiar_numeros,
    tipo_relacion_basura_cero
)
from config import MAPEO_REGION


# ============================================================
# 🔽 URL oficial del dataset (puedes cambiarlo libremente)
# ============================================================

DATA_URL = (
    "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/"
    "Listado_de_Negocios_Verdes_20251025.csv"
)


# ============================================================
# 🔄 Función principal de carga y limpieza
# ============================================================

@st.cache_data(show_spinner=True)
def load_data():
    """Carga y limpia el dataset principal de negocios verdes."""

    df = pd.read_csv(DATA_URL)

    # Normalizar columnas
    df.columns = df.columns.str.upper().str.strip()

    # Limpiar columnas con saltos de línea
    df.rename(columns={col: col.split("\n")[0] for col in df.columns}, inplace=True)

    # Convertir AÑO
    if "AÑO" in df.columns:
        df["AÑO"] = (
            df["AÑO"].astype(str).str.replace(",", "").replace("nan", pd.NA)
        )
        df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce").astype("Int64")

    # Normalizar autoridad ambiental
    if "AUTORIDAD AMBIENTAL" in df.columns:
        df["AUTORIDAD AMBIENTAL"] = (
            df["AUTORIDAD AMBIENTAL"]
            .astype(str)
            .str.strip()
            .str.upper()
            .replace("", "NO REGISTRA")
        )

    # Normalizar REGIÓN
    if "REGIÓN" in df.columns:

        df["REGIÓN"] = df["REGIÓN"].apply(normalizar_region)

        def asignar_region(row):
            region = row["REGIÓN"]
            autoridad = row["AUTORIDAD AMBIENTAL"]

            if pd.isna(region) or str(region).lower() == "no registra":
                return MAPEO_REGION.get(autoridad, region)

            return region

        df["REGIÓN"] = df.apply(asignar_region, axis=1)

    # Normalizar DEPARTAMENTO
    if "DEPARTAMENTO" in df.columns:
        df["DEPARTAMENTO"] = df["DEPARTAMENTO"].apply(normalizar_departamento)

    # Limpiar texto en categorías
    for col in ["CATEGORÍA", "SECTOR", "SUBSECTOR"]:
        if col in df.columns:
            df[col] = df[col].apply(limpiar_numeros)

    # Producto principal estandarizado
    if "PRODUCTO PRINCIPAL" in df.columns:
        df["PRODUCTO PRINCIPAL"] = (
            df["PRODUCTO PRINCIPAL"]
            .astype(str)
            .str.upper()
            .str.replace(".", "", regex=False)
            .replace({"MIEL": "MIEL DE ABEJAS"})
        )

    # Clasificación Basura Cero
    if set(["DESCRIPCIÓN", "SECTOR", "SUBSECTOR"]).issubset(df.columns):
        df["RELACIÓN BASURA CERO"] = df.apply(tipo_relacion_basura_cero, axis=1)

    # Columna SI / NO
    df["BASURA 0"] = df["RELACIÓN BASURA CERO"].apply(
        lambda x: "Sí"
        if pd.notna(x)
        and str(x).strip() != ""
        and str(x).lower() != "no aplica"
        else "No"
    )

    return df

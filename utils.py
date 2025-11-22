# ============================================================
# 📌 utils.py — Funciones auxiliares del proyecto Basura Cero
# ============================================================

import pandas as pd
import re
from config import (
    DEPARTMENT_CANONICAL,
    DEPARTMENT_COORDS,
    categorias_basura_cero
)

# ============================================================
# 🔄 Normalización de región
# ============================================================

def normalizar_region(region: str):
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

# ============================================================
# 🔄 Normalización de departamento
# ============================================================

def normalizar_departamento(valor):
    """Normaliza el nombre de un departamento y devuelve su forma canónica."""
    if pd.isna(valor):
        return pd.NA

    texto = (
        str(valor)
        .strip()
        .upper()
        .replace(".", " ")
        .replace(",", " ")
    )

    texto = re.sub(r"\s+", " ", texto)  # Normaliza espacios

    return DEPARTMENT_CANONICAL.get(texto, texto)

# ============================================================
# 📍 Obtener coordenadas de un departamento
# ============================================================

def coordenadas_departamento(nombre):
    """Obtiene las coordenadas del departamento con base en su nombre canónico."""
    if pd.isna(nombre):
        return None

    clave = DEPARTMENT_CANONICAL.get(str(nombre).strip().upper(), None)

    if clave is None:
        return None

    return DEPARTMENT_COORDS.get(clave)

# ============================================================
# ✂ Limpiar numeración
# ============================================================

def limpiar_numeros(texto):
    """Elimina prefijos numéricos tipo '1.2.3. ' al inicio del texto."""
    if pd.isna(texto):
        return texto

    return re.sub(r"^\s*[\d\.]+\s*", "", str(texto))

# ============================================================
# ♻ Clasificación Basura Cero
# ============================================================

def tipo_relacion_basura_cero(fila):
    """
    Detecta palabras clave en DESCRIPCIÓN, SECTOR y SUBSECTOR para
    asignar categorías asociadas al programa Basura Cero.
    """
    texto = f"{fila['DESCRIPCIÓN']} {fila['SECTOR']} {fila['SUBSECTOR']}".lower()
    tipos = []

    for categoria, palabras in categorias_basura_cero.items():
        if any(p in texto for p in palabras):
            tipos.append(categoria)

    return ", ".join(tipos) if tipos else "No aplica"

# ============================================================
# ✔ Validar si un registro tiene relación con Basura Cero
# ============================================================

def tiene_relacion_basura_cero(valor):
    """Devuelve True si el valor indica relación válida con Basura Cero."""
    if pd.isna(valor):
        return False

    valor = str(valor).strip().lower()

    return valor not in ["", "no aplica", "no disponible"]

# ============================================================
# 🎯 Utilidades varias
# ============================================================

def to_upper(texto):
    """Convierte texto a mayúsculas de forma segura."""
    if pd.isna(texto):
        return texto
    return str(texto).upper().strip()


def safe_strip(valor):
    """Elimina espacios de forma segura."""
    if pd.isna(valor):
        return valor
    return str(valor).strip()

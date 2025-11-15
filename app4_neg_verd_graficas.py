import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

# URL del archivo CSV
url = "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/Listado_de_Negocios_Verdes_20251025.csv"

# Cargar el CSV
df = pd.read_csv(url)

# Crear un diccionario de renombres automáticamente (quita todo después de \n)
renames = {}
for col in df.columns:
    if '\n' in col:
        new_name = col.split('\n')[0].strip()  # Toma solo la parte antes de \n
        renames[col] = new_name

# Aplicar los renombres
df = df.rename(columns=renames)

# Convertir títulos a mayúsculas
df.columns = df.columns.str.upper()

# Convertir a mayúsculas la columna PRODUCTO PRINCIPAL
df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].str.upper()

# Luego, elimina todos los puntos '.' que aparezcan en los nombres de productos
df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].str.replace('.', '', regex=False)

# Reemplazar 'MIEL' por 'MIEL DE ABEJAS'
df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].replace("MIEL", "MIEL DE ABEJAS")

# Limpiar la columna 'AÑO' (quitar comas)
if 'AÑO' in df.columns:
    df['AÑO'] = df['AÑO'].astype(str).str.replace(',', '', regex=False)
    df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').astype('Int64')

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

# Guardar resultado limpio a archivo CSV
df.to_csv('negocios_verdes_compacto.csv', index=False)

# Mostrar una tabla con el resultado de la limpieza (primeras 10 filas del DataFrame limpio)
print("Tabla con el resultado de la limpieza de la base de datos (primeras 10 filas):")
print(df.head(10))

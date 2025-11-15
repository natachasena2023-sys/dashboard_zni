# ============================================================
# 🧩 ANÁLISIS DE NEGOCIOS VERDES Y SU RELACIÓN CON BASURA CERO
# ============================================================

# === Librerías ===
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

# ============================================================
# 1️⃣ Cargar y limpiar el dataset
# ============================================================

url = "https://github.com/natachasena2023-sys/bootcam_analisis/raw/refs/heads/main/Listado_de_Negocios_Verdes_20251025.csv"

df = pd.read_csv(url)

# --- Renombrar columnas eliminando saltos de línea ---
renames = {}
for col in df.columns:
    if '\n' in col:
        new_name = col.split('\n')[0].strip()
        renames[col] = new_name
df = df.rename(columns=renames)

# --- Estandarizar nombres de columnas ---
df.columns = df.columns.str.upper().str.strip()

# --- Limpieza de la columna PRODUCTO PRINCIPAL ---
if 'PRODUCTO PRINCIPAL' in df.columns:
    df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].astype(str).str.upper()
    df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].str.replace('.', '', regex=False)
    df['PRODUCTO PRINCIPAL'] = df['PRODUCTO PRINCIPAL'].replace("MIEL", "MIEL DE ABEJAS")

# --- Limpiar columna AÑO ---
if 'AÑO' in df.columns:
    df['AÑO'] = df['AÑO'].astype(str).str.replace(',', '', regex=False)
    df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').astype('Int64')

# --- Mapeo de autoridades a regiones ---
mapeo_region = {
    "AMVA": "ANDINA", "CAM": "ANDINA", "CAR": "ANDINA", "CARDER": "ANDINA",
    "CARDIQUE": "CARIBE", "CARSUCRE": "CARIBE", "CAS": "ANDINA", "CDA": "AMAZONÍA",
    "CDMB": "ANDINA", "CODECHOCÓ": "PACÍFICA", "CORALINA": "INSULAR", 
    "CORANTIOQUIA": "ANDINA", "CORMACARENA": "ORINOQUÍA", "CORNARE": "ANDINA",
    "CORPAMAG": "CARIBE", "CORPOAMAZONÍA": "AMAZONÍA", "CORPOBOYACÁ": "ANDINA",
    "CORPOCALDAS": "ANDINA", "CORPOCESAR": "CARIBE", "CORPOCHIVOR": "ANDINA",
    "CORPOGUAJIRA": "CARIBE", "CORPOGUAVIO": "ANDINA", "CORPOMOJANA": "CARIBE",
    "CORPONARIÑO": "PACÍFICA", "CORPONOR": "CARIBE", "CORPORINOQUÍA": "ORINOQUÍA",
    "CORPOURABÁ": "PACÍFICA", "CORTOLIMA": "ANDINA", "CRA": "CARIBE", 
    "CRC": "PACÍFICA", "CRQ": "ANDINA", "CSB": "CARIBE", "CVC": "PACÍFICA",
    "CVS": "CARIBE", "DADSA": "ANDINA", "DAGMA": "ANDINA", 
    "EPA Barranquilla Verde": "CARIBE", "EPA Buenaventura": "PACÍFICA",
    "EPA Cartagena": "CARIBE", "SDA": "ANDINA"
}

df['AUTORIDAD AMBIENTAL'] = df['AUTORIDAD AMBIENTAL'].astype(str).str.strip()
df['REGIÓN'] = df['REGIÓN'].astype(str).str.strip()

def asignar_region(row):
    if pd.isna(row['REGIÓN']) or row['REGIÓN'].lower() == "no registra":
        return mapeo_region.get(row['AUTORIDAD AMBIENTAL'], row['REGIÓN'])
    else:
        return row['REGIÓN']

df['REGIÓN'] = df.apply(asignar_region, axis=1)

# --- Quitar numeraciones tipo "1.1.2." en CATEGORÍA, SECTOR y SUBSECTOR ---
def limpiar_numeros(texto):
    if pd.isna(texto):
        return texto
    return re.sub(r'^\s*[\d\.]+\s*', '', texto)

for col in ['CATEGORÍA', 'SECTOR', 'SUBSECTOR']:
    if col in df.columns:
        df[col] = df[col].apply(limpiar_numeros)

# ============================================================
# 2️⃣ Clasificación: Relación con BASURA CERO
# ============================================================

categorias_basura_cero = {
    'Reciclaje/Reutilización': ['recicl', 'reutiliz', 'reuso', 'aprovech'],
    'Compostaje/Biomasa': ['compost', 'orgánic', 'biomasa', 'abono'],
    'Producción limpia': ['producción limpia', 'transformación sostenible', 'ecodiseño', 'eficiencia'],
    'Economía circular': ['economía circular', 'ciclo cerrado', 'remanufactura'],
    'Bioinsumos/Bioproductos': ['bioinsumo', 'biodegrad', 'biofertiliz', 'bioproduct'],
    'Energía renovable': ['energía solar', 'energía renovable', 'biogás', 'panel solar', 'fotovoltaic'],
    'Agroecología/Sostenibilidad rural': ['agroecolog', 'agroindustria sostenible', 'sostenible', 'ecológica']
}

def tipo_relacion_basura_cero(fila):
    texto = f"{fila['DESCRIPCIÓN']} {fila['SECTOR']} {fila['SUBSECTOR']}".lower()
    tipos_detectados = []
    for categoria, palabras in categorias_basura_cero.items():
        if any(palabra in texto for palabra in palabras):
            tipos_detectados.append(categoria)
    if tipos_detectados:
        return ', '.join(tipos_detectados)
    else:
        return 'No aplica'

df['Tipo_Relacion_Basura_Cero'] = df.apply(tipo_relacion_basura_cero, axis=1)
df['Relacion_Basura_Cero'] = df['Tipo_Relacion_Basura_Cero'].apply(lambda x: 'Sí' if x != 'No aplica' else 'No')

# ============================================================
# 3️⃣ Mostrar una vista previa
# ============================================================

print("Vista previa del dataset clasificado:")
print(df[['RAZÓN SOCIAL', 'DESCRIPCIÓN', 'Tipo_Relacion_Basura_Cero', 'Relacion_Basura_Cero']].head(10))

# ============================================================
# 4️⃣ Visualizaciones
# ============================================================

# --- Gráfica 2 (versión mejorada con valores visibles) ---
plt.figure(figsize=(10, 6))

# Calcular el top 10
top10_tipos = (
    df['Tipo_Relacion_Basura_Cero']
    .value_counts()
    .head(10)
    .sort_values(ascending=True)
)

# Crear gráfico
ax = top10_tipos.plot(
    kind='barh',
    color='#16a085'
)

# Título y etiquetas
plt.title('Top 10 tipos de contribución a la estrategia Basura Cero', fontsize=13, pad=15)
plt.xlabel('Número de proyectos', fontsize=11)
plt.ylabel('Tipo de relación', fontsize=11)

# Agregar etiquetas al final de cada barra
for container in ax.containers:
    ax.bar_label(container, fmt='%d', padding=4, fontsize=10, color="#0B5345")

# Cuadrícula y diseño
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# --- Gráfica 3: Basura Cero por Región ---
tabla_region = df.groupby(['REGIÓN', 'Relacion_Basura_Cero']).size().unstack(fill_value=0)

tabla_region.plot(kind='bar', stacked=True, figsize=(10,6), color=['#27ae60', '#c0392b'])
plt.title('Negocios Verdes relacionados con Basura Cero por Región')
plt.ylabel('Número de proyectos')
plt.xlabel('Región')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ============================================================
# 5️⃣ Guardar el resultado limpio
# ============================================================
df.to_csv("negocios_verdes_clasificados.csv", index=False)
print("✅ Archivo limpio y clasificado guardado como 'negocios_verdes_clasificados.csv'")
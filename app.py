import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Staffaggio Luglio 2025", layout="wide")
st.title("📅 Pianificazione Staffaggio - Luglio 2025")

@st.cache_data
def load_data():
    return pd.read_excel("Staffaggio Luglio 2025.xlsx")

df = load_data()
df.dropna(axis=1, how='all', inplace=True)

# Giorni della settimana riconosciuti
giorni_settimana = ["LUNEDÌ", "MARTEDÌ", "MERCOLEDÌ", "GIOVEDÌ", "VENERDÌ", "SABATO", "DOMENICA"]
giorni_presenti = [g for g in giorni_settimana if g in df.columns]

col1, col2 = st.columns(2)

# Filtro giorno
with col1:
    giorno_scelto = st.selectbox("📅 Seleziona giorno della settimana", giorni_presenti)

# Filtro agenzia
with col2:
    agenzie = sorted(df["AGENZIA"].dropna().unique())
    agenzia_scelta = st.selectbox("🏢 Seleziona Agenzia", ["Tutte le agenzie"] + agenzie)

# Filtro righe con presenza di BA
df_giorno = df[df[giorno_scelto].notna() & (df[giorno_scelto] != 0)]

if agenzia_scelta != "Tutte le agenzie":
    df_giorno = df_giorno[df_giorno["AGENZIA"] == agenzia_scelta]

st.write(f"### 📍 {len(df_giorno)} punti vendita con presenza BA il {giorno_scelto}")

# Stampa l’elenco formattato
for _, row in df_giorno.iterrows():
    corner = str(row["CORNER"]).strip()
    agenzia = row["AGENZIA"]
    orario = row[giorno_scelto]
    indirizzo = str(row["INDIRIZZO"]).strip()
    link_mappa = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(indirizzo)}"

    st.markdown(f"""
    **[{corner}]({link_mappa})** _(Agenzia: {agenzia})_  
    🕒 **Orario:** {orario}
    ---
    """)

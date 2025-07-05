import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Staffaggio Luglio 2025", layout="wide")
st.title("📊 Pianificazione Staffaggio - Luglio 2025")

uploaded_file = st.file_uploader("Carica il file Excel o CSV unificato", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File caricato correttamente!")

    df.dropna(axis=1, how='all', inplace=True)

    st.sidebar.header("🔎 Filtri")
    fonte = st.sidebar.multiselect("Seleziona Agenzia (FONTE)", sorted(df["FONTE"].dropna().unique()))
    regione = st.sidebar.multiselect("Seleziona Regione", sorted(df["REGIONE"].dropna().unique()) if "REGIONE" in df else [])
    area_manager = st.sidebar.multiselect("Seleziona Area Manager", sorted(df["AREA MANAGER"].dropna().unique()) if "AREA MANAGER" in df else [])
    corner = st.sidebar.text_input("Filtra per nome punto vendita (CORNER contiene)")

    df_filtrato = df.copy()
    if fonte:
        df_filtrato = df_filtrato[df_filtrato["FONTE"].isin(fonte)]
    if regione and "REGIONE" in df_filtrato:
        df_filtrato = df_filtrato[df_filtrato["REGIONE"].isin(regione)]
    if area_manager and "AREA MANAGER" in df_filtrato:
        df_filtrato = df_filtrato[df_filtrato["AREA MANAGER"].isin(area_manager)]
    if corner:
        col_match = [col for col in df_filtrato.columns if "corner" in col.lower()]
        if col_match:
            df_filtrato = df_filtrato[df_filtrato[col_match[0]].str.contains(corner, case=False, na=False)]

    st.write(f"### 📍 {len(df_filtrato)} risultati trovati")
    st.dataframe(df_filtrato, use_container_width=True)

    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_data = convert_df_to_csv(df_filtrato)
    st.download_button(
        label="⬇️ Scarica CSV filtrato",
        data=csv_data,
        file_name="staffaggio_filtrato.csv",
        mime="text/csv"
    )
else:
    st.info("📂 Carica un file per iniziare.")

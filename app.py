import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# Konfigurasi Google Sheets
# ==========================

sheet_id = "13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

# Mapping Bulan -> Nama Sheet
bulan_sheet = {
    "Januari": "JAN",
    "Februari": "FEB",
    "Maret": "MAR",
    "April": "APRIL",
    "Mei": "MEI",
    "Juni": "JUNI",
    "Juli": "JULI",
    "Agustus": "AGS",
    "September": "SEP",
    "Oktober": "OKT",
    "November": "NOV",
    "Desember": "DES"
}

# ==========================
# Tampilan Dashboard
# ==========================

st.set_page_config(
    page_title="Dashboard PERKIN 2026",
    layout="wide"
)

st.title("📊 Dashboard PERKIN 2026")

# ==========================
# Pilih Bulan
# ==========================

bulan = st.selectbox(
    "Pilih Bulan",
    list(bulan_sheet.keys())
)

nama_sheet = bulan_sheet[bulan]

# ==========================
# Baca Data dari Sheet Terpilih
# ==========================

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nama_sheet}"

df = pd.read_csv(url)

# Bersihkan nama kolom
df.columns = df.columns.str.strip()

# Bersihkan isi data
df["Indikator"] = df["Indikator"].astype(str).str.strip()
df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()

# Pastikan numerik
df["Target"] = pd.to_numeric(df["Target"], errors="coerce")
df["Realisasi"] = pd.to_numeric(df["Realisasi"], errors="coerce")

# ==========================
# Pilih Indikator
# ==========================

indikator = st.selectbox(
    "Pilih Indikator",
    sorted(df["Indikator"].dropna().unique())
)

df_filter = df[
    df["Indikator"] == indikator
].copy()

# ==========================
# Hitung Capaian
# ==========================

df_filter["Capaian"] = (
    df_filter["Realisasi"] /
    df_filter["Target"] * 100
).fillna(0).round(2)

# ==========================
# Ubah ke Format Panjang
# ==========================

df_long = pd.melt(
    df_filter,
    id_vars=["Kabupaten"],
    value_vars=["Target", "Realisasi", "Capaian"],
    var_name="Kategori",
    value_name="Nilai"
)

# ==========================
# Diagram Batang
# ==========================

fig = px.bar(
    df_long,
    x="Kabupaten",
    y="Nilai",
    color="Kategori",
    barmode="group",
    text="Nilai",
    title=f"{indikator} - {bulan}"
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Kabupaten/Kota",
    yaxis_title="Nilai",
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

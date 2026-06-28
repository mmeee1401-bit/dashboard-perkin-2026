import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# Konfigurasi Halaman
# ==========================================

st.set_page_config(
    page_title="Dashboard PERKIN 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

.main{
    background-color:#F4F7FC;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

[data-testid="stSidebar"]{
    background:#005BAC;
}

[data-testid="stSidebar"] *{
    color:white;
}

.title-card{
    background:linear-gradient(90deg,#005BAC,#0099E5);
    padding:20px;
    border-radius:18px;
    color:white;
    box-shadow:0px 6px 18px rgba(0,0,0,0.2);
    margin-bottom:20px;
}

.metric-card{
    background:white;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
    text-align:center;
}

.graph-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 3px 12px rgba(0,0,0,0.1);
    margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# Google Sheets
# ==========================================

sheet_id = "13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

bulan_sheet = {
    "Januari":"JAN",
    "Februari":"FEB",
    "Maret":"MAR",
    "April":"APRIL",
    "Mei":"MEI",
    "Juni":"JUNI",
    "Juli":"JULI",
    "Agustus":"AGS",
    "September":"SEP",
    "Oktober":"OKT",
    "November":"NOV",
    "Desember":"DES"
}

# ==========================================
# Sidebar
# ==========================================

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/8/89/Logo_BKKBN.png",
    width=170
)

st.sidebar.title("Dashboard PERKIN")

bulan = st.sidebar.selectbox(
    "📅 Pilih Bulan",
    list(bulan_sheet.keys())
)

nama_sheet = bulan_sheet[bulan]

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nama_sheet}"

df = pd.read_csv(url)

df.columns = df.columns.str.strip()

df["Indikator"] = df["Indikator"].astype(str).str.strip()
df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()

df["Target"] = pd.to_numeric(df["Target"], errors="coerce")
df["Realisasi"] = pd.to_numeric(df["Realisasi"], errors="coerce")

indikator = st.sidebar.selectbox(
    "📌 Pilih Indikator",
    sorted(df["Indikator"].unique())
)

df_filter = df[df["Indikator"]==indikator].copy()

df_filter["Capaian"] = (
    df_filter["Realisasi"] /
    df_filter["Target"] *100
).fillna(0).round(2)

# ==========================================
# Header
# ==========================================

st.markdown(f"""
<div class="title-card">

<h1>📊 Dashboard PERKIN 2026</h1>

<h4>Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN</h4>

<b>Bulan :</b> {bulan}

</div>
""", unsafe_allow_html=True)

# ==========================================
# KPI CARD
# ==========================================

total_target = df_filter["Target"].sum()
total_realisasi = df_filter["Realisasi"].sum()

if total_target > 0:
    persen = round((total_realisasi / total_target) * 100, 2)
else:
    persen = 0

jumlah_kab = df_filter["Kabupaten"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
    <h5>🎯 Total Target</h5>
    """, unsafe_allow_html=True)

    st.metric(
        label="",
        value=f"{total_target:,.0f}"
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
    <h5>✅ Total Realisasi</h5>
    """, unsafe_allow_html=True)

    st.metric(
        label="",
        value=f"{total_realisasi:,.0f}"
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
    <h5>📈 Persentase Capaian</h5>
    """, unsafe_allow_html=True)

    st.metric(
        label="",
        value=f"{persen:.2f}%"
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
    <h5>🏛 Kabupaten/Kota</h5>
    """, unsafe_allow_html=True)

    st.metric(
        label="",
        value=jumlah_kab
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# GRAFIK 1
# ==========================================

st.markdown(
    "<div class='graph-card'>",
    unsafe_allow_html=True
)

st.subheader("📊 Target vs Realisasi")

df_bar = pd.melt(
    df_filter,
    id_vars=["Kabupaten"],
    value_vars=["Target", "Realisasi"],
    var_name="Kategori",
    value_name="Nilai"
)

fig1 = px.bar(
    df_bar,
    x="Kabupaten",
    y="Nilai",
    color="Kategori",
    barmode="group",
    text="Nilai",
    color_discrete_map={
        "Target":"#1E88E5",
        "Realisasi":"#43A047"
    }
)

fig1.update_traces(
    textposition="outside"
)

fig1.update_layout(
    height=520,
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend_title="",
    xaxis_title="Kabupaten/Kota",
    yaxis_title="Jumlah",
    title=None
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
# ==========================================
# GRAFIK 2 - PERSENTASE CAPAIAN
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<div class='graph-card'>",
    unsafe_allow_html=True
)

st.subheader("📈 Persentase Capaian (%)")

fig2 = px.bar(
    df_filter.sort_values("Capaian", ascending=False),
    x="Kabupaten",
    y="Capaian",
    text="Capaian",
    color="Capaian",
    color_continuous_scale="Blues"
)

fig2.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig2.update_layout(
    height=500,
    plot_bgcolor="white",
    paper_bgcolor="white",
    coloraxis_showscale=False,
    xaxis_title="Kabupaten/Kota",
    yaxis_title="Persentase (%)",
    yaxis_range=[0,110]
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

# ==========================================
# RANKING KABUPATEN
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🏆 Ranking Kabupaten/Kota")

ranking = df_filter.sort_values(
    "Capaian",
    ascending=False
)[["Kabupaten","Target","Realisasi","Capaian"]]

ranking.index = range(1, len(ranking)+1)

st.dataframe(
    ranking,
    use_container_width=True
)

# ==========================================
# DATA DETAIL
# ==========================================

with st.expander("📋 Lihat Data Detail"):

    st.dataframe(
        df_filter,
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
"""
<hr>

<div style='text-align:center;
font-size:15px;
color:gray;'>

<b>Dashboard PERKIN 2026</b><br>

Kementerian Kependudukan dan Pembangunan Keluarga /
BKKBN Provinsi Kepulauan Bangka Belitung

<br><br>

Dibangun menggunakan
❤️ Streamlit | Plotly | Google Sheets

</div>

""",
unsafe_allow_html=True
)

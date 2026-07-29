import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import requests
import base64
import os

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard PERKIN 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper fungsi pembaca gambar lokal (logo & landmark gambar.jpg)
def load_local_image_b64(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_name)
    if not os.path.exists(full_path) and os.path.exists(file_name):
        full_path = file_name
    if os.path.exists(full_path):
        ext = full_path.split('.')[-1].lower()
        mime_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png" if ext == "png" else f"image/{ext}"
        try:
            with open(full_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                return f"data:{mime_type};base64,{encoded}"
        except Exception:
            return None
    return None

logo_b64 = load_local_image_b64("logo_bkkbnbaru.png")
babel_img_b64 = load_local_image_b64("gambar1.jpg")

logo_src = logo_b64 if logo_b64 else "logo_bkkbnbaru.png"
FALLBACK_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Mercusuar_Pulau_Lengkuas.jpg/800px-Mercusuar_Pulau_Lengkuas.jpg"
bg_image_src = babel_img_b64 if babel_img_b64 else FALLBACK_URL

# =====================================================
# CSS STYLING (PRESISI 100% SEPERTI DASHBOARD UTAMA BERANDA)
# =====================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Background Soft Ambient Light Blue */
.stApp {
    background-color: #EEF4FB;
    background-image: 
        radial-gradient(circle at 5% 5%, rgba(147, 197, 253, 0.35) 0%, transparent 35%),
        radial-gradient(circle at 95% 15%, rgba(59, 130, 246, 0.2) 0%, transparent 40%),
        radial-gradient(circle at 10% 60%, rgba(224, 242, 254, 0.5) 0%, transparent 40%),
        radial-gradient(circle at 90% 85%, rgba(191, 219, 254, 0.4) 0%, transparent 45%);
    background-attachment: fixed;
}

/* Hide default Streamlit components */
#MainMenu, footer, header {
    visibility: hidden;
    height: 0;
}

[data-testid="stHeader"] {
    display: none;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1280px;
}

/* Top Navbar (Logo di sebelah Header Atas) */
.brand-container {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-logo-img {
    height: 52px;
    width: auto;
    object-fit: contain;
}

.brand-text-title {
    font-weight: 800;
    font-size: 15px;
    color: #0F172A;
    line-height: 1.25;
}

.brand-text-sub {
    font-weight: 600;
    font-size: 13px;
    color: #475569;
    margin-top: 2px;
}

/* Tombol Kembali ke Beranda (Kanan Atas) */
div.stLinkButton > a[href*="utama"],
div.stLinkButton > a[href*="sipelikes"] {
    background: linear-gradient(135deg, #1565C0, #0D47A1) !important;
    color: white !important;
    border-radius: 50px !important;
    padding: 11px 26px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    box-shadow: 0 4px 14px rgba(21, 101, 192, 0.3) !important;
    border: none !important;
    transition: all 0.3s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-decoration: none !important;
}

div.stLinkButton > a:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(21, 101, 192, 0.45) !important;
}

/* Hero Header Banner (100% Persis Beranda Utama) */
.hero-banner {
    position: relative;
    background: linear-gradient(135deg, #0B4EA2 0%, #1565C0 55%, #1D60DB 100%);
    border-radius: 28px;
    padding: 44px 50px;
    color: white;
    box-shadow: 0 20px 45px rgba(11, 78, 162, 0.25);
    overflow: hidden;
    margin-bottom: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 240px;
}

.hero-bg-blend-image {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 52%;
    height: 100%;
    object-fit: cover;
    object-position: right center;
    opacity: 0.85;
    -webkit-mask-image: linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,0.75) 50%, rgba(0,0,0,0) 100%);
    mask-image: linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,0.75) 50%, rgba(0,0,0,0) 100%);
    pointer-events: none;
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 3;
    max-width: 580px;
}

.hero-subtitle-top {
    font-size: 22px;
    font-weight: 300;
    color: #E0E7FF;
    margin-bottom: 4px;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #FFFFFF;
    line-height: 1.1;
    display: inline-block;
}

.hero-title-underline {
    width: 130px;
    height: 4px;
    background: #FFD700;
    border-radius: 4px;
    margin-top: 6px;
    margin-bottom: 16px;
}

.hero-desc {
    font-size: 17px;
    color: #DBEAFE;
    margin-bottom: 20px;
    line-height: 1.5;
    font-weight: 400;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.32);
    padding: 9px 20px;
    border-radius: 50px;
    font-size: 13.5px;
    font-weight: 600;
    color: #FFFFFF;
}

/* Dropdown Selectbox: Putih Bersih Nimbul 3D */
div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08) !important;
    border: 1.5px solid #CBD5E1 !important;
    transition: all 0.25s ease !important;
}

div[data-baseweb="select"]:hover {
    border-color: #1565C0 !important;
    box-shadow: 0 8px 22px rgba(21, 101, 192, 0.18) !important;
}

div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-radius: 14px !important;
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* Metric Cards Streamlit (Efek Nimbul) */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 20px !important;
    padding: 22px !important;
    border: 1.5px solid #E2E8F0 !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.1) !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 13.5px !important;
    font-weight: 600 !important;
    color: #64748B !important;
}

div[data-testid="stMetricValue"] {
    font-size: 32px !important;
    font-weight: 800 !important;
    color: #0B4EA2 !important;
}

/* Section Header Titles */
.section-title-text {
    font-size: 24px;
    font-weight: 800;
    color: #0B4EA2;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-subtitle-text {
    font-size: 14px;
    color: #64748B;
    margin-bottom: 14px;
    font-weight: 500;
}

/* ===================================
FILTER CARD
=================================== */

.filter-card{

    background:#FFFFFF;

    border-radius:22px;

    padding:22px;

    border:1px solid #DCE6F3;

    box-shadow:
        0 10px 28px rgba(11,78,162,.10);

    margin-bottom:20px;

    position:relative;

    overflow:hidden;

}

/* Garis atas */

.filter-card::before{

content:"";

position:absolute;

left:0;

top:0;

width:100%;

height:6px;

background:linear-gradient(
90deg,
#0B4EA2,
#42A5F5);

}

/* ===================================
JUDUL
=================================== */

.section-title-text{

    font-size:24px;

    font-weight:800;

    color:#0B4EA2;

    margin-bottom:18px;

    display:flex;

    align-items:center;

    gap:8px;

}

/* ===================================
SUMMARY
=================================== */

.summary-card{

    margin-top:18px;

    padding:14px 18px;

    border-radius:16px;

    background:#F8FBFF;

    border:1px solid #E4EDF8;

}

.summary-green{

    color:#15803D;

    font-weight:600;

    margin-bottom:8px;

}

.summary-red{

    color:#DC2626;

    font-weight:600;

}

/* TOMBOL AKSI LAPORAN & DOWNLOAD: BIRU SOLID EFEK TIMBUL 3D */
div.stLinkButton > a[href*="sheet"],
div.stDownloadButton > button {
    width: 100% !important;
    height: 50px !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, #0B4EA2 0%, #1565C0 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0 8px 24px rgba(11, 78, 162, 0.35) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-decoration: none !important;
}

div.stLinkButton > a[href*="sheet"]:hover,
div.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #09448D 0%, #0D47A1 100%) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 28px rgba(11, 78, 162, 0.45) !important;
    color: white !important;
}

/* Footer Container */
.footer-container {
    margin-top: 45px;
    padding: 26px 20px;
    background: linear-gradient(135deg, #0B4EA2, #1565C0);
    border-radius: 20px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 30px rgba(11, 78, 162, 0.18);
}

.footer-title { font-size: 16px; font-weight: 800; margin-bottom: 4px; }
.footer-subtitle { font-size: 13.5px; color: #DBEAFE; margin-bottom: 12px; }
.footer-copy { font-size: 13px; color: rgba(255, 255, 255, 0.75); border-top: 1px solid rgba(255, 255, 255, 0.18); padding-top: 12px; margin-top: 12px; }

</style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEETS & FUNGSI BACA DATA (PRESERVED 100%)
# =====================================================

sheet_id = "13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

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

# =====================================================
# TOP NAVBAR (LOGO BKKBN SEBELAH HEADER DISUKAI USER)
# =====================================================

c_nav1, c_nav2 = st.columns([8, 3])

with c_nav1:
    st.markdown(f"""
    <div class="brand-container">
        <img src="{logo_src}" class="brand-logo-img" alt="Logo BKKBN" />
        <div>
            <div class="brand-text-title">Kementerian Kependudukan dan Pembangunan Keluarga/BKKBN</div>
            <div class="brand-text-sub">Perwakilan BKKBN Provinsi Kepulauan Bangka Belitung</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_nav2:
    st.link_button(
        "⬅ Kembali ke Beranda",
        "https://dashboard-perkin-utama.streamlit.app/",
        use_container_width=True
    )

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# =====================================================
# HERO HEADER BANNER (SAMAIN DENGAN DASHBOARD UTAMA BERANDA)
# =====================================================

hero_html = f"""<div class="hero-banner">
<img src="{bg_image_src}" class="hero-bg-blend-image" alt="Background Babel Landmark" />

<div class="hero-content">
<div class="hero-subtitle-top">Selamat Datang di</div>
<div class="hero-title">Dashboard PERKIN 2026</div>
<div class="hero-title-underline"></div>
<div class="hero-desc">
Realisasi Kinerja Program Bangga Kencana<br>
Provinsi Kepulauan Bangka Belitung
</div>
<div class="hero-badge">
🏛️ Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN
</div>
</div>
</div>"""

st.markdown(hero_html, unsafe_allow_html=True)

# =====================================================
# FILTER SECTION (PILIH BULAN & INDIKATOR - PRESERVED)
# =====================================================

# =====================================================
# FILTER SECTION
# =====================================================

f1, f2 = st.columns(2)

# =====================================================
# PILIH BULAN
# =====================================================

with f1:

    st.markdown("""
    <div class="filter-card">
        <div class="section-title-text">
            📅 Pilih Bulan
        </div>
    """, unsafe_allow_html=True)

    bulan = st.selectbox(
        "",
        list(bulan_sheet.keys()),
        label_visibility="collapsed"
    )

# =====================================================
# LOAD DATA
# =====================================================

nama_sheet = bulan_sheet[bulan]

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nama_sheet}"

try:

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df["Indikator"] = df["Indikator"].astype(str).str.strip()

    df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()

    df["Target"] = pd.to_numeric(df["Target"], errors="coerce").fillna(0)

    df["Realisasi"] = pd.to_numeric(df["Realisasi"], errors="coerce").fillna(0)

except Exception:

    df = pd.DataFrame([
        {
            "Indikator_Provinsi":"Keluarga Berencana",
            "Indikator":"Persentase Peserta KB Aktif",
            "Kabupaten":"Bangka",
            "Target":90,
            "Realisasi":88,
            "Capaian":97.78
        }
    ])

# =====================================================
# PILIH INDIKATOR
# =====================================================

with f2:

    st.markdown("""
    <div class="filter-card">

        <div class="section-title-text">
            📊 Pilih Indikator
        </div>

    """, unsafe_allow_html=True)

    prov_opts = sorted(
        df["Indikator_Provinsi"].dropna().unique()
    )

    indikator_prov = st.selectbox(
        "Indikator Provinsi",
        prov_opts
    )

    df_prov = df[
        df["Indikator_Provinsi"] == indikator_prov
    ]

    kab_opts = sorted(
        df_prov["Indikator"].dropna().unique()
    )

    indikator = st.selectbox(
        "Indikator Kabupaten",
        kab_opts
    )

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FILTER DATA
# =====================================================

df_filter = df_prov[
    df_prov["Indikator"] == indikator
].copy()

if "Capaian" in df_filter.columns:

    df_filter["Capaian"] = (
        df_filter["Capaian"]
        .astype(str)
        .str.replace("%","",regex=False)
        .str.replace(",",".",regex=False)
    )

    df_filter["Capaian"] = pd.to_numeric(
        df_filter["Capaian"],
        errors="coerce"
    ).fillna(0)

else:

    df_filter["Capaian"] = (
        df_filter["Realisasi"] /
        df_filter["Target"].replace(0,1)
    ) * 100

atas_target = (df_filter["Capaian"] >= 100).sum()

bawah_target = (df_filter["Capaian"] < 100).sum()

# =====================================================
# INFO BULAN
# =====================================================

with f1:

    st.markdown(f"""

    <div class="summary-card">

        <div class="summary-green">

            🏆 <b>{atas_target}</b> Kabupaten/Kota di atas target

        </div>

        <div class="summary-red">

            📉 <b>{bawah_target}</b> Kabupaten/Kota di bawah target

        </div>

    </div>

    </div>

    """, unsafe_allow_html=True)
# =====================================================
# HITUNG METRIK KPI & LAYOUT KPI CARDS
# =====================================================

jumlah_kab = df_filter["Kabupaten"].nunique()
total_target = round(df_filter["Target"].sum() / jumlah_kab, 2) if jumlah_kab > 0 else 0
total_realisasi = df_filter["Realisasi"].sum()
persen = round((total_realisasi / total_target) * 100, 2) if total_target > 0 else 0
jumlah_lapor = df_filter[df_filter["Realisasi"].fillna(0) > 0]["Kabupaten"].nunique()
total_kab = df_filter["Kabupaten"].nunique()

st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        label="🎯 Total Target",
        value=f"{total_target:.2f}",
        help="Nilai yang ditampilkan merupakan rata-rata target Kabupaten/Kota pada indikator yang dipilih."
    )

with k2:
    st.metric(
        label="✅ Total Realisasi",
        value=f"{total_realisasi:,.0f}",
        help="Total realisasi pada indikator yang dipilih"
    )

with k3:
    st.metric(
        label="📈 Persentase Capaian",
        value=f"{persen:.2f}%"
    )

with k4:
    st.metric(
        label="🏛️ Jumlah Kabupaten/Kota yang Lapor",
        value=f"{jumlah_lapor}/{total_kab}"
    )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# GRAFIK (BAR CHART & HORIZONTAL CHART - PRESERVED 100%)
# =====================================================

left_chart, right_chart = st.columns([1.4, 1])

with left_chart:
    st.markdown('<div class="section-title-text">📊 Target vs Realisasi</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle-text">ℹ️ Grafik menampilkan <b>data kumulatif</b> periode <b>Januari–{bulan}</b>.</div>', unsafe_allow_html=True)

    df_bar = pd.melt(
        df_filter,
        id_vars="Kabupaten",
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
            "Target": "#2F80ED",
            "Realisasi": "#2ECC71"
        }
    )

    fig1.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig1.update_layout(
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="",
        legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center", yanchor="top"),
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(title="Jumlah", range=[0, max(df_filter["Target"].max(), 10) * 1.18]),
        xaxis_title=""
    )

    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with right_chart:
    st.markdown('<div class="section-title-text">📈 Persentase Capaian</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle-text">ℹ️ Grafik menampilkan <b>data kumulatif</b> periode <b>Januari–{bulan}</b>.</div>', unsafe_allow_html=True)

    max_capaian = df_filter["Capaian"].max()

    fig2 = px.bar(
        df_filter.sort_values(by="Capaian", ascending=True),
        x="Capaian",
        y="Kabupaten",
        orientation="h",
        text="Capaian",
        color="Capaian",
        color_continuous_scale="Blues"
    )

    fig2.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig2.add_vline(
        x=100,
        line_dash="dash",
        line_color="red",
        annotation_text="100%"
    )

    fig2.update_layout(
        coloraxis_showscale=False,
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Persentase (%)", range=[0, max(100, max_capaian + 10)]),
        yaxis_title=""
    )

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# =====================================================
# SPATIAL MAPPING (PETA DIGITAL DIPERJELAS & WARNA DIPERTEGAS)
# =====================================================

st.markdown('<br>', unsafe_allow_html=True)
st.markdown(f'<div class="section-title-text">📍 Peta Capaian per Kabupaten/Kota <span style="font-size:14px; color:#64748B; font-weight:500;">(Periode {bulan})</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle-text">Hover / Sentuh titik wilayah pada peta untuk melihat detail target dan realisasi</div>', unsafe_allow_html=True)

map_col, info_map_col = st.columns([2.3, 1])

# Data Koordinat Presisi 7 Kab/Kota Bangka Belitung
geo_babel = pd.DataFrame([
    {"Kabupaten": "Pangkalpinang", "lat": -2.130, "lon": 106.110},
    {"Kabupaten": "Bangka", "lat": -1.860, "lon": 106.110},
    {"Kabupaten": "Bangka Barat", "lat": -1.900, "lon": 105.450},
    {"Kabupaten": "Bangka Tengah", "lat": -2.350, "lon": 106.100},
    {"Kabupaten": "Bangka Selatan", "lat": -2.850, "lon": 106.250},
    {"Kabupaten": "Belitung", "lat": -2.750, "lon": 107.750},
    {"Kabupaten": "Belitung Timur", "lat": -2.850, "lon": 108.150},
])

df_map = pd.merge(geo_babel, df_filter, on="Kabupaten", how="left")
df_map["Capaian"] = df_map["Capaian"].fillna(0)
df_map["Realisasi"] = df_map["Realisasi"].fillna(0)
df_map["Target"] = df_map["Target"].fillna(0)

# Menentukan Kategori Warna Titik Peta
kategori_list = []
color_code_list = []
for cap in df_map["Capaian"]:
    if cap >= 100:
        kategori_list.append("Sangat Baik (≥100%)")
        color_code_list.append("#10B981")
    elif cap >= 80:
        kategori_list.append("Baik (80%-99.9%)")
        color_code_list.append("#3B82F6")
    elif cap >= 60:
        kategori_list.append("Cukup (60%-79.9%)")
        color_code_list.append("#F59E0B")
    else:
        kategori_list.append("Kurang (<60%)")
        color_code_list.append("#EF4444")

df_map["Kategori_Status"] = kategori_list
df_map["Color_Code"] = color_code_list

with map_col:
    # Peta Scatter Plotly dengan Titik Terang & Jelas
    fig_map = px.scatter_mapbox(
        df_map,
        lat="lat",
        lon="lon",
        hover_name="Kabupaten",
        hover_data={"Capaian": ":.1f%", "Realisasi": ":.1f", "Target": ":.1f", "lat": False, "lon": False, "Kategori_Status": True},
        color="Kategori_Status",
        color_discrete_map={
            "Sangat Baik (≥100%)": "#10B981",
            "Baik (80%-99.9%)": "#3B82F6",
            "Cukup (60%-79.9%)": "#F59E0B",
            "Kurang (<60%)": "#EF4444"
        },
        zoom=7.4,
        center={"lat": -2.4, "lon": 106.8}
    )

    fig_map.update_traces(
        marker=dict(size=24, opacity=0.95)
    )

    fig_map.update_layout(
        mapbox_style="open-street-map",
        height=430,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        legend_title="Kategori Kinerja"
    )

    st.plotly_chart(fig_map, use_container_width=True)

with info_map_col:
    st.markdown("""
    <div style="background:#FFFFFF; border:1.5px solid #CBD5E1; border-radius:18px; padding:20px; box-shadow:0 8px 22px rgba(0,0,0,0.05);">
        <div style="font-size:15px; font-weight:800; color:#0B4EA2; margin-bottom:10px;">🟢 Legend & Kategori Wilayah</div>
        <div style="font-size:13px; color:#475569; line-height:1.7; margin-bottom:14px;">
            Titik warna pada peta mewakili besaran persentase capaian indikator di 7 Kabupaten/Kota se-Provinsi Babel.
        </div>
        <hr style="border:none; border-top:1px solid #E2E8F0; margin:14px 0;">
        <div style="font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;">Status Kategori Warna:</div>
        <div style="font-size:12.5px; color:#334155; line-height:2.2;">
            <div>🟢 <b>Sangat Baik (≥ 100%)</b></div>
            <div>🔵 <b>Baik (80% - 99,99%)</b></div>
            <div>🟡 <b>Cukup (60% - 79,99%)</b></div>
            <div>🔴 <b>Kurang (< 60%)</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# LINK DOWNLOAD EXCEL GOOGLE SHEETS (BIRU SOLID NIMBUL 3D)
# =====================================================

download_url = "https://docs.google.com/spreadsheets/d/1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/export?format=xlsx"
sheet_url = "https://docs.google.com/spreadsheets/d/1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/edit?usp=sharing"

try:
    response = requests.get(download_url, timeout=10)
    file_bytes = response.content
except Exception:
    file_bytes = b""

st.markdown("<br>", unsafe_allow_html=True)
kosong, kanan = st.columns([7, 3])

with kanan:
    st.link_button(
        "📄 Lihat Laporan PERKIN 2026",
        sheet_url,
        use_container_width=True
    )
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Laporan PERKIN 2026",
        data=file_bytes,
        file_name="PERKIN & REALISASI PER KAB_KOTA 2026.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# =====================================================
# FOOTER (PRESERVED 100%)
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="footer-container">
    <div class="footer-title">Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN</div>
    <div class="footer-subtitle">Perwakilan BKKBN Provinsi Kepulauan Bangka Belitung</div>
    <div class="footer-copy">Dashboard PERKIN 2026 | © BKKBN BANGKA BELITUNG 2026</div>
</div>
""", unsafe_allow_html=True)

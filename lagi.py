import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import requests
import base64
import os

\# =====================================================
\# PAGE CONFIG
\# =====================================================
st.set\_page\_config(
    page\_title="Dashboard PERKIN 2026",
    page\_icon="📊",
    layout="wide",
    initial\_sidebar\_state="collapsed"
)

\# Helper fungsi pembaca gambar lokal (logo & landmark gambar.jpg)
def load\_local\_image\_b64(file\_name):
    script\_dir = os.path.dirname(os.path.abspath(\_\_file\_\_))
    full\_path = os.path.join(script\_dir, file\_name)
    if not os.path.exists(full\_path) and os.path.exists(file\_name):
        full\_path = file\_name
    if os.path.exists(full\_path):
        ext = full\_path.split('.')[-1].lower()
        mime\_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png" if ext == "png" else f"image/{ext}"
        try:
            with open(full\_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                return f"data:{mime\_type};base64,{encoded}"
        except Exception:
            return None
    return None

logo\_b64 = load\_local\_image\_b64("logo\_bkkbnbaru.png")
babel\_img\_b64 = load\_local\_image\_b64("gambar1.jpg")

logo\_src = logo\_b64 if logo\_b64 else "logo\_bkkbnbaru.png"
FALLBACK\_URL = "[https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Mercusuar\_Pulau\_Lengkuas.jpg/800px-Mercusuar\_Pulau\_Lengkuas.jpg](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Mercusuar_Pulau_Lengkuas.jpg/800px-Mercusuar_Pulau_Lengkuas.jpg)"
bg\_image\_src = babel\_img\_b64 if babel\_img\_b64 else FALLBACK\_URL

\# =====================================================
\# CSS STYLING (PRESISI 100% SEPERTI DASHBOARD UTAMA BERANDA)
\# =====================================================
st.markdown("""
\<style>

@import url('[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans\:wght@300;400;500;600;700;800&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans\:wght@300;400;500;600;700;800\&display=swap)');

html, body, [class\*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/\* Background Soft Ambient Light Blue \*/
.stApp {
    background-color: #EEF4FB;
    background-image:&#x20;
        radial-gradient(circle at 5% 5%, rgba(147, 197, 253, 0.35) 0%, transparent 35%),
        radial-gradient(circle at 95% 15%, rgba(59, 130, 246, 0.2) 0%, transparent 40%),
        radial-gradient(circle at 10% 60%, rgba(224, 242, 254, 0.5) 0%, transparent 40%),
        radial-gradient(circle at 90% 85%, rgba(191, 219, 254, 0.4) 0%, transparent 45%);
    background-attachment: fixed;
}

/\* Hide default Streamlit components \*/
\#MainMenu, footer, header {
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

/\* Top Navbar (Logo di sebelah Header Atas) \*/
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

/\* Tombol Kembali ke Beranda (Kanan Atas) \*/
div.stLinkButton > a[href\*="utama"],
div.stLinkButton > a[href\*="sipelikes"] {
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

div.stLinkButton > a\:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(21, 101, 192, 0.45) !important;
}

/\* Hero Header Banner (100% Persis Beranda Utama) \*/
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

/\* Dropdown Selectbox: Putih Bersih Nimbul 3D \*/
div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08) !important;
    border: 1.5px solid #CBD5E1 !important;
    transition: all 0.25s ease !important;
}

div[data-baseweb="select"]\:hover {
    border-color: #1565C0 !important;
    box-shadow: 0 8px 22px rgba(21, 101, 192, 0.18) !important;
}

div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-radius: 14px !important;
    color: #0F172A !important;
    font-weight: 600 !important;
}

/\* Metric Cards Streamlit (Efek Nimbul) \*/
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 20px !important;
    padding: 22px !important;
    border: 1.5px solid #E2E8F0 !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

div[data-testid="stMetric"]\:hover {
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

/\* Section Header Titles \*/
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

/\* ===========================
SECTION FILTER
\=========================== \*/

.filter-section{

    background:#FFFFFF;

    padding:22px;

    border-radius:22px;

    border:1px solid #DCE6F3;

    box-shadow:0 10px 24px rgba(0,0,0,.08);

    margin-bottom:20px;

}

/\* Judul \*/

.section-title-text{

    font-size:24px;

    font-weight:800;

    color:#0B4EA2;

    margin-bottom:15px;

}

/\* Selectbox \*/

div[data-testid="stSelectbox"]{

    background:#FFFFFF;

    padding:8px;

    border-radius:16px;

    box-shadow:0 6px 18px rgba(0,0,0,.06);

    border:1px solid #E2E8F0;

}

/\* Hover \*/

div[data-testid="stSelectbox"]\:hover{

    border:1px solid #1976D2;

}

/\* Label \*/

label{

    font-weight:700 !important;

    color:#0B4EA2 !important;

}

/\* TOMBOL AKSI LAPORAN & DOWNLOAD: BIRU SOLID EFEK TIMBUL 3D \*/
div.stLinkButton > a[href\*="sheet"],
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

div.stLinkButton > a[href\*="sheet"]\:hover,
div.stDownloadButton > button\:hover {
    background: linear-gradient(135deg, #09448D 0%, #0D47A1 100%) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 28px rgba(11, 78, 162, 0.45) !important;
    color: white !important;
}

/\* Footer Container \*/
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

\</style>
""", unsafe\_allow\_html=True)

\# =====================================================
\# GOOGLE SHEETS & FUNGSI BACA DATA (PRESERVED 100%)
\# =====================================================

sheet\_id = "13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

bulan\_sheet = {
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

\# =====================================================
\# TOP NAVBAR (LOGO BKKBN SEBELAH HEADER DISUKAI USER)
\# =====================================================

c\_nav1, c\_nav2 = st.columns([8, 3])

with c\_nav1:
    st.markdown(f"""
    \<div class="brand-container">
        \<img src="{logo\_src}" class="brand-logo-img" alt="Logo BKKBN" />
        \<div>
            \<div class="brand-text-title">Kementerian Kependudukan dan Pembangunan Keluarga/BKKBN\</div>
            \<div class="brand-text-sub">Perwakilan BKKBN Provinsi Kepulauan Bangka Belitung\</div>
        \</div>
    \</div>
    """, unsafe\_allow\_html=True)

with c\_nav2:
    st.link\_button(
        "⬅ Kembali ke Beranda",
        "[https://dashboard-perkin-utama.streamlit.app/](https://dashboard-perkin-utama.streamlit.app/)",
        use\_container\_width=True
    )

st.markdown("\<div style='height:14px'>\</div>", unsafe\_allow\_html=True)

\# =====================================================
\# HERO HEADER BANNER (SAMAIN DENGAN DASHBOARD UTAMA BERANDA)
\# =====================================================

hero\_html = f"""\<div class="hero-banner">
\<img src="{bg\_image\_src}" class="hero-bg-blend-image" alt="Background Babel Landmark" />

\<div class="hero-content">
\<div class="hero-subtitle-top">Selamat Datang di\</div>
\<div class="hero-title">Dashboard PERKIN 2026\</div>
\<div class="hero-title-underline">\</div>
\<div class="hero-desc">
Realisasi Kinerja Program Bangga Kencana\<br>
Provinsi Kepulauan Bangka Belitung
\</div>
\<div class="hero-badge">
🏛️ Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN
\</div>
\</div>
\</div>"""

st.markdown(hero\_html, unsafe\_allow\_html=True)

\# =====================================================
\# FILTER SECTION (PILIH BULAN & INDIKATOR - PRESERVED)
\# =====================================================

f1, f2 = st.columns(2)

\# PILIH BULAN
with f1:
    st.markdown("""\<div class="section-title-text">📅 Pilih Bulan\</div>""", unsafe\_allow\_html=True)

    bulan = st.selectbox(
        "",
        list(bulan\_sheet.keys()),
        label\_visibility="collapsed"
    )
    info\_bulan = st.empty()

\# LOAD DATA DARI GOOGLE SHEETS
nama\_sheet = bulan\_sheet[bulan]
url = f"[https://docs.google.com/spreadsheets/d/{sheet\_id}/gviz/tq?tqx=out\:csv&sheet={nama\_sheet](https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out\:csv\&sheet={nama_sheet)}"

try:
    df = pd.read\_csv(url)
    df.columns = df.columns.str.strip()
    df["Indikator"] = df["Indikator"].astype(str).str.strip()
    df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()
    df["Target"] = pd.to\_numeric(df["Target"], errors="coerce").fillna(0)
    df["Realisasi"] = pd.to\_numeric(df["Realisasi"], errors="coerce").fillna(0)
except Exception:
    df = pd.DataFrame([
        {"Indikator\_Provinsi": "Keluarga Berencana", "Indikator": "Persentase Peserta KB Aktif", "Kabupaten": "Bangka", "Target": 90.0, "Realisasi": 88.0, "Capaian": 97.78},
        {"Indikator\_Provinsi": "Keluarga Berencana", "Indikator": "Persentase Peserta KB Aktif", "Kabupaten": "Belitung", "Target": 90.0, "Realisasi": 90.0, "Capaian": 100.00},
        {"Indikator\_Provinsi": "Keluarga Berencana", "Indikator": "Persentase Peserta KB Aktif", "Kabupaten": "Bangka Selatan", "Target": 90.0, "Realisasi": 85.0, "Capaian": 94.44},
        {"Indikator\_Provinsi": "Keluarga Berencana", "Indikator": "Persentase Peserta KB Aktif", "Kabupaten": "Bangka Tengah", "Target": 90.0, "Realisasi": 93.0, "Capaian": 103.33},
        {"Indikator\_Provinsi": "Keluarga Berencana", "Indikator": "Persentase Peserta KB Aktif", "Kabupaten": "Bangka Barat", "Target": 90.0, "Realisasi": 95.0, "Capaian": 105.56},
        {"Indikator\_Provinsi": "Keluarga Berencana", "Indikator": "Persentase Peserta KB Aktif", "Kabupaten": "Belitung Timur", "Target": 90.0, "Realisasi": 92.0, "Capaian": 102.22},
        {"Indikator\_Provinsi": "Keluarga Berencana", "Indikator": "Persentase Peserta KB Aktif", "Kabupaten": "Pangkalpinang", "Target": 90.0, "Realisasi": 75.0, "Capaian": 83.33},
    ])

\# PILIH INDIKATOR
with f2:
    st.markdown("""\<div class="section-title-text">📊 Pilih Indikator\</div>""", unsafe\_allow\_html=True)

    prov\_opts = sorted(df["Indikator\_Provinsi"].dropna().unique()) if "Indikator\_Provinsi" in df.columns else ["Keluarga Berencana"]
    indikator\_prov = st.selectbox("Indikator Provinsi", prov\_opts)

    df\_prov = df[df["Indikator\_Provinsi"] == indikator\_prov] if "Indikator\_Provinsi" in df.columns else df

    kab\_opts = sorted(df\_prov["Indikator"].dropna().unique())
    indikator = st.selectbox("Indikator Kabupaten", kab\_opts)

\# FILTER DATA SESUAI SELEKSI
df\_filter = df\_prov[df\_prov["Indikator"] == indikator].copy()

if "Capaian" in df\_filter.columns:
    df\_filter["Capaian"] = (
        df\_filter["Capaian"]
        .astype(str)
        .str.replace("%","", regex=False)
        .str.replace(",",".", regex=False)
    )
    df\_filter["Capaian"] = pd.to\_numeric(df\_filter["Capaian"], errors="coerce").fillna(0)
else:
    df\_filter["Capaian"] = (df\_filter["Realisasi"] / df\_filter["Target"].replace(0, 1)) \* 100

atas\_target = (df\_filter["Capaian"] >= 100).sum()
bawah\_target = (df\_filter["Capaian"] < 100).sum()

with info\_bulan.container():
    st.markdown(f"""
    \<div style="background:#FFFFFF; padding:12px 16px; border-radius:16px; margin-top:12px; border:1.5px solid #E2E8F0; box-shadow:0 6px 18px rgba(0,0,0,0.05);">
        \<div style="font-size:13.5px; color:#15803D; margin-bottom:4px;">🏆 \<b>{atas\_target}\</b> Kabupaten/Kota di atas target\</div>
        \<div style="font-size:13.5px; color:#DC2626;">📉 \<b>{bawah\_target}\</b> Kabupaten/Kota di bawah target\</div>
    \</div>
    """, unsafe\_allow\_html=True)

\# =====================================================
\# HITUNG METRIK KPI & LAYOUT KPI CARDS
\# =====================================================

jumlah\_kab = df\_filter["Kabupaten"].nunique()
total\_target = round(df\_filter["Target"].sum() / jumlah\_kab, 2) if jumlah\_kab > 0 else 0
total\_realisasi = df\_filter["Realisasi"].sum()
persen = round(
    ((df\_filter["Realisasi"] / df\_filter["Target"]) \* 100).sum() / 7,
    2
)
jumlah\_lapor = df\_filter[df\_filter["Realisasi"].fillna(0) > 0]["Kabupaten"].nunique()
total\_kab = df\_filter["Kabupaten"].nunique()

st.markdown("\<br>", unsafe\_allow\_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        label="🎯 Total Target",
        value=f"{total\_target:.2f}",
        help="Nilai yang ditampilkan merupakan rata-rata target Kabupaten/Kota pada indikator yang dipilih."
    )

with k2:
    st.metric(
        label="✅ Total Realisasi",
        value=f"{total\_realisasi:,.0f}",
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
        value=f"{jumlah\_lapor}/{total\_kab}"
    )

st.markdown("\<br>", unsafe\_allow\_html=True)

\# =====================================================
\# GRAFIK (BAR CHART & HORIZONTAL CHART - PRESERVED 100%)
\# =====================================================

left\_chart, right\_chart = st.columns([1.4, 1])

with left\_chart:
    st.markdown('\<div class="section-title-text">📊 Target vs Realisasi\</div>', unsafe\_allow\_html=True)
    st.markdown(f'\<div class="section-subtitle-text">ℹ️ Grafik menampilkan \<b>data kumulatif\</b> periode \<b>Januari–{bulan}\</b>.\</div>', unsafe\_allow\_html=True)

    df\_bar = pd.melt(
        df\_filter,
        id\_vars="Kabupaten",
        value\_vars=["Target", "Realisasi"],
        var\_name="Kategori",
        value\_name="Nilai"
    )

    fig1 = px.bar(
        df\_bar,
        x="Kabupaten",
        y="Nilai",
        color="Kategori",
        barmode="group",
        text="Nilai",
        color\_discrete\_map={
            "Target": "#2F80ED",
            "Realisasi": "#2ECC71"
        }
    )

    fig1.update\_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig1.update\_layout(
        height=380,
        paper\_bgcolor="white",
        plot\_bgcolor="white",
        legend\_title="",
        legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center", yanchor="top"),
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(title="Jumlah", range=[0, max(df\_filter["Target"].max(), 10) \* 1.18]),
        xaxis\_title=""
    )

    st.plotly\_chart(fig1, use\_container\_width=True, config={"displayModeBar": False})

with right\_chart:
    st.markdown('\<div class="section-title-text">📈 Persentase Capaian\</div>', unsafe\_allow\_html=True)
    st.markdown(f'\<div class="section-subtitle-text">ℹ️ Grafik menampilkan \<b>data kumulatif\</b> periode \<b>Januari–{bulan}\</b>.\</div>', unsafe\_allow\_html=True)

    max\_capaian = df\_filter["Capaian"].max()

    fig2 = px.bar(
        df\_filter.sort\_values(by="Capaian", ascending=True),
        x="Capaian",
        y="Kabupaten",
        orientation="h",
        text="Capaian",
        color="Capaian",
        color\_continuous\_scale="Blues"
    )

    fig2.update\_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig2.add\_vline(
        x=100,
        line\_dash="dash",
        line\_color="red",
        annotation\_text="100%"
    )

    fig2.update\_layout(
        coloraxis\_showscale=False,
        height=380,
        paper\_bgcolor="white",
        plot\_bgcolor="white",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Persentase (%)", range=[0, max(100, max\_capaian + 10)]),
        yaxis\_title=""
    )

    st.plotly\_chart(fig2, use\_container\_width=True, config={"displayModeBar": False})

\# =====================================================
\# SPATIAL MAPPING
\# =====================================================

st.markdown(
    f'''
    \<div class="section-title-text">
        📍 Peta Capaian per Kabupaten/Kota
        \<span style="font-size:14px; color:#64748B; font-weight:500;">
            (Tahun 2023)
        \</span>
    \</div>
    ''',
    unsafe\_allow\_html=True
)

st.markdown(
    '''
    \<div class="section-subtitle-text">
        Hover / Sentuh titik wilayah pada peta untuk melihat detail target dan realisasi
    \</div>
    ''',
    unsafe\_allow\_html=True
)

map\_col, info\_map\_col = st.columns([2.3, 1])

\# =====================================================
\# KOORDINAT 7 KABUPATEN/KOTA BABEL
\# =====================================================

geo\_babel = pd.DataFrame([
    {"Kabupaten": "Pangkalpinang", "lat": -2.130, "lon": 106.110},
    {"Kabupaten": "Bangka", "lat": -1.860, "lon": 106.110},
    {"Kabupaten": "Bangka Barat", "lat": -1.900, "lon": 105.450},
    {"Kabupaten": "Bangka Tengah", "lat": -2.350, "lon": 106.100},
    {"Kabupaten": "Bangka Selatan", "lat": -2.850, "lon": 106.250},
    {"Kabupaten": "Belitung", "lat": -2.750, "lon": 107.750},
    {"Kabupaten": "Belitung Timur", "lat": -2.850, "lon": 108.150},
])

\# Gabungkan koordinat dengan data indikator
df\_map = pd.merge(
    geo\_babel,
    df\_filter,
    on="Kabupaten",
    how="left"
)

\# Isi data kosong
df\_map["Capaian"] = df\_map["Capaian"].fillna(0)
df\_map["Realisasi"] = df\_map["Realisasi"].fillna(0)
df\_map["Target"] = df\_map["Target"].fillna(0)

\# =====================================================
\# KATEGORI STATUS
\# =====================================================

kategori\_list = []

for cap in df\_map["Capaian"]:

    if cap >= 100:
        kategori\_list.append("Sangat Baik (≥100%)")

    elif cap >= 80:
        kategori\_list.append("Baik (80%-99.9%)")

    elif cap >= 60:
        kategori\_list.append("Cukup (60%-79.9%)")

    else:
        kategori\_list.append("Kurang (<60%)")

df\_map["Kategori\_Status"] = kategori\_list

\# =====================================================
\# PETA
\# =====================================================

with map\_col:

    fig\_map = px.scatter\_map(
        df\_map,

        lat="lat",
        lon="lon",

        hover\_name="Kabupaten",

        hover\_data={
            "Capaian": ":.1f",
            "Realisasi": ":.1f",
            "Target": ":.1f",
            "lat": False,
            "lon": False,
            "Kategori\_Status": True
        },

        color="Kategori\_Status",

        color\_discrete\_map={
            "Sangat Baik (≥100%)": "#10B981",
            "Baik (80%-99.9%)": "#3B82F6",
            "Cukup (60%-79.9%)": "#F59E0B",
            "Kurang (<60%)": "#EF4444"
        },

        zoom=7.4,

        center={
            "lat": -2.4,
            "lon": 106.8
        }
    )

    fig\_map.update\_traces(
        marker=dict(
            size=24,
            opacity=0.95
        )
    )

    fig\_map.update\_layout(
        map\_style="open-street-map",

        height=430,

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        paper\_bgcolor="white",

        legend\_title="Kategori Kinerja"
    )

    st.plotly\_chart(
        fig\_map,
        use\_container\_width=True,
        config={
            "displayModeBar": False
        }
    )

\# =====================================================
\# INFO LEGEND
\# =====================================================

with info\_map\_col:

    st.markdown(
        """
        \<div style="
            background:#FFFFFF;
            border:1.5px solid #CBD5E1;
            border-radius:18px;
            padding:20px;
            box-shadow:0 8px 22px rgba(0,0,0,0.05);
        ">

            \<div style="
                font-size:15px;
                font-weight:800;
                color:#0B4EA2;
                margin-bottom:10px;
            ">
                📍 Legend & Kategori Wilayah
            \</div>

            \<div style="
                font-size:13px;
                color:#475569;
                line-height:1.7;
                margin-bottom:14px;
            ">
                Titik warna pada peta mewakili besaran
                persentase capaian indikator di
                7 Kabupaten/Kota se-Provinsi Babel.
            \</div>

            \<hr style="
                border\:none;
                border-top:1px solid #E2E8F0;
                margin:14px 0;
            ">

            \<div style="
                font-size:13px;
                font-weight:700;
                color:#0F172A;
                margin-bottom:10px;
            ">
                Status Kategori Warna:
            \</div>

            \<div style="
                font-size:12.5px;
                color:#334155;
                line-height:2.2;
            ">

                \<div>🟢 \<b>Sangat Baik (≥ 100%)\</b>\</div>

                \<div>🔵 \<b>Baik (80% - 99,99%)\</b>\</div>

                \<div>🟡 \<b>Cukup (60% - 79,99%)\</b>\</div>

                \<div>🔴 \<b>Kurang (&lt; 60%)\</b>\</div>

            \</div>

        \</div>
        """,
        unsafe\_allow\_html=True
    )

\# =====================================================
\# LINK DOWNLOAD EXCEL GOOGLE SHEETS (BIRU SOLID NIMBUL 3D)
\# =====================================================

download\_url = "[https://docs.google.com/spreadsheets/d/1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/export?format=xlsx](https://docs.google.com/spreadsheets/d/1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/export?format=xlsx)"
sheet\_url = "[https://docs.google.com/spreadsheets/d/1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/edit?usp=sharing)"

try:
    response = requests.get(download\_url, timeout=10)
    file\_bytes = response.content
except Exception:
    file\_bytes = b""

st.markdown("\<br>", unsafe\_allow\_html=True)
kosong, kanan = st.columns([7, 3])

with kanan:
    st.link\_button(
        "📄 Lihat Laporan PERKIN 2026",
        sheet\_url,
        use\_container\_width=True
    )
    st.markdown("\<div style='height:10px'>\</div>", unsafe\_allow\_html=True)
    st.download\_button(
        label="📥 Download Laporan PERKIN 2026",
        data=file\_bytes,
        file\_name="PERKIN & REALISASI PER KAB\_KOTA 2026.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use\_container\_width=True
    )

\# =====================================================
\# FOOTER (PRESERVED 100%)
\# =====================================================

st.markdown("\<br>", unsafe\_allow\_html=True)

st.markdown("""
\<div class="footer-container">
    \<div class="footer-title">Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN\</div>
    \<div class="footer-subtitle">Perwakilan BKKBN Provinsi Kepulauan Bangka Belitung\</div>
    \<div class="footer-copy">Dashboard PERKIN 2026 | © BKKBN BANGKA BELITUNG 2026\</div>
\</div>
""", unsafe\_allow\_html=True)

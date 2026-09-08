import streamlit as st
import pandas as pd
import plotly.express as px
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


# =====================================================
# KONFIGURASI
# =====================================================

SHEET_ID = "13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

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
# HELPER
# =====================================================

def load_local_image_b64(file_name):

    script_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    full_path = os.path.join(
        script_dir,
        file_name
    )

    if not os.path.exists(full_path):
        return None

    try:

        ext = os.path.splitext(full_path)[1].lower()

        if ext in [".jpg", ".jpeg"]:
            mime = "image/jpeg"
        elif ext == ".png":
            mime = "image/png"
        elif ext == ".webp":
            mime = "image/webp"
        else:
            return None

        with open(full_path, "rb") as f:
            encoded = base64.b64encode(
                f.read()
            ).decode("utf-8")

        return f"data:{mime};base64,{encoded}"

    except Exception:
        return None


# =====================================================
# LOAD GAMBAR
# =====================================================

logo_b64 = load_local_image_b64(
    "logo_bkkbnbaru.png"
)

babel_img_b64 = load_local_image_b64(
    "gambar1.jpg"
)

logo_src = logo_b64 or "logo_bkkbnbaru.png"

FALLBACK_URL = (
    "https://upload.wikimedia.org/"
    "wikipedia/commons/thumb/7/7b/"
    "Mercusuar_Pulau_Lengkuas.jpg/"
    "800px-Mercusuar_Pulau_Lengkuas.jpg"
)

bg_image_src = babel_img_b64 or FALLBACK_URL


# =====================================================
# CSS
# =====================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap'
    );

    html,
    body,
    [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #EEF4FB;
        background-image:
            radial-gradient(
                circle at 5% 5%,
                rgba(147, 197, 253, 0.30),
                transparent 35%
            ),
            radial-gradient(
                circle at 95% 15%,
                rgba(59, 130, 246, 0.15),
                transparent 40%
            );
        background-attachment: fixed;
    }

    #MainMenu,
    footer,
    header {
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

    div.stLinkButton > a {
        background: linear-gradient(
            135deg,
            #1565C0,
            #0D47A1
        ) !important;

        color: white !important;
        border-radius: 50px !important;
        padding: 11px 26px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border: none !important;
        text-decoration: none !important;
    }

    .hero-banner {
        position: relative;
        background:
            linear-gradient(
                135deg,
                #0B4EA2 0%,
                #1565C0 55%,
                #1D60DB 100%
            );
        border-radius: 28px;
        padding: 44px 50px;
        color: white;
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
        opacity: 0.72;
        -webkit-mask-image:
            linear-gradient(
                to left,
                rgba(0,0,0,1),
                rgba(0,0,0,0)
            );
        mask-image:
            linear-gradient(
                to left,
                rgba(0,0,0,1),
                rgba(0,0,0,0)
            );
        pointer-events: none;
    }

    .hero-content {
        position: relative;
        z-index: 2;
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
        color: #FFFFFF;
        line-height: 1.1;
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
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.32);
        padding: 9px 20px;
        border-radius: 50px;
        font-size: 13.5px;
        font-weight: 600;
        color: #FFFFFF;
    }

    .section-title-text {
        font-size: 24px;
        font-weight: 800;
        color: #0B4EA2;
        margin-bottom: 8px;
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

    div[data-testid="stSelectbox"] {
        background: #FFFFFF;
        padding: 8px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow:
            0 6px 18px rgba(0,0,0,0.05);
    }

    label {
        font-weight: 700 !important;
        color: #0B4EA2 !important;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border-radius: 20px !important;
        padding: 22px !important;
        border: 1.5px solid #E2E8F0 !important;
        box-shadow:
            0 8px 22px rgba(0,0,0,0.06) !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #64748B !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800 !important;
        color: #0B4EA2 !important;
    }

    div.stDownloadButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 14px !important;
        background:
            linear-gradient(
                135deg,
                #0B4EA2,
                #1565C0
            ) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    .footer-container {
        margin-top: 45px;
        padding: 26px 20px;
        background:
            linear-gradient(
                135deg,
                #0B4EA2,
                #1565C0
            );
        border-radius: 20px;
        color: white;
        text-align: center;
    }

    .footer-title {
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .footer-subtitle {
        font-size: 13.5px;
        color: #DBEAFE;
        margin-bottom: 12px;
    }

    .footer-copy {
        font-size: 13px;
        color: rgba(255,255,255,0.75);
        border-top: 1px solid rgba(255,255,255,0.18);
        padding-top: 12px;
        margin-top: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# FUNGSI LOAD GOOGLE SHEETS
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def load_google_sheet(sheet_name):

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/gviz/tq?"
        f"tqx=out:csv&sheet={sheet_name}"
    )

    try:

        df = pd.read_csv(
            url,
            timeout=15
        )

    except Exception as e:

        return None, f"Gagal mengambil data: {e}"

    if df.empty:
        return None, "Sheet tidak memiliki data."

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    required = [
        "Indikator",
        "Kabupaten",
        "Target",
        "Realisasi"
    ]

    missing = [
        col
        for col in required
        if col not in df.columns
    ]

    if missing:

        return (
            None,
            "Kolom tidak ditemukan: "
            + ", ".join(missing)
        )

    df["Indikator"] = (
        df["Indikator"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["Kabupaten"] = (
        df["Kabupaten"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["Target"] = pd.to_numeric(
        df["Target"],
        errors="coerce"
    ).fillna(0)

    df["Realisasi"] = pd.to_numeric(
        df["Realisasi"],
        errors="coerce"
    ).fillna(0)

    return df, None


# =====================================================
# NAVBAR
# =====================================================

nav1, nav2 = st.columns(
    [8, 3]
)

with nav1:

    st.markdown(
        f"""
        <div class="brand-container">

            <img
                src="{logo_src}"
                class="brand-logo-img"
                alt="Logo BKKBN"
            >

            <div>

                <div class="brand-text-title">
                    Kementerian Kependudukan dan
                    Pembangunan Keluarga/BKKBN
                </div>

                <div class="brand-text-sub">
                    Perwakilan BKKBN Provinsi
                    Kepulauan Bangka Belitung
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with nav2:

    st.link_button(
        "⬅ Kembali ke Beranda",
        "https://dashboard-perkin-utama.streamlit.app/",
        use_container_width=True
    )


st.markdown(
    "<div style='height:14px'></div>",
    unsafe_allow_html=True
)


# =====================================================
# HERO
# =====================================================

st.markdown(
    f"""
    <div class="hero-banner">

        <img
            src="{bg_image_src}"
            class="hero-bg-blend-image"
            alt="Background Babel"
        >

        <div class="hero-content">

            <div class="hero-subtitle-top">
                Selamat Datang di
            </div>

            <div class="hero-title">
                Dashboard PERKIN 2026
            </div>

            <div class="hero-title-underline"></div>

            <div class="hero-desc">
                Realisasi Kinerja Program Bangga Kencana
                <br>
                Provinsi Kepulauan Bangka Belitung
            </div>

            <div class="hero-badge">
                🏛️ Kementerian Kependudukan dan
                Pembangunan Keluarga / BKKBN
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# FILTER
# =====================================================

f1, f2 = st.columns(2)


with f1:

    st.markdown(
        """
        <div class="section-title-text">
            📅 Pilih Bulan
        </div>
        """,
        unsafe_allow_html=True
    )

    bulan = st.selectbox(
        "Bulan",
        list(bulan_sheet.keys()),
        index=0,
        label_visibility="collapsed"
    )


with f2:

    st.markdown(
        """
        <div class="section-title-text">
            📊 Pilih Indikator
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# LOAD DATA
# =====================================================

nama_sheet = bulan_sheet[bulan]

df, error_message = load_google_sheet(
    nama_sheet
)


if df is None:

    st.error(
        f"Data bulan {bulan} tidak dapat dimuat."
    )

    st.caption(error_message)

    st.stop()


# =====================================================
# PILIH INDIKATOR
# =====================================================

indikator_list = sorted(
    df["Indikator"]
    .dropna()
    .astype(str)
    .loc[
        lambda x: x.str.strip() != ""
    ]
    .unique()
    .tolist()
)


if not indikator_list:

    st.warning(
        f"Tidak ada indikator pada sheet {nama_sheet}."
    )

    st.stop()


with f2:

    indikator = st.selectbox(
        "Indikator",
        indikator_list
    )


# =====================================================
# FILTER DATA
# =====================================================

df_filter = df[
    df["Indikator"] == indikator
].copy()


if df_filter.empty:

    st.info(
        "Belum ada data untuk indikator ini."
    )

    st.stop()


# =====================================================
# HITUNG CAPAIAN
# =====================================================

target = df_filter["Target"].copy()

target_aman = target.replace(
    0,
    pd.NA
)

df_filter["Capaian"] = (
    df_filter["Realisasi"]
    / target_aman
) * 100

df_filter["Capaian"] = (
    df_filter["Capaian"]
    .fillna(0)
    .clip(lower=0)
)


# =====================================================
# STATUS
# =====================================================

atas_target = int(
    (
        df_filter["Capaian"] >= 100
    ).sum()
)

bawah_target = int(
    (
        df_filter["Capaian"] < 100
    ).sum()
)


# =====================================================
# INFO BULAN
# =====================================================

st.markdown(
    f"""
    <div style="
        background:#FFFFFF;
        padding:12px 16px;
        border-radius:16px;
        margin-top:12px;
        margin-bottom:20px;
        border:1.5px solid #E2E8F0;
        box-shadow:0 6px 18px rgba(0,0,0,0.05);
    ">

        <div style="
            font-size:13.5px;
            color:#15803D;
            margin-bottom:4px;
        ">
            🏆
            <b>{atas_target}</b>
            Kabupaten/Kota di atas target
        </div>

        <div style="
            font-size:13.5px;
            color:#DC2626;
        ">
            📉
            <b>{bawah_target}</b>
            Kabupaten/Kota di bawah target
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# KPI
# =====================================================

jumlah_kab = int(
    df_filter["Kabupaten"]
    .nunique()
)


if jumlah_kab > 0:

    total_target = (
        df_filter["Target"].sum()
        / jumlah_kab
    )

else:

    total_target = 0


total_realisasi = (
    df_filter["Realisasi"].sum()
)


capaian_valid = (
    df_filter["Capaian"]
    .replace(0, pd.NA)
    .dropna()
)


if not capaian_valid.empty:

    persen = float(
        capaian_valid.mean()
    )

else:

    persen = 0


jumlah_lapor = int(
    df_filter.loc[
        df_filter["Realisasi"] > 0,
        "Kabupaten"
    ].nunique()
)


# =====================================================
# KPI CARDS
# =====================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "🎯 Total Target",
        f"{total_target:,.2f}"
    )


with k2:

    st.metric(
        "✅ Total Realisasi",
        f"{total_realisasi:,.0f}"
    )


with k3:

    st.metric(
        "📈 Persentase Capaian",
        f"{persen:.2f}%"
    )


with k4:

    st.metric(
        "🏛️ Kabupaten/Kota yang Lapor",
        f"{jumlah_lapor}/{jumlah_kab}"
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# GRAFIK
# =====================================================

left_chart, right_chart = st.columns(
    [1.4, 1]
)


# =====================================================
# GRAFIK TARGET VS REALISASI
# =====================================================

with left_chart:

    st.markdown(
        """
        <div class="section-title-text">
            📊 Target vs Realisasi
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="section-subtitle-text">
            ℹ️ Data bulan <b>{bulan}</b>
            untuk indikator yang dipilih.
        </div>
        """,
        unsafe_allow_html=True
    )

    df_bar = pd.melt(
        df_filter,
        id_vars=["Kabupaten"],
        value_vars=[
            "Target",
            "Realisasi"
        ],
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

    nilai_maks = max(
        float(df_bar["Nilai"].max()),
        10
    )

    fig1.update_layout(
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="",
        legend=dict(
            orientation="h",
            y=-0.22,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        yaxis=dict(
            title="Jumlah",
            range=[
                0,
                nilai_maks * 1.20
            ]
        ),
        xaxis_title=""
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =====================================================
# GRAFIK CAPAIAN
# =====================================================

with right_chart:

    st.markdown(
        """
        <div class="section-title-text">
            📈 Persentase Capaian
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="section-subtitle-text">
            ℹ️ Capaian Kabupaten/Kota
            bulan <b>{bulan}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

    df_capaian = (
        df_filter
        .sort_values(
            "Capaian",
            ascending=True
        )
    )

    max_capaian = max(
        float(
            df_capaian["Capaian"].max()
        ),
        100
    )

    fig2 = px.bar(
        df_capaian,
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
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        xaxis=dict(
            title="Persentase (%)",
            range=[
                0,
                max_capaian + 10
            ]
        ),
        yaxis_title=""
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =====================================================
# PETA
# =====================================================

st.markdown(
    f"""
    <div class="section-title-text">
        📍 Peta Capaian per Kabupaten/Kota
        <span style="
            font-size:14px;
            color:#64748B;
            font-weight:500;
        ">
            (Bulan {bulan})
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-subtitle-text">
        Hover titik wilayah untuk melihat
        target, realisasi, dan capaian.
    </div>
    """,
    unsafe_allow_html=True
)


geo_babel = pd.DataFrame([
    {
        "Kabupaten": "Pangkalpinang",
        "lat": -2.130,
        "lon": 106.110
    },
    {
        "Kabupaten": "Bangka",
        "lat": -1.860,
        "lon": 106.110
    },
    {
        "Kabupaten": "Bangka Barat",
        "lat": -1.900,
        "lon": 105.450
    },
    {
        "Kabupaten": "Bangka Tengah",
        "lat": -2.350,
        "lon": 106.100
    },
    {
        "Kabupaten": "Bangka Selatan",
        "lat": -2.850,
        "lon": 106.250
    },
    {
        "Kabupaten": "Belitung",
        "lat": -2.750,
        "lon": 107.750
    },
    {
        "Kabupaten": "Belitung Timur",
        "lat": -2.850,
        "lon": 108.150
    }
])


df_map = geo_babel.merge(
    df_filter[
        [
            "Kabupaten",
            "Target",
            "Realisasi",
            "Capaian"
        ]
    ],
    on="Kabupaten",
    how="left"
)


df_map["Target"] = pd.to_numeric(
    df_map["Target"],
    errors="coerce"
).fillna(0)

df_map["Realisasi"] = pd.to_numeric(
    df_map["Realisasi"],
    errors="coerce"
).fillna(0)

df_map["Capaian"] = pd.to_numeric(
    df_map["Capaian"],
    errors="coerce"
).fillna(0)


def kategori_capaian(nilai):

    if nilai >= 100:
        return "Sangat Baik (≥100%)"

    if nilai >= 80:
        return "Baik (80%-99.9%)"

    if nilai >= 60:
        return "Cukup (60%-79.9%)"

    return "Kurang (<60%)"


df_map["Kategori_Status"] = (
    df_map["Capaian"]
    .apply(kategori_capaian)
)


map_col, info_col = st.columns(
    [2.3, 1]
)


with map_col:

    fig_map = px.scatter_geo(
        df_map,
        lat="lat",
        lon="lon",
        scope="asia",
        projection="mercator",
        color="Kategori_Status",
        hover_name="Kabupaten",
        hover_data={
            "Target": ":.1f",
            "Realisasi": ":.1f",
            "Capaian": ":.1f",
            "Kategori_Status": True,
            "lat": False,
            "lon": False
        },
        color_discrete_map={
            "Sangat Baik (≥100%)": "#10B981",
            "Baik (80%-99.9%)": "#3B82F6",
            "Cukup (60%-79.9%)": "#F59E0B",
            "Kurang (<60%)": "#EF4444"
        }
    )

    fig_map.update_traces(
        marker=dict(
            size=18,
            opacity=0.95,
            line=dict(
                width=2,
                color="white"
            )
        )
    )

    fig_map.update_geos(
        showland=True,
        landcolor="#E8F1F8",
        showocean=True,
        oceancolor="#DCEEFF",
        showcountries=True,
        countrycolor="#94A3B8",
        showcoastlines=True,
        coastlinecolor="#64748B",
        showlakes=True,
        lakecolor="#DCEEFF",
        center={
            "lat": -2.4,
            "lon": 106.8
        },
        lataxis_range=[
            -3.3,
            -1.4
        ],
        lonaxis_range=[
            104.9,
            108.7
        ]
    )

    fig_map.update_layout(
        height=430,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            title="Kategori Kinerja",
            orientation="v",
            y=0.98,
            x=0.02,
            bgcolor="rgba(255,255,255,0.90)",
            bordercolor="#CBD5E1",
            borderwidth=1
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =====================================================
# INFO PETA
# =====================================================

with info_col:

    st.markdown(
        """
        <div style="
            background:#FFFFFF;
            border:1.5px solid #CBD5E1;
            border-radius:18px;
            padding:20px;
            box-shadow:0 8px 22px rgba(0,0,0,0.05);
        ">

            <div style="
                font-size:15px;
                font-weight:800;
                color:#0B4EA2;
                margin-bottom:10px;
            ">
                📍 Legend & Kategori Wilayah
            </div>

            <div style="
                font-size:13px;
                color:#475569;
                line-height:1.7;
                margin-bottom:14px;
            ">
                Titik pada peta mewakili
                persentase capaian indikator
                pada 7 Kabupaten/Kota
                di Provinsi Kepulauan Bangka Belitung.
            </div>

            <hr style="
                border:none;
                border-top:1px solid #E2E8F0;
                margin:14px 0;
            ">

            <div style="
                font-size:13px;
                font-weight:700;
                color:#0F172A;
                margin-bottom:10px;
            ">
                Status Kategori Warna:
            </div>

            <div style="
                font-size:12.5px;
                color:#334155;
                line-height:2.2;
            ">

                <div>
                    🟢 <b>Sangat Baik (≥ 100%)</b>
                </div>

                <div>
                    🔵 <b>Baik (80% - 99,99%)</b>
                </div>

                <div>
                    🟡 <b>Cukup (60% - 79,99%)</b>
                </div>

                <div>
                    🔴 <b>Kurang (&lt; 60%)</b>
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# DOWNLOAD EXCEL
# =====================================================

download_url = (
    "https://docs.google.com/spreadsheets/d/"
    "1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/"
    "export?format=xlsx"
)

sheet_url = (
    "https://docs.google.com/spreadsheets/d/"
    "1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/"
    "edit?usp=sharing"
)


# =====================================================
# CACHE DOWNLOAD
# =====================================================

@st.cache_data(
    ttl=1800,
    show_spinner=False
)
def get_excel_file():

    try:

        response = requests.get(
            download_url,
            timeout=15
        )

        if response.status_code == 200:

            return response.content

    except Exception:

        pass

    return b""


file_bytes = get_excel_file()


# =====================================================
# DOWNLOAD SECTION
# =====================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)


kosong, kanan = st.columns(
    [7, 3]
)


with kanan:

    st.link_button(
        "📄 Lihat Laporan PERKIN 2026",
        sheet_url,
        use_container_width=True
    )

    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True
    )

    st.download_button(
        label="📥 Download Laporan PERKIN 2026",
        data=file_bytes,
        file_name=(
            "PERKIN & REALISASI "
            "PER KAB_KOTA 2026.xlsx"
        ),
        mime=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
        disabled=(
            len(file_bytes) == 0
        )
    )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer-container">

        <div class="footer-title">
            Kementerian Kependudukan dan
            Pembangunan Keluarga / BKKBN
        </div>

        <div class="footer-subtitle">
            Perwakilan BKKBN Provinsi
            Kepulauan Bangka Belitung
        </div>

        <div class="footer-copy">
            Dashboard PERKIN 2026 |
            © BKKBN BANGKA BELITUNG 2026
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
